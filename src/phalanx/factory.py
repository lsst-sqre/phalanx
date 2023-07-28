"""Factory for Phalanx support code components."""

from __future__ import annotations

from .services.secrets import SecretsService
from .storage.config import ConfigStorage

__all__ = ["Factory"]


class Factory:
    """Factory to create Phalanx components."""

    def create_secrets_service(self) -> SecretsService:
        """Create service for manipulating Phalanx secrets.

        Returns
        -------
        SecretsService
            Service for manipulating secrets.
        """
        config_storage = ConfigStorage()
        return SecretsService(config_storage)
