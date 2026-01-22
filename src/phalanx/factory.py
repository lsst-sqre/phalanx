"""Factory for Phalanx support code components."""

from pathlib import Path

from phalanx.constants import GOOGLE_CLOUD_RUN_ID_LABEL

from .services.application import ApplicationService
from .services.cluster import GKEPhalanxClusterService
from .services.environment import EnvironmentService
from .services.gke_backup import GKEBackupService
from .services.secrets import SecretsService
from .services.vault import VaultService
from .storage.argocd import ArgoCDStorage
from .storage.config import ConfigStorage
from .storage.gke_backup import GKEBackupStorage
from .storage.helm import HelmStorage
from .storage.kubernetes import KubernetesStorage
from .storage.onepassword import OnepasswordStorage
from .storage.vault import VaultStorage

__all__ = ["Factory"]


class Factory:
    """Factory to create Phalanx components.

    Parameters
    ----------
    path
        Path to the root of the Phalanx configuration tree.
    """

    def __init__(self, path: Path) -> None:
        self._path = path

    def create_application_service(self) -> ApplicationService:
        """Create service for manipulating Phalanx applications.

        Returns
        -------
        ApplicationService
            Service for manipulating applications.
        """
        config_storage = self.create_config_storage()
        helm_storage = HelmStorage(config_storage)
        return ApplicationService(self._path, config_storage, helm_storage)

    def create_config_storage(self) -> ConfigStorage:
        """Create storage layer for the Phalanx configuration.

        Returns
        -------
        ConfigStorage
            Storage service for loading the Phalanx configuration.
        """
        return ConfigStorage(self._path)

    def create_environment_service(self) -> EnvironmentService:
        """Create service for manipulating Phalanx environments.

        Returns
        -------
        EnvironmentService
            Service for manipulating environments.
        """
        config_storage = self.create_config_storage()
        return EnvironmentService(
            config_storage=config_storage,
            argocd_storage=ArgoCDStorage(),
            kubernetes_storage=self.create_kubernetes_storage(),
            helm_storage=HelmStorage(config_storage),
            vault_storage=VaultStorage(),
        )

    def create_gke_phalanx_cluster_service(
        self, context: str
    ) -> GKEPhalanxClusterService:
        """Create a service for manipulating Kubernetes clusters directly.

        Parameters
        ----------
        context
            The Kubernetes context to pass to all kubectl commands.

        Returns
        -------
        GKEPhalanxClusterService
           A service object for manipulating resources in a Phalanx cluster.
        """
        storage = self.create_kubernetes_storage(context)
        return GKEPhalanxClusterService(storage)

    def create_gke_backup_service(
        self, region: str, project: str, phalanx_run_id: str
    ) -> GKEBackupService:
        """Create a service for using Google Cloud Backup for GKE.

        This service is scoped to running operations in a single region and
        project.

        Parameters
        ----------
        region
            The Google Cloud region to run comands against.
        project
            The Google Cloud project to run comands against.
        phalanx_run_id
            An identifier to put in the ``phalanx-run`` label on every Google
            Cloud resource that is created with this service. This is helpful
            in resuming backup and restore process after a Google Cloud
            operation fails (which does happen intermittently), and in cleaning
            up these resources later.

        Returns
        -------
        GKEBackupService
           A service object for manipulating resources in a Phalanx cluster.
        """
        labels = {GOOGLE_CLOUD_RUN_ID_LABEL: phalanx_run_id}
        storage = GKEBackupStorage(
            region=region, project=project, labels=labels
        )
        return GKEBackupService(storage, phalanx_run_id)

    def create_kubernetes_storage(
        self, context: str | None = None
    ) -> KubernetesStorage:
        """Create storage object for interacting with Kubernetes.

        Parameters
        ----------
        context
            The Kubernetes context to pass to all kubectl commands. If this is
            None, then commands will be run against the current context in the
            kube config file.

        Returns
        -------
        KubernetesStorage
            Storage object for interacting with Kubernetes.
        """
        return KubernetesStorage(context)

    def create_onepassword_storage(self) -> OnepasswordStorage:
        """Create storage object for interacting with 1Password.

        Returns
        -------
        OnepasswordStorage
            Storage object for interacting with 1Password.
        """
        return OnepasswordStorage()

    def create_secrets_service(self) -> SecretsService:
        """Create service for manipulating Phalanx secrets.

        Returns
        -------
        SecretsService
            Service for manipulating secrets.
        """
        return SecretsService(
            self.create_config_storage(),
            self.create_onepassword_storage(),
            VaultStorage(),
        )

    def create_vault_service(self) -> VaultService:
        """Create service for managing Vault tokens and policies.

        Returns
        -------
        VaultService
            Service for managing Vault tokens and policies.
        """
        config_storage = self.create_config_storage()
        vault_storage = VaultStorage()
        return VaultService(config_storage, vault_storage)
