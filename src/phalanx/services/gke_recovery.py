"""Operations to recover a GKE Phalanx cluster from backups."""

from phalanx.models.vault import VaultCredentials
from phalanx.services.cluster import GKEPhalanxClusterService
from phalanx.services.environment import EnvironmentService

__all__ = ["GKERecoveryService"]


# Eventually, this will have two GKECluster services too to run commands
# against both the new and old clusters.
class GKERecoveryService:
    """Operations to recover a GKE Phalanx cluster from backups.

    Parameters
    ----------
    old_cluster
        A service to perform kubectl operations on the old cluster.
    new_cluster
        A service to perform kubectl operations on the new cluster.
    new_environment
        A service to environment installation on the new cluster.
    """

    def __init__(
        self,
        old_cluster: GKEPhalanxClusterService,
        new_cluster: GKEPhalanxClusterService,
        new_environment: EnvironmentService,
    ) -> None:
        self._old_cluster = old_cluster
        self._new_cluster = new_cluster
        self._new_environment = new_environment

    def set_pause_sasquatch(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
    ) -> None:
        """Set a helm value in the sasquatch app to pause Kafka reconciliation.

        Why not just use kubectl to set the annotation directly on the
        Kafka resource? Because during the recovery process, we need to
        sync sasquatch for the first time with reconciliation paused.
        """
        return self._new_environment.set_pause_sasquatch(
            environment_name, vault_credentials
        )
