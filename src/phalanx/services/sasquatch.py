"""Service for manipulating Sasquatch in a Phalanx environment."""

from __future__ import annotations

from ..storage.sasquatch import SasquatchStorage

__all__ = ["SasquatchService"]


class SasquatchService:
    """Service for manipulating sasquatch in a Phalanx environment.

    Parameters
    ----------
    kube_context
        The context name of the kubernetes cluster that will be modified.
    sasquatch_storage
        Factory class for Sasquatch manipulation.
    """

    def __init__(
        self,
        kube_context: str,
        sasquatch_storage: SasquatchStorage,
    ) -> None:
        self._kube_context = kube_context
        self._sasquatch_storage = sasquatch_storage

    def cluster_id_on_disk(self) -> str:
        """Get the Sasquatch Kafka cluster ID in the data on disk.

        We need to do this if we're restoring a Strimzi Kafka cluster from
        volumes on disk, because the auto-generated random cluster ID on the
        new Kafka CR will not match, and there is no way to set it at resource
        creation time. So, we need to get the old cluster ID from the data on
        the restored disk and manually change the cluster ID on the Strimzi
        CRs.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        return self._sasquatch_storage.cluster_id_on_disk()

    def pause_reconciliation(self) -> None:
        """Pause Strimzi Kafka CR reconciliation.

        We need to pause the Strimzi Kafka CR reconciliation loop when we are
        restoring a cluster from backed-up persistent volumes. We need to
        manually change the cluster ID, which we can't do while the
        reconciliation loop is running.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        self._sasquatch_storage.pause_reconciliation()
        print("Sasquatch Strimzi Kafka reconciliation paused")

    def resume_reconciliation(self) -> None:
        """Resume Strimzi Kafka CR reconciliation.

        When we're done making configuration changes, we need to unpause
        Strimzi resource reconciliation.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        self._sasquatch_storage.resume_reconciliation()
        print("Sasquatch Strimzi Kafka reconciliation resumed")

    def set_cluster_id(self, cluster_id: str) -> None:
        """Configure a Strimzi Kafka cluster with an explicitly specified ID.

        When we're recovering a Strimzi Kafka cluster from
        backed-up persistent storage, We need to manually
        change the cluster ID to match the original cluster
        ID.

        For more info on Strimzi Kafka cluster recovery, see:
        https://strimzi.io/docs/operators/latest/deploying#assembly-cluster-recovery-volume-str
        """
        self._sasquatch_storage.set_cluster_id(cluster_id)
        print(f"Sasquatch Strimzi Kafka cluster ID set to {cluster_id}")

    def retain_pvs(self) -> None:
        """Set all of the sasquatch bound PersistentVolumes to be retained."""
        self._sasquatch_storage.retain_pvs()
        print("All Sasquatch PersistentVolume reclaim policies set to Retain")

    def delete_strimzi_podsets(self) -> None:
        """Destroy all Strimzi podset resources.

        When reconciliation is unpaused on the Strimzi Kafka resource, this
        will cause all of the Kafka pods to be recreated. This is useful when
        manually setting the cluster ID for a Strimzi Kafka cluster.
        """
        self._sasquatch_storage.delete_strimzi_podsets()
        print("All Sasquatch StrimziPodsets destroyed")

    def delete_pvcs(self) -> None:
        """Delete the Sasquatch PVCs and remove the associations on the PVs.

        This will first change the reclaimPolicy on associated PVs to Retain.
        This needs to be done when the PVCs are not attached to any pods.
        """
        self._sasquatch_storage.delete_pvcs()

    def recover(self, *, delete_pvcs: bool = False) -> None:
        """Recover a Sasquatch Kafka cluster from disk backups.

        Prerequisites:

        * The backing PVCs and PVs have been restored
        * The strimzi and sasquatch Phalanx apps have been synced.
        """
        cluster_id = self.cluster_id_on_disk()

        self.retain_pvs()
        self.pause_reconciliation()
        self.set_cluster_id(cluster_id)
        self.delete_strimzi_podsets()
        if delete_pvcs:
            self.delete_pvcs()
        self.resume_reconciliation()
        print("Sasquatch recovery complete")
