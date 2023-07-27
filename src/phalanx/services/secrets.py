"""Service to manipulate Phalanx secrets."""

from __future__ import annotations

import os
import secrets
from base64 import urlsafe_b64encode
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import SecretStr

from ..exceptions import UnresolvedSecretsError
from ..models.applications import ApplicationInstance
from ..models.environments import Environment
from ..models.secrets import (
    ResolvedSecret,
    Secret,
    SecretGenerateRules,
    SecretGenerateType,
)
from ..storage.config import ConfigStorage

__all__ = ["SecretsService"]


class _SecretStatus(Enum):
    """Status of a secret resolution."""

    DROP = "DROP"
    KEEP = "KEEP"
    PENDING = "PENDING"


@dataclass
class _SecretResolution:
    """Status of the resolution of a secret."""

    status: _SecretStatus
    """Status of the secret."""

    secret: ResolvedSecret | None = None
    """Resolved secret, if status is ``KEEP``."""


class SecretsService:
    """Service to manipulate Phalanx secrets.

    Parameters
    ----------
    config_storage
        Storage object for the Phalanx configuration.
    """

    def __init__(self, config_storage: ConfigStorage) -> None:
        self._config = config_storage

    def list_secrets(self, environment_name: str) -> list[ResolvedSecret]:
        """List all required secrets for the given environment.

        Parameters
        ----------
        environment_name
            Name of the environment.

        Returns
        -------
        list of ResolvedSecret
            Secrets required for the given environment.
        """
        environment = self._config.load_environment(environment_name)
        secrets = []
        for application in environment.all_applications():
            secrets.extend(application.secrets)
        return self._resolve_secrets(secrets, environment)

    def _generate_secret(
        self, config: SecretGenerateRules, source: SecretStr | None = None
    ) -> SecretStr:
        """Generate the value of a secret.

        Parameters
        ----------
        config
            Rules for generating the secret.
        source
            Secret on which this secret is based.

        Returns
        -------
        SecretStr
            Newly-generated secret.
        """
        match config.type:
            case SecretGenerateType.password:
                return SecretStr(secrets.token_hex(32))
            case SecretGenerateType.gafaelfawr_token:
                key = urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
                secret = urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
                return SecretStr(f"gt-{key}.{secret}")
            case SecretGenerateType.fernet_key:
                return SecretStr(Fernet.generate_key().decode())
            case SecretGenerateType.rsa_private_key:
                private_key = rsa.generate_private_key(
                    backend=default_backend(),
                    public_exponent=65537,
                    key_size=2048,
                )
                private_key_bytes = private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
                return SecretStr(private_key_bytes.decode())
            case SecretGenerateType.bcrypt_password_hash:
                if not source:
                    raise RuntimeError("bcrypt-password-hash with no source")
                password_hash = bcrypt.hashpw(
                    source.get_secret_value().encode(),
                    bcrypt.gensalt(rounds=15),
                )
                return SecretStr(password_hash.decode())
            case SecretGenerateType.mtime:
                date = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
                return SecretStr(date)

    def _resolve_secrets(
        self, secrets: list[Secret], environment: Environment
    ) -> list[ResolvedSecret]:
        """Resolve the secrets for a Phalanx environment.

        Resolving secrets is the process where the secret configuration is
        resolved using per-environment Helm chart values to generate the list
        of secrets required for a given environment and their values.

        Parameters
        ----------
        secrets
            Secret configuration by application and key.
        environment
            Phalanx environment for which to resolve secrets.

        Returns
        -------
        list of ResolvedSecret
            Resolved secrets by application and secret key.

        Raises
        ------
        UnresolvedSecretsError
            Raised if some secrets could not be resolved.
        """
        resolved: defaultdict[str, dict[str, ResolvedSecret]]
        resolved = defaultdict(dict)
        unresolved = list(secrets)
        left = len(unresolved)
        while unresolved:
            secrets = unresolved
            unresolved = []
            for config in secrets:
                instance = environment.applications[config.application]
                resolution = self._resolve_secret(config, instance, resolved)
                if resolution.status == _SecretStatus.KEEP:
                    secret = resolution.secret
                    if not secret:
                        raise RuntimeError("Resolved secret with no secret")
                    resolved[secret.application][secret.key] = secret
                if resolution.status == _SecretStatus.PENDING:
                    unresolved.append(config)
            if len(unresolved) >= left:
                raise UnresolvedSecretsError(unresolved)
            left = len(unresolved)
        return sorted(
            [s for sl in resolved.values() for s in sl.values()],
            key=lambda s: (s.application, s.key),
        )

    def _resolve_secret(
        self,
        config: Secret,
        instance: ApplicationInstance,
        resolved: dict[str, dict[str, ResolvedSecret]],
    ) -> _SecretResolution:
        """Resolve a single secret.

        Parameters
        ----------
        config
            Configuration of the secret.
        instance
            Application instance owning this secret.
        resolved
            Other secrets for that environment that have already been
            resolved.

        Returns
        -------
        SecretResolution
            Results of attempting to resolve this secret.
        """
        # If a value was already provided, this is the easy case.
        if config.value:
            return _SecretResolution(
                status=_SecretStatus.KEEP,
                secret=ResolvedSecret(
                    key=config.key,
                    application=config.application,
                    value=config.value,
                ),
            )

        # Do copying or generation if configured.
        if config.copy_rules:
            application = config.copy_rules.application
            other = resolved.get(application, {}).get(config.copy_rules.key)
            if not other:
                return _SecretResolution(status=_SecretStatus.PENDING)
            return _SecretResolution(
                status=_SecretStatus.KEEP,
                secret=ResolvedSecret(
                    key=config.key,
                    application=config.application,
                    value=other.value,
                ),
            )
        if config.generate:
            if config.generate.source:
                other_key = config.generate.source
                other = resolved.get(config.application, {}).get(other_key)
                if not other:
                    return _SecretResolution(status=_SecretStatus.PENDING)
                value = self._generate_secret(config.generate, other.value)
            else:
                value = self._generate_secret(config.generate)
            return _SecretResolution(
                status=_SecretStatus.KEEP,
                secret=ResolvedSecret(
                    key=config.key,
                    application=config.application,
                    value=value,
                ),
            )

        # The remaining case is that the secret is a static secret.
        secret = ResolvedSecret(
            key=config.key, application=config.application, static=True
        )
        return _SecretResolution(status=_SecretStatus.KEEP, secret=secret)
