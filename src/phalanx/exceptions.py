"""Exceptions for the Phalanx command-line tool."""

from __future__ import annotations

import subprocess
from collections.abc import Iterable

from .models.secrets import Secret

__all__ = [
    "ApplicationExistsError",
    "HelmFailedError",
    "InvalidApplicationConfigError",
    "InvalidEnvironmentConfigError",
    "InvalidSecretConfigError",
    "MalformedOnepasswordSecretError",
    "MissingOnepasswordSecretsError",
    "NoOnepasswordConfigError",
    "NoOnepasswordCredentialsError",
    "UnknownEnvironmentError",
    "UnresolvedSecretsError",
    "VaultNotFoundError",
]


class ApplicationExistsError(Exception):
    """Application being created already exists.

    Parameters
    ----------
    name
        Name of the application.
    """

    def __init__(self, name: str) -> None:
        msg = f"Application {name} already exists"
        super().__init__(msg)


class HelmFailedError(Exception):
    """A Helm command failed.

    Parameters
    ----------
    command
        Subcommand being run.
    args
        Arguments to that subcommand.
    exc
        Exception reporting the failure.
    """

    def __init__(
        self,
        command: str,
        args: Iterable[str],
        exc: subprocess.CalledProcessError,
    ) -> None:
        args_str = " ".join(args)
        msg = f"helm {command} {args_str} failed with status {exc.returncode}"
        super().__init__(msg)
        self.stdout = exc.stdout
        self.stderr = exc.stderr


class InvalidApplicationConfigError(Exception):
    """Configuration for an application is invalid.

    Parameters
    ----------
    name
        Name of the application.
    error
        Error message.
    environment
        Name of the affected environment.
    """

    def __init__(
        self, name: str, error: str, *, environment: str | None = None
    ) -> None:
        msg = f"Invalid configuration for application {name}"
        if environment:
            msg += f" in environment {environment}"
        msg += f": {error}"
        super().__init__(msg)


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
        msg = f"Invalid configuration for environment {name}: {error}"
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


class MalformedOnepasswordSecretError(Exception):
    """A secret stored in 1Password was malformed.

    The most common cause of this error is that the secret was marked as
    encoded in base64 but couldn't be decoded.

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
        msg = f"Value of secret {name} is malformed: {error}"
        super().__init__(msg)


class MissingOnepasswordSecretsError(Exception):
    """Secrets are missing from 1Password.

    Parameters
    ----------
    secrets
        List of strings identifying missing secrets. These will either be a
        bare application name, indicating the entire application item is
        missing from 1Password, or the application name followed by a space,
        indicating the 1Password item doesn't have that field.
    """

    def __init__(self, secrets: Iterable[str]) -> None:
        self.secrets = list(secrets)
        msg = f'Missing 1Password items or fields: {", ".join(self.secrets)}'
        super().__init__(msg)


class NoOnepasswordConfigError(Exception):
    """Environment does not use 1Password."""


class NoOnepasswordCredentialsError(Exception):
    """1Password is configured, but no credentials were supplied."""

    def __init__(self) -> None:
        msg = "No 1Password Connect credentials (OP_CONNECT_TOKEN) set"
        super().__init__(msg)


class UnresolvedSecretsError(Exception):
    """Some secrets could not be resolved.

    Parameters
    ----------
    secrets
        Secrets that could not be resolved.
    """

    def __init__(self, secrets: Iterable[Secret]) -> None:
        self.secrets = [f"{u.application}/{u.key}" for u in secrets]
        msg = f'Some secrets could not be resolved: {", ".join(self.secrets)}'
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
