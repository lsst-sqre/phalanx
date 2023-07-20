"""Pydantic models for Phalanx environments."""

from __future__ import annotations

from pydantic import BaseModel

from .applications import ApplicationInstance

__all__ = [
    "Environment",
    "EnvironmentConfig",
]


class EnvironmentConfig(BaseModel):
    """Configuration for a Phalanx environment.

    This is a partial model for the environment :file:`values.yaml` file.
    """

    environment: str
    """Name of the environment."""

    applications: list[str]
    """List of enabled applications."""


class Environment(BaseModel):
    """A Phalanx environment and its associated settings."""

    name: str
    """Name of the environment."""

    applications: dict[str, ApplicationInstance]
    """Applications enabled for that environment, by name."""

    def all_applications(self) -> list[ApplicationInstance]:
        """Return enabled applications in sorted order."""
        return sorted(self.applications.values(), key=lambda a: a.name)
