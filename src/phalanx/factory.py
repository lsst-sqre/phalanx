"""Factory for Phalanx support code components."""

from __future__ import annotations

from .services.secrets import SecretsService
from .storage.config import ConfigStorage
from .storage.vault import VaultStorage

__all__ = ["Factory"]


class Factory:
    """Factory to create Phalanx components."""

    def create_config_storage(self) -> ConfigStorage:
        """Create storage layer for the Phalanx configuration.

        Returns
        -------
        ConfigStorage
            Storage service for loading the Phalanx configuration.
        """
        return ConfigStorage()

    def create_secrets_service(self) -> SecretsService:
        """Create service for manipulating Phalanx secrets.

        Returns
        -------
        SecretsService
            Service for manipulating secrets.
        """
        config_storage = self.create_config_storage()
        vault_storage = VaultStorage()
        return SecretsService(config_storage, vault_storage)
