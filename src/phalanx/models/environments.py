"""Pydantic models for Phalanx environments."""

from __future__ import annotations

from pydantic import BaseModel, Field
from safir.pydantic import CamelCaseModel

from .applications import ApplicationInstance
from .secrets import Secret

__all__ = [
    "Environment",
    "EnvironmentConfig",
]


class EnvironmentConfig(CamelCaseModel):
    """Configuration for a Phalanx environment.

    This is a partial model for the environment :file:`values.yaml` file.
    """

    environment: str
    """Name of the environment."""

    vault_url: str
    """URL of Vault server for this environment."""

    vault_path_prefix: str
    """Prefix of Vault paths, including the Kv2 mount point."""

    applications: list[str] = Field(
        [], description="List of enabled applications"
    )


class Environment(BaseModel):
    """A Phalanx environment and its associated settings."""

    name: str
    """Name of the environment."""

    vault_url: str
    """URL of Vault server for this environment."""

    vault_path_prefix: str
    """Prefix of Vault paths, including the Kv2 mount point."""

    applications: dict[str, ApplicationInstance]
    """Applications enabled for that environment, by name."""

    def all_applications(self) -> list[ApplicationInstance]:
        """Return enabled applications in sorted order."""
        return sorted(self.applications.values(), key=lambda a: a.name)

    def all_secrets(self) -> list[Secret]:
        """Return a list of all secrets regardless of application.

        Returns
        -------
        list of Secret
            All secrets from all applications.
        """
        secrets = []
        for application in self.all_applications():
            secrets.extend(application.secrets)
        return secrets
