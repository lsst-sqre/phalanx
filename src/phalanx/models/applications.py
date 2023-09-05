"""Pydantic models for Phalanx applications."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .secrets import ConditionalSecretConfig, Secret

__all__ = [
    "Application",
    "ApplicationConfig",
    "ApplicationInstance",
    "DocLink",
]


class DocLink(BaseModel):
    """A documentation link for an application.

    This represents an individual array item in the ``phalanx.lsst.io/docs``
    Helm chart annotation in :file:`Chart.yaml`.
    """

    url: str
    """URL to the document."""

    title: str
    """Title of the document."""

    id: str | None
    """Identifier of the document."""

    def to_rst(self) -> str:
        """Format as a reStructuredText link."""
        label = f"{self.id}: {self.title}" if self.id else self.title
        return f"`{label} <{self.url}>`__"


class ApplicationConfig(BaseModel):
    """Configuration for a Phalanx application."""

    name: str
    """Name of the application."""

    namespace: str
    """Namespace to which the application is deployed."""

    chart: dict[str, Any]
    """Parsed Helm :file:`Chart.yaml` file."""

    doc_links: list[DocLink]
    """List of links to documentation about this application."""

    values: dict[str, Any]
    """Base Helm chart values."""

    environment_values: dict[str, dict[str, Any]]
    """Per-environment Helm chart overrides by environment name."""

    secrets: dict[str, ConditionalSecretConfig]
    """Secrets for the application, by secret key."""

    environment_secrets: dict[str, dict[str, ConditionalSecretConfig]]
    """Per-environment secrets for the application, by secret key."""

    @property
    def homepage(self) -> str | None:
        """The Helm home field, typically used for the application's docs."""
        return self.chart.get("home")

    @property
    def source_urls(self) -> list[str]:
        """Application source URLs from the Helm sources field."""
        return self.chart.get("sources", [])


class Application(ApplicationConfig):
    """A Phalanx application that knows which environments use it."""

    active_environments: list[str]
    """Environments on which this application is enabled."""


class ApplicationInstance(BaseModel):
    """A Phalanx application as configured for a specific environment."""

    name: str
    """Name of the application."""

    environment: str
    """Name of the environment for which the application is configured."""

    chart: dict[str, Any]
    """Parsed Helm :file:`Chart.yaml` file."""

    values: dict[str, Any]
    """Merged Helm values for the application in this environment."""

    secrets: dict[str, Secret] = Field(
        {},
        title="Required secrets",
        description=(
            "Secrets required for this application in this environment."
        ),
    )

    def all_static_secrets(self) -> list[Secret]:
        """Return all static secrets for this instance of the application."""
        return [
            s
            for s in self.secrets.values()
            if not (s.copy_rules or s.generate or s.value)
        ]

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
