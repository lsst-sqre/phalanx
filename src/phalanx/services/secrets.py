"""Service to manipulate Phalanx secrets."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

import yaml

from ..exceptions import UnresolvedSecretsError
from ..models.applications import ApplicationInstance
from ..models.environments import Environment
from ..models.secrets import ResolvedSecret, Secret, SourceSecretGenerateRules
from ..storage.config import ConfigStorage
from ..yaml import YAMLFoldedString

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

    def generate_static_template(self, environment_name: str) -> str:
        """Generate a template for providing static secrets.

        The template provides space for all static secrets required for a
        given environment. The resulting file, once the values have been
        added, can be used as input to other secret commands instead of an
        external secret source such as 1Password.

        Parameters
        ----------
        environment_name
            Name of the environment.

        Returns
        -------
        dict
            YAML template the user can fill out, as a string.
        """
        secrets = self.list_secrets(environment_name)
        template: defaultdict[str, dict[str, dict[str, str | None]]]
        template = defaultdict(dict)
        for secret in secrets:
            static = not (secret.copy_rules or secret.generate or secret.value)
            if static:
                template[secret.application][secret.key] = {
                    "description": YAMLFoldedString(secret.description),
                    "value": None,
                }
        return yaml.dump(template, width=72)

    def list_secrets(self, environment_name: str) -> list[Secret]:
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
        return secrets

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
            if isinstance(config.generate, SourceSecretGenerateRules):
                other_key = config.generate.source
                other = resolved.get(config.application, {}).get(other_key)
                if not (other and other.value):
                    return _SecretResolution(status=_SecretStatus.PENDING)
                value = config.generate.generate(other.value)
            else:
                value = config.generate.generate()
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
