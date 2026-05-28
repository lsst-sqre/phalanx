"""Service for manipulating Phalanx Kubernetes clusters directly."""

import traceback

from ..constants import (
    GKE_LOAD_BALANCER_SERVICE_FINALIZERS,
    PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION,
    PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
    PREVIOUS_REPLICA_COUNT_ANNOTATION,
    RECOVER_IGNORE_SERVICES,
    RECOVER_SCALE_WORKLOAD_EXCLUDE,
    SASQUATCH_BROKER_PVC,
    SASQUATCH_KAFKA_NAME,
    SASQUATCH_NAMESPACE,
)
from ..exceptions import (
    InvalidLoadBalancerServiceStateError,
    ServiceMissingTrafficPolicyError,
)
from ..models.kubernetes import NamespacedResource, Service, Workload
from ..storage.kubernetes import KubernetesStorage

__all__ = ["GKEPhalanxClusterService"]


_KAFKA = NamespacedResource(
    kind="Kafka", namespace=SASQUATCH_NAMESPACE, name=SASQUATCH_KAFKA_NAME
)
"""The Sasquatch Kafka resource."""


class GKEPhalanxClusterService:
    """Kubernetes operations on a GKE Phalanx cluster.

    These operations are not in the EnviromentService because:

    * They do not necessarily correspond 1-1 to a Phalanx enviroment.
    * They are often part of tasks that involve multiple clusters, so passing
      an explicit context is less error prone, and allows the operations to be
      automated without having to manually change the kubectl current context.
    * Some of the operations are specific to Google Cloud GKE clusters, like
      waiting for an associated cloud load balancer to be destroyed when
      converting a Service from LoadBalancer to ClusterIP.

    For example, when recovering a GCP cluster from backups while the old
    cluster still exists, you will need to work with two clusters, both of
    which are associated with the same environment.

    Parameters
    ----------
    kubernetes_storage
        Interface to direct Kubernetes object manipulation.
    """

    def __init__(self, kubernetes_storage: KubernetesStorage) -> None:
        self._kubernetes = kubernetes_storage
        self.context = self._kubernetes.context

    def suspend_cronjobs(self) -> None:
        """Suspend all CronJobs in all Phalanx apps."""
        cronjobs = self._kubernetes.get_phalanx_cronjobs()
        return self._kubernetes.suspend_cronjobs(cronjobs)

    def resume_cronjobs(self) -> None:
        """Resume all CronJobs in all Phalanx apps."""
        cronjobs = self._kubernetes.get_phalanx_cronjobs()
        return self._kubernetes.resume_cronjobs(cronjobs)

    def scale_down_workloads(self) -> None:
        """Scale down (almost) all Phalanx workloads.

        During cluster rebuilds when there is an old and a new cluster, certain
        workloads can't be running in both clusters at the same time, or else
        state external to the cluster could be corrupted.

        We'll leave ArgoCD running so the scaled-down cluster can still be
        inspected.
        """
        workloads = self._get_workloads(exclude=RECOVER_SCALE_WORKLOAD_EXCLUDE)
        sasquatch_workloads = [
            workload
            for workload in workloads
            if workload.namespace == SASQUATCH_NAMESPACE
        ]

        for workload in sasquatch_workloads:
            workloads.remove(workload)

        # Scale down other workloads before sasquatch so we don't get errors
        # about metrics.
        for workload in workloads:
            if not self._check_workload_state(workload):
                continue

            self._kubernetes.annotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
                value=str(workload.replicas),
            )
            self._kubernetes.scale(workload, 0)

        for workload in sasquatch_workloads:
            if not self._check_workload_state(workload):
                continue

            self._kubernetes.annotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
                value=str(workload.replicas),
            )
            self._kubernetes.scale(workload, 0)

        for workload in sasquatch_workloads:
            self._kubernetes.wait_for_rollout(
                namespace=workload.namespace, name=workload.get_kind_name()
            )

    def scale_up_workloads(self) -> None:
        """Scale up (almost) all Phalanx workloads to their previous counts.

        This is only intended to be run after a scale down operation.
        """
        # Scale up all sasquatch workloads so we don't have apps starting
        # without metrics
        workloads = self._get_workloads(exclude=RECOVER_SCALE_WORKLOAD_EXCLUDE)
        sasquatch_workloads = [
            workload
            for workload in workloads
            if workload.namespace == SASQUATCH_NAMESPACE
        ]

        for workload in sasquatch_workloads:
            workloads.remove(workload)

        for workload in sasquatch_workloads:
            self._check_workload_state(workload)
            if workload.previous_replica_count is None:
                continue
            self._kubernetes.scale(workload, workload.previous_replica_count)
            self._kubernetes.deannotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
            )

        # Scale up all of the other workloads
        for workload in workloads:
            if not self._check_workload_state(workload):
                continue
            if workload.previous_replica_count is None:
                continue
            self._kubernetes.scale(workload, workload.previous_replica_count)
            self._kubernetes.deannotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
            )

    def pause_kafka_reconciliation(self) -> None:
        """Pause Strimzi reconciliation of the Sasquatch Kafka cluster.

        During some recovery operations, we want to modify resources that are
        managed by the Strimzi operator. The Strimzi operator will
        automatically revert any changes we make, so we have to pause Strimzi
        reconciliation if we want our changes to persist.

        https://strimzi.io/docs/operators/latest/full/deploying#proc-pausing-reconciliation-str
        """
        self._kubernetes.annotate(
            _KAFKA,
            key="strimzi.io/pause-reconciliation",
            value="true",
            overwrite=True,
        )

    def resume_kafka_reconciliation(self) -> None:
        """Resume Strimzi reconciliation of the Sasquatch Kafka cluster.

        https://strimzi.io/docs/operators/latest/full/deploying#proc-pausing-reconciliation-str
        """
        self._kubernetes.deannotate(
            _KAFKA, key="strimzi.io/pause-reconciliation"
        )

    def get_kafka_cluster_id(self) -> str:
        """Get the Strimzi cluster id from a Kafka node PVC.

        When recovering a Strimzi Kafka cluster from backed-up
        PersistentVolumes, the cluster id generated from applying a Strimzi
        Kafka resource will not match the cluster id in the data in the
        recovered volumes. We need to get the cluster id from the data on the
        volume before we let strimzi reconcile the Kafka resource, or the Kafka
        pods will not be able to start.

        Command is from the Strimzi recovery docs here:
        https://strimzi.io/docs/operators/latest/full/deploying#proc-cluster-recovery-volume-str

        This method assumes a lot about what various resources are called.
        """
        pvc_name = SASQUATCH_BROKER_PVC
        command = (
            r"grep cluster.id /disk/kafka-log*/meta.properties"
            r" | awk -F'=' '{print $2}'"
        )
        overrides = {
            "spec": {
                "containers": [
                    {
                        "name": "busybox",
                        "image": "busybox",
                        "command": ["/bin/sh", "-c", command],
                        "volumeMounts": [
                            {"name": "disk", "mountPath": "/disk"}
                        ],
                    }
                ],
                "volumes": [
                    {
                        "name": "disk",
                        "persistentVolumeClaim": {"claimName": pvc_name},
                    }
                ],
            }
        }

        return self._kubernetes.run_with_overrides(
            namespace=SASQUATCH_NAMESPACE, overrides=overrides
        )

    def set_kafka_cluster_id(self, cluster_id: str) -> None:
        """Configure a Strimzi Kafka cluster with an explicitly specified ID.

        When we're recovering a Strimzi Kafka cluster from backed-up persistent
        storage, We need to manually change the cluster ID to match the
        original cluster ID.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str

        Parameters
        ----------
        cluster_id
            The new cluster ID for the Kafka cluster.
        """
        self._kubernetes.patch_status(_KAFKA, {"clusterId": cluster_id})

    def scale_up_all(self) -> None:
        """Scale up all Phalanx workloads and resume all crons."""
        self.resume_kafka_reconciliation()
        self.restore_service_ips()
        self.scale_up_workloads()
        self.resume_cronjobs()

    def scale_down_all(self) -> None:
        """Scale down all Phalanx workloads except ArgoCD and crons."""
        self.pause_kafka_reconciliation()
        self.release_service_ips()
        self.suspend_cronjobs()
        self.scale_down_workloads()

    def get_phalanx_load_balancer_services(self) -> list[Service]:
        """Get all Services of type LoadBalancer for all Phalanx apps.

        We say a Service is in a Phalanx app if it has an ArgoCD label.

        Returns
        -------
        list[Service]
            A list of all of the LoadBalancer Services provisioned by Phalanx
            apps.
        """
        return self._kubernetes.get_phalanx_load_balancer_services()

    def release_service_ips(self) -> list[Service]:
        """Release all IPs on LoadBalancer Services for all Phalanx apps.

        This will clear any spec.loadBalancerIPs, then change the Service type
        from LoadBalancer to ClusterIP, then back to LoadBalancer.

        This can be used when recovering a Phalanx cluster to another GKE
        cluster while the old cluster is still running.

        Returns
        -------
        list[Service]
            A list of Services with refreshed IPs.

        Raises
        ------
        InvalidLoadBalancerServiceStateError
            If the service resource does not have exactly one of
            spec.loadBalancerIP or an annotation for the previous
            loadBalancerIP set.

        ServiceMissingTrafficPolicyError
            If the service resource does not have an externalTrafficPolicy.
        """
        new_services = []
        services = self._kubernetes.get_phalanx_load_balancer_services()
        for service in services:
            if service.namespace in RECOVER_IGNORE_SERVICES:
                print(
                    "Not releasing IP address for services in"
                    " {service.namespace} because there is no way to declare a"
                    " specific loadBalancerIP on them."
                )
                continue

            self._check_service_state(service)
            if not service.external_traffic_policy:
                continue
            if service.previous_loadbalancer_ip:
                print(
                    f"Service {service.namespace}/{service.name} already has"
                    f" the {PREVIOUS_LOAD_BALANCER_IP_ANNOTATION} annotation"
                    f" set, skipping"
                )
                continue
            self._kubernetes.annotate(
                service,
                key=PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
                value=str(service.load_balancer_ip),
            )
            self._kubernetes.annotate(
                service,
                key=PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION,
                value=service.external_traffic_policy.value,
            )
            self._kubernetes.remove_service_load_balancer_ip(service)
            self._refresh_service_ingress(service)
            self._kubernetes.update_service_external_traffic_policy(
                service, service.external_traffic_policy
            )
            new_service = self._kubernetes.get_service(
                name=service.name, namespace=service.namespace
            )
            new_services.append(new_service)

        return new_services

    def restore_service_ips(self) -> list[Service]:
        """Restore all IPs on LoadBalancer Services for all Phalanx apps.

        This is only intended to be run after a release operation because it
        depends on an annotation set during that operation.

        Returns
        -------
        list[Service]
            A list of Services with restored IPs.

        Raises
        ------
        InvalidLoadBalancerServiceStateError
            If the service resource does not have exactly one of
            spec.loadBalancerIP or an annotation for the previous
            loadBalancerIP set.

        """
        new_services = []
        services = self._kubernetes.get_phalanx_load_balancer_services()
        for service in services:
            if (
                not service.previous_loadbalancer_ip
                or not service.previous_external_traffic_policy
            ):
                continue
            try:
                self._check_service_state(service)
            except Exception:
                traceback.print_exc()
                continue
            self._kubernetes.add_service_load_balancer_ip(
                service, service.previous_loadbalancer_ip
            )
            self._kubernetes.deannotate(
                service,
                key=PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
            )
            self._kubernetes.deannotate(
                service,
                key=PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION,
            )
            self._refresh_service_ingress(service)
            self._kubernetes.update_service_external_traffic_policy(
                service, service.previous_external_traffic_policy
            )
            new_service = self._kubernetes.get_service(
                name=service.name, namespace=service.namespace
            )
            new_services.append(new_service)

        return new_services

    def retain_pvs(self) -> None:
        """Set the persistentVolumeReclaimPolicy to Retain for all PVs."""
        self._kubernetes.retain_pvs()

    def _refresh_service_ingress(self, service: Service) -> None:
        """Destroy and recreate the ingress associated with a Service.

        Parameters
        ----------
        service
            The Service whose associated ingress to refresh.
        """
        self._kubernetes.set_service_to_cluster_ip(service)
        self._kubernetes.wait_for_resource_no_finalizers(
            service, GKE_LOAD_BALANCER_SERVICE_FINALIZERS
        )
        self._kubernetes.set_service_to_load_balancer(service)
        self._kubernetes.wait_for_service_ingress(service)

    def _check_service_state(self, service: Service) -> None:
        """Ensure a LoadBalancer Service is not in an incorrect state.

        Parameters
        ----------
        service
            The service whose state to check.
        """
        exactly_one = (
            service.load_balancer_ip,
            service.previous_loadbalancer_ip,
        )
        if all(exactly_one) or not any(exactly_one):
            raise InvalidLoadBalancerServiceStateError(service)

        if not service.external_traffic_policy:
            raise ServiceMissingTrafficPolicyError(service)

    def _get_workloads(self, exclude: frozenset[str]) -> list[Workload]:
        """Get all Phalanx workloads in the cluster except ArgoCD workloads.

        Parameters
        ----------
        exclude
            Exclude these workloads from the returned list.

        Returns
        -------
        list[Workload]
            A list of Phalanx workloads execpt for ArgoCD workloads.
        """
        deployments = self._kubernetes.get_phalanx_deployments()
        statefulsets = self._kubernetes.get_phalanx_stateful_sets()

        return [
            workload
            for workload in deployments + statefulsets
            if workload.namespace not in exclude
        ]

    def _check_workload_state(self, workload: Workload) -> bool:
        """Make sure the workload is in an OK state to be scaled.

        Parameters
        ----------
        workload
          The workload to check the state of.

        Returns
        -------
        bool
            True if the workload is in an OK state to be scaled

        """
        if workload.previous_replica_count:
            if workload.replicas != 0:
                msg = (
                    f"Workload is in an invalid state to be scaled. If it has"
                    f" a previous annotation, then it must have a replica"
                    f" count of zero. Workload: {workload.kind}"
                    f" {workload.namespace} {workload.name}"
                )
                print(msg)
                return False
        return True

    def kube_version(self) -> str:
        """Return the version of the kubectl client and kubernetes server.

        Useful for checking that kubectl can connect to a cluster using a given
        context.
        """
        return self._kubernetes.version()
