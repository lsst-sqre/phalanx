"""Factory for Phalanx support code components."""

from __future__ import annotations

from pathlib import Path

from .services.application import ApplicationService
from .services.environment import EnvironmentService
from .services.secrets import SecretsService
from .services.vault import VaultService
from .storage.argocd import ArgoCDStorage
from .storage.config import ConfigStorage
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

    def create_kubernetes_storage(self) -> KubernetesStorage:
        """Create storage object for interacting with Kubernetes.

        Returns
        -------
        KubernetesStorage
            Storage object for interacting with Kubernetes.
        """
        return KubernetesStorage()

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
