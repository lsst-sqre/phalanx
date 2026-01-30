"""Service to coordinate other services for cluster recovery."""

from phalanx.models.vault import VaultCredentials
from phalanx.services.gke_backup import GKEBackupService

from .cluster import GKEPhalanxClusterService
from .recovery_environment import RecoveryEnvironmentService

__all__ = ["GKERecoveryService"]


class GKERecoveryService:
    """Service to coordinate other services for cluster recovery.

    Parameters
    ----------
    source_cluster
        The Google Cloud name of the old cluster.
    destination_cluster
        The Google Cloud name of the new cluster.
    environment
        The name of the Phalanx environment to load config from.
    git_branch
        The name of the Git branch to sync from in ArgoCD.
    gke_backup_service
        Performs Google Cloud API calls to backup and restore GKE clusters.
    old_cluster_service
        Performs kubectl operations against the old cluster.
    new_cluster_service
        Performs kubectl operations against the new cluster.
    recovery_environment_service
        Performs ArgoCD and Helm operations (and some kubectl operations)
        against the new cluster.
    vault_credentials
        Credentials to read from the Vault instance that backs the cluster
        environment.
    """

    def __init__(
        self,
        *,
        source_cluster: str,
        destination_cluster: str,
        environment: str,
        git_branch: str | None,
        gke_backup_service: GKEBackupService,
        new_cluster_service: GKEPhalanxClusterService,
        old_cluster_service: GKEPhalanxClusterService,
        recovery_environment_service: RecoveryEnvironmentService,
        vault_credentials: VaultCredentials,
    ) -> None:
        self._source_cluster = source_cluster
        self._destination_cluster = destination_cluster
        self._environment_name = environment
        self._git_branch = git_branch
        self._gke_backup = gke_backup_service
        self._new_cluster = new_cluster_service
        self._old_cluster = old_cluster_service
        self._environment = recovery_environment_service
        self._vault_credentials = vault_credentials

    def recover(self) -> None:
        self._gke_backup.backup_and_restore_pvcs(
            source_cluster=self._source_cluster,
            destination_cluster=self._destination_cluster,
        )
        self._old_cluster.scale_down_all()

        self._new_cluster.retain_pvs()
        sasquatch_cluster_id = (
            self._new_cluster.get_sasquatch_kafka_cluster_id()
        )
        print(f"Sasquatch Kafka cluster id: {sasquatch_cluster_id}")

        self._environment.start_recover(
            self._environment_name, self._vault_credentials, self._git_branch
        )
        self._new_cluster.set_sasquatch_cluster_id(sasquatch_cluster_id)
        self._new_cluster.resume_sasquatch_kafka_reconciliation()
        self._environment.unset_pause_sasquatch(
            self._environment_name, self._vault_credentials
        )
        self._environment.finish_recover(
            self._environment_name, self._vault_credentials, self._git_branch
        )

    def preflight_check(self) -> None:
        """Check that everything is in a good state to start recovery."""
        self._check_kubectl_connect()

    def _check_kubectl_connect(self) -> None:
        """Check that kubectl can connect to clusters."""
        try:
            self._old_cluster.kube_version()
            print("Source cluster reachable with kubectl.")
        except:
            print("Could not connect to source cluster with kubectl.")
            raise

        try:
            self._new_cluster.kube_version()
            print("Destination cluster reachable with kubectl.")
        except:
            print("Could not connect to destination cluster with kubectl.")
            raise

    def _check_static_ips(self) -> None:
        """Check that any loadBalancerIP is static in Google Cloud."""
        services = self._old_cluster.get_phalanx_load_balancer_services()
