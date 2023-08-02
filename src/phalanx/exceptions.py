"""Exceptions for the Phalanx command-line tool."""

from __future__ import annotations

from collections.abc import Iterable

from .models.secrets import Secret

__all__ = [
    "InvalidEnvironmentConfigError",
    "InvalidSecretConfigError",
    "UnknownEnvironmentError",
    "UnresolvedSecretsError",
    "VaultNotFoundError",
]


class InvalidEnvironmentConfigError(Exception):
    """Configuration for an environment is invalid.

    Parameters
    ----------
    name
        Name of the environment.
    error
        Error message.
    """

    def __init__(self, name: str, error: str) -> None:
        msg = "Invalid configuration for environment {name}: {error}"
        super().__init__(msg)


class InvalidSecretConfigError(Exception):
    """Secret configuration is invalid.

    Parameters
    ----------
    application
        Name of the application.
    key
        Secret key.
    error
        Error message.
    """

    def __init__(self, application: str, key: str, error: str) -> None:
        name = f"{application}/{key}"
        msg = f"Invalid configuration for secret {name}: {error}"
        super().__init__(msg)


class UnresolvedSecretsError(Exception):
    """Some secrets could not be resolved.

    Parameters
    ----------
    secrets
        Secrets that could not be resolved.
    """

    def __init__(self, secrets: Iterable[Secret]) -> None:
        names = [f"{u.application}/{u.key}" for u in secrets]
        names_str = ", ".join(names)
        msg = f"Some secrets could not be resolved: {names_str}"
        super().__init__(msg)


class UnknownEnvironmentError(Exception):
    """No configuration found for an environment name.

    Parameters
    ----------
    name
        Name of the environment.
    """

    def __init__(self, name: str) -> None:
        msg = f"No configuration found for environment {name}"
        super().__init__(msg)


class VaultNotFoundError(Exception):
    """Secret could not be found in Vault.

    Parameters
    ----------
    url
        Base URL of the Vault server.
    path
        Path that was not found.
    """

    def __init__(self, url: str, path: str) -> None:
        msg = f"Vault secret {path} not found in server {url}"
        super().__init__(msg)
