"""Manipulate Sasquatch in a Phalanx environment."""

__all__ = ["SasquatchStorage"]


import json

from phalanx.exceptions import CommandFailedError

from .. import constants
from .command import Command

__all__ = ["SasquatchStorage"]


class SasquatchStorage:
    """Manipulate Sasquatch in a kubernetes cluster."""

    def __init__(self, kube_context: str) -> None:
        self._kubectl = Command("kubectl")
        self._kube_context = kube_context

    def cluster_id_on_disk(self) -> str:
        """Get the Strimzi Kafka cluster ID in the data on disk.

        We need to do this if we're restoring a Strimzi Kafka cluster from
        volumes on disk, because the auto-generated random cluster ID on the
        new Kafka CR will not match, and there is no way to set it at resource
        creation time. So, we need to get the old cluster ID from the data on
        the restored disk and manually change the cluster ID on the Strimzi
        CRs.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        command = (
            "grep cluster.id /disk/kafka-log*/meta.properties | awk -F'='"
            " '{print $2}'"
        )
        overrides = {
            "spec": {
                "affinity": {
                    "podAffinity": {
                        "requiredDuringSchedulingIgnoredDuringExecution": [
                            {
                                "topologyKey": "kubernetes.io/hostname",
                                "labelSelector": {
                                    "matchExpressions": [
                                        {
                                            "key": "strimzi.io/pod-name",
                                            "operator": "In",
                                            "values": [
                                                constants.SASQUATCH_KAFKA_POD
                                            ],
                                        }
                                    ]
                                },
                            }
                        ]
                    }
                },
                "containers": [
                    {
                        "name": "busybox",
                        "image": "busybox",
                        "command": [
                            "/bin/sh",
                            "-c",
                            command,
                        ],
                        "volumeMounts": [
                            {
                                "name": "disk",
                                "mountPath": "/disk",
                            }
                        ],
                    }
                ],
                "volumes": [
                    {
                        "name": "disk",
                        "persistentVolumeClaim": {
                            "claimName": constants.SASQUATCH_KAFKA_PVC_NAME
                        },
                    }
                ],
            }
        }

        overrides_json = json.dumps(overrides)

        try:
            result = self._kubectl.capture(
                "--context",
                self._kube_context,
                "--namespace",
                constants.SASQUATCH_NAMESPACE,
                "run",
                "tmp",
                "-itq",
                "--rm",
                "--restart",
                "Never",
                "--image",
                "foo",
                "--overrides",
                overrides_json,
            )
        except CommandFailedError as e:
            print(e.stdout)
            print(e.stderr)
        return result.stdout.strip()

    def pause_reconciliation(self) -> None:
        """Pause Strimzi Kafka CR reconciliation.

        We need to pause the Strimzi Kafka CR reconciliation loop when we are
        restoring a cluster from backed-up persistent volumes. We need to
        manually change the cluster ID, which we can't do while the
        reconciliation loop is running.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        self._kubectl.run(
            "--context",
            self._kube_context,
            "--namespace",
            constants.SASQUATCH_NAMESPACE,
            "annotate",
            "Kafka",
            "sasquatch",
            "strimzi.io/pause-reconciliation=true",
        )

    def resume_reconciliation(self) -> None:
        """Resume Strimzi Kafka CR reconciliation.

        When we're done making configuration changes, we need to unpause
        Strimzi resource reconciliation.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        self._kubectl.run(
            "--context",
            self._kube_context,
            "--namespace",
            constants.SASQUATCH_NAMESPACE,
            "annotate",
            "Kafka",
            "sasquatch",
            "strimzi.io/pause-reconciliation-",
        )

    def set_cluster_id(self, cluster_id: str) -> None:
        """Configure a Strimzi Kafka cluster with an explicitly specified ID.

        When we're recovering a Strimzi Kafka cluster from
        backed-up persistent storage, We need to manually
        change the cluster ID to match the original cluster
        ID.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        # Patch the kafka resource
        self._kubectl.run(
            "--context",
            self._kube_context,
            "--namespace",
            constants.SASQUATCH_NAMESPACE,
            "patch",
            "Kafka",
            "sasquatch",
            "--type",
            "merge",
            "--subresource",
            "status",
            "--patch",
            f"status: {{clusterId: {cluster_id}}}",
        )

        nodepools = self._get_multiple("KafkaNodePool")
        for pool in nodepools:
            # Patch the KafkaNodePool resources
            self._kubectl.run(
                "--context",
                self._kube_context,
                "--namespace",
                constants.SASQUATCH_NAMESPACE,
                "patch",
                "KafkaNodePool",
                pool,
                "--type",
                "merge",
                "--subresource",
                "status",
                "--patch",
                f"status: {{clusterId: {cluster_id}}}",
            )

    def retain_pvs(self) -> None:
        """Set all of the sasquatch bound PersistentVolumes to be retained."""
        pvs = self._get_multiple("PersistentVolumeClaim", ".spec.volumeName")
        for pv in pvs:
            self._kubectl.run(
                "--context",
                self._kube_context,
                "patch",
                "PersistentVolume",
                pv,
                "-p",
                '{"spec": {"persistentVolumeReclaimPolicy" : "Retain"}}',
            )

    def delete_strimzi_podsets(self) -> None:
        """Destroy all Strimzi podset resources.

        When reconciliation is unpaused on the Strimzi Kafka resource, this
        will cause all of the Kafka pods to be recreated. This is useful when
        manually setting the cluster ID for a Strimzi Kafka cluster.
        """
        podsets = self._get_multiple("StrimziPodSet")
        for podset in podsets:
            self._kubectl.run(
                "--context",
                self._kube_context,
                "--namespace",
                constants.SASQUATCH_NAMESPACE,
                "delete",
                "StrimziPodSet",
                podset,
            )

    def delete_pvcs(self) -> None:
        """Delete the Sasquatch PVCs and remove the associations on the PVs.

        This will first change the reclaimPolicy on associated PVs to Retain.
        This needs to be done when the PVCs are not attached to any pods.
        """
        self.retain_pvs()

        pvcs = self._get_multiple(
            "PersistentVolumeClaim", labels=["strimzi.io/kind=Kafka"]
        )

        pvs = self._get_multiple(
            "PersistentVolumeClaim",
            ".spec.volumeName",
            labels=["strimzi.io/kind=Kafka"],
        )

        for pvc in pvcs:
            self._kubectl.run(
                "--context",
                self._kube_context,
                "--namespace",
                constants.SASQUATCH_NAMESPACE,
                "delete",
                "PersistentVolumeClaim",
                pvc,
            )

        for pv in pvs:
            self._kubectl.run(
                "--context",
                self._kube_context,
                "patch",
                "PersistentVolume",
                pv,
                "--patch",
                "spec: {claimRef: {uid: null, resourceVersion: null }}",
            )

    def _get_multiple(
        self,
        resource: str,
        attribute: str = ".metadata.name",
        labels: list[str] | None = None,
    ) -> list[str]:
        """Get multiple Kubernetes resources in the Sasquatch namespace."""
        args = [
            "--context",
            self._kube_context,
            "--namespace",
            constants.SASQUATCH_NAMESPACE,
            "get",
            resource,
            "--template",
            "{{ range .items }}{{ " + attribute + ' }}{{ "\\n" }}{{ end }}',
        ]

        if labels:
            for label in labels:
                args += ["-l", label]
        raw = self._kubectl.capture(*args)
        return raw.stdout.strip().split()
