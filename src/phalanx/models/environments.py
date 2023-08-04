"""Pydantic models for Phalanx environments."""

from __future__ import annotations

from pydantic import Field
from safir.pydantic import CamelCaseModel

from .applications import ApplicationInstance
from .secrets import Secret

__all__ = [
    "Environment",
    "EnvironmentConfig",
]


class EnvironmentVaultConfig(CamelCaseModel):
    """Vault configuration for a specific environment."""

    vault_url: str
    """URL of Vault server for this environment."""

    vault_path_prefix: str
    """Prefix of Vault paths, including the Kv2 mount point."""


class EnvironmentConfig(EnvironmentVaultConfig):
    """Configuration for a Phalanx environment.

    This is a partial model for the environment :file:`values.yaml` file.
    """

    environment: str
    """Name of the environment."""

    applications: list[str] = Field(
        [], description="List of enabled applications"
    )


class Environment(EnvironmentVaultConfig):
    """A Phalanx environment and its associated settings."""

    name: str
    """Name of the environment."""

    vault_url: str
    """URL of Vault server for this environment."""

    vault_path_prefix: str
    """Prefix of Vault paths, including the Kv2 mount point."""

    applications: dict[str, ApplicationInstance]
    """Applications enabled for that environment, by name."""

    class Config:
        allow_population_by_field_name = True

    def all_applications(self) -> list[ApplicationInstance]:
        """Return all enabled applications in sorted order."""
        return sorted(self.applications.values(), key=lambda a: a.name)

    def all_secrets(self) -> list[Secret]:
        """Return all secrets regardless of application."""
        secrets = []
        for application in self.all_applications():
            secrets.extend(application.secrets)
        return secrets
