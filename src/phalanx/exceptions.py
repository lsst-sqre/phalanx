"""Exceptions for the Phalanx command-line tool."""

from __future__ import annotations

from collections.abc import Iterable

from .models.secrets import RequiredSecret, Secret

__all__ = [
    "InvalidEnvironmentConfigError",
    "InvalidSecretConfigError",
    "UnknownEnvironmentError",
    "UnresolvedSecretsError",
]


class InvalidEnvironmentConfigError(Exception):
    """Configuration for an environment is invalid."""

    def __init__(self, name: str, error: str) -> None:
        msg = "Invalid configuration for environment {name}: {error}"
        super().__init__(msg)


class InvalidSecretConfigError(Exception):
    """Secret configuration is invalid."""

    def __init__(self, config: Secret | RequiredSecret, error: str) -> None:
        name = f"{config.application}/{config.key}"
        msg = f"Invalid configuration for secret {name}: {error}"
        super().__init__(msg)


class UnresolvedSecretsError(Exception):
    """Some secrets could not be resolved."""

    def __init__(self, secrets: Iterable[RequiredSecret]) -> None:
        names = [f"{u.application}/{u.key}" for u in secrets]
        names_str = ", ".join(names)
        msg = f"Some secrets could not be resolved: {names_str}"
        super().__init__(msg)


class UnknownEnvironmentError(Exception):
    """No configuration found for an environment name."""

    def __init__(self, name: str) -> None:
        msg = f"No configuration found for environment {name}"
        super().__init__(msg)
