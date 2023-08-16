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

    @property
    def vault_path(self) -> str:
        """Vault path without the initial Kv2 mount point."""
        _, path = self.vault_path_prefix.split("/", 1)
        return path

    @property
    def vault_read_approle(self) -> str:
        """Name of the Vault read AppRole for this environment."""
        # AppRole names cannot contain /, so we'll use only the final
        # component of the path for the AppRole name.
        vault_path = self.vault_path
        if "/" in vault_path:
            _, approle_name = vault_path.rsplit("/", 1)
            return approle_name
        else:
            return vault_path

    @property
    def vault_write_token(self) -> str:
        """Display name of the Vault write token for this environment.

        Unlike AppRole names, this could include a slash, but use the same
        name as the AppRole for consistency and simplicity.
        """
        return self.vault_read_approle

    @property
    def vault_read_policy(self) -> str:
        """Name of the Vault read policy for this environment."""
        return f"{self.vault_path}/read"

    @property
    def vault_write_policy(self) -> str:
        """Name of the Vault write policy for this environment."""
        return f"{self.vault_path}/write"


class EnvironmentConfig(EnvironmentVaultConfig):
    """Configuration for a Phalanx environment.

    This is a partial model for the environment :file:`values.yaml` file.
    """

    name: str
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
