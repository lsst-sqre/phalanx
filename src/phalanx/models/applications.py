"""Pydantic models for Phalanx applications."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .secrets import RequiredSecret, Secret

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

    secrets: list[Secret]
    """Base secret configuration for the application."""

    environment_secrets: dict[str, list[Secret]]
    """Per-environment secrets for the application."""


class ApplicationInstance(BaseModel):
    """A Phalanx application as configured for a specific environment."""

    name: str
    """Name of the application."""

    environment: str
    """Name of the environment for which the application is configured."""

    values: dict[str, Any]
    """Merged Helm values for the application in this environment."""

    secrets: list[RequiredSecret] = []
    """Secrets required for this application in this environment."""

    def is_condition_met(self, condition: str | None) -> bool:
        """Determine whether a secret condition has been met.

        Conditions are used both for the secret as a whole and for the
        ``copy`` and ``generate`` sections. The condition is met if it either
        is `None` or if it is a string pointing to a values parameter for the
        application instance that is set to a true value.

        Parameters
        ----------
        condition
            Condition to check.

        Returns
        -------
        bool
            `True` if the condition was met or does not exist, `False`
            otherwise.
        """
        if not condition:
            return True
        path = condition.split(".")
        values = self.values
        for key in path:
            if key not in values:
                return False
            values = values[key]
        return bool(values)
