"""Pydantic models for Phalanx applications."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .secrets import ConditionalSecretConfig, Secret

__all__ = [
    "Application",
    "ApplicationInstance",
]


class Application(BaseModel):
    """A Phalanx application."""

    name: str
    """Name of the application."""

    values: dict[str, Any]
    """Base Helm chart values."""

    environment_values: dict[str, dict[str, Any]]
    """Per-environment Helm chart overrides by environment name."""

    secrets: dict[str, ConditionalSecretConfig]
    """Secrets for the application, by secret key."""

    environment_secrets: dict[str, dict[str, ConditionalSecretConfig]]
    """Per-environment secrets for the application, by secret key."""


class ApplicationInstance(BaseModel):
    """A Phalanx application as configured for a specific environment."""

    name: str
    """Name of the application."""

    environment: str
    """Name of the environment for which the application is configured."""

    values: dict[str, Any]
    """Merged Helm values for the application in this environment."""

    secrets: list[Secret] = []
    """Secrets required for this application in this environment."""

    def is_values_setting_true(self, setting: str) -> bool:
        """Determine whether a given Helm values setting is true.

        The values setting is considered true if the corresponding values
        parameter is present and set to a true value (a non-empty array or
        dictionary or a string, number, or boolean value that evaluates to
        true in Python).

        Parameters
        ----------
        setting
            Setting to check.

        Returns
        -------
        bool
            `True` if the setting was set to a true value, `False` otherwise.
        """
        path = setting.split(".")
        values = self.values
        for key in path:
            if key not in values:
                return False
            values = values[key]
        return bool(values)
