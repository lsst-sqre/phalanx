"""Parsing and analysis of Phalanx configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..exceptions import UnknownEnvironmentError
from ..models.applications import Application, ApplicationInstance
from ..models.environments import Environment, EnvironmentConfig
from ..models.secrets import RequiredSecret, Secret, SecretConfig

__all__ = ["ConfigStorage"]


def _merge_overrides(
    base: dict[str, Any], overrides: dict[str, Any]
) -> dict[str, Any]:
    """Merge values settings with overrides.

    Parameters
    ----------
    base
        Base settings.
    overrides
        Overrides that should take precedence.

    Returns
    -------
    dict
        Merged dictionary.
    """
    for key, value in overrides.items():
        if key in base:
            if isinstance(base[key], dict) and isinstance(value, dict):
                _merge_overrides(base[key], value)
            else:
                base[key] = value
        else:
            base[key] = value
    return base


class ConfigStorage:
    """Analyze Phalanx configuration and convert it to models."""

    def __init__(self) -> None:
        self._path = Path.cwd()

    def load_environment(self, environment_name: str) -> Environment:
        """Load the configuration of a Phalanx environment from disk.

        Parameters
        ----------
        environment_name
            Name of the environment.

        Returns
        -------
        Environment
            Environment configuration.

        Raises
        ------
        UnknownEnvironmentError
            Raised if the named environment has no configuration.
        """
        config = self._load_environment_config(environment_name)
        applications = [self._load_application(a) for a in config.applications]
        instances = {
            a.name: self._resolve_application(a, environment_name)
            for a in applications
        }
        return Environment(name=config.environment, applications=instances)

    def _load_application(self, name: str) -> Application:
        """Load the configuration for an application from disk.

        Parameters
        ----------
        name
            Name of the application.

        Returns
        -------
        Application
            Application data.
        """
        base_path = Path.cwd() / "applications" / name

        # Load main values file.
        values_path = base_path / "values.yaml"
        if values_path.exists():
            with values_path.open("r") as fh:
                values = yaml.safe_load(fh)
        else:
            values = {}

        # Load environment-specific values files.
        environment_values = {}
        for path in base_path.glob("values-*.yaml"):
            env_name = path.stem[len("values-") :]
            with path.open("r") as fh:
                environment_values[env_name] = yaml.safe_load(fh)

        # Load the secrets configuration.
        secrets_path = base_path / "secrets.yaml"
        secrets = []
        if secrets_path.exists():
            with secrets_path.open("r") as fh:
                raw_secrets = yaml.safe_load(fh)
            for key, raw_config in raw_secrets.items():
                config = SecretConfig.parse_obj(raw_config)
                secret = Secret(key=key, application=name, **config.dict())
                secrets.append(secret)

        # Load the environment-specific secrets configuration.
        environment_secrets = {}
        for path in base_path.glob("secrets-*.yaml"):
            env_name = path.stem[len("secrets-") :]
            with path.open("r") as fh:
                raw_secrets = yaml.safe_load(fh)
            env_secrets = []
            for key, raw_config in raw_secrets.items():
                config = SecretConfig.parse_obj(raw_config)
                secret = Secret(key=key, application=name, **config.dict())
                env_secrets.append(secret)
            environment_secrets[env_name] = env_secrets

        # Return the resulting application.
        return Application(
            name=name,
            values=values,
            environment_values=environment_values,
            secrets=secrets,
            environment_secrets=environment_secrets,
        )

    def _load_environment_config(
        self, environment_name: str
    ) -> EnvironmentConfig:
        """Load the configuration for a Phalanx environment.

        Parameters
        ----------
        environment_name
            Name of the environent.

        Returns
        -------
        Environment
            Loaded environment.

        Raises
        ------
        InvalidEnvironmentConfigError
            Raised if the configuration for an environment is invalid.
        UnknownEnvironmentError
            Raised if the named environment has no configuration.
        """
        values_name = f"values-{environment_name}.yaml"
        values_path = Path.cwd() / "environments" / values_name
        if not values_path.exists():
            raise UnknownEnvironmentError(environment_name)
        with values_path.open() as fh:
            values = yaml.safe_load(fh)

        # Eventually this will have more structure, but for now assume any
        # key whose value is a dictionary with an enabled key is indicating an
        # application that is or is not enabled.
        applications = []
        for key, value in values.items():
            if isinstance(value, dict) and "enabled" in value:
                if value["enabled"]:
                    applications.append(key)

        # For now, this is hard-coded, but we'll eventually figure it out from
        # the Argo CD Application resource templates.
        applications.append("argocd")

        # Return the configuration.
        return EnvironmentConfig(
            environment=environment_name, applications=sorted(applications)
        )

    def _resolve_application(
        self, application: Application, environment_name: str
    ) -> ApplicationInstance:
        """Resolve an application to its environment-specific configuration.

        Parameters
        ----------
        application
            Application to resolve.
        environment_name
            Name of the environment the application should be configured for.

        Returns
        -------
        ApplicationInstance
            Resolved application.
        """
        # Merge values with any environment overrides.
        values = application.values
        if environment_name in application.environment_values:
            env_values = application.environment_values[environment_name]
            values = _merge_overrides(values, env_values)

        # Merge secrets with any environment secrets.
        if environment_name in application.environment_secrets:
            env_secrets = application.environment_secrets[environment_name]
            extra_secrets = {s.key: s for s in env_secrets}
            secrets = []
            for secret in application.secrets:
                if secret.key in extra_secrets:
                    secrets.append(extra_secrets[secret.key])
                    del extra_secrets[secret.key]
                else:
                    secrets.append(secret)
            secrets.extend(extra_secrets.values())
        else:
            secrets = application.secrets

        # Create an initial application instance without secrets so that we
        # can use its class methods.
        instance = ApplicationInstance(
            name=application.name,
            environment=environment_name,
            values=values,
        )

        # Filter out the secrets that don't apply to this instance.
        instance.secrets = [
            RequiredSecret.from_secret(s)
            for s in secrets
            if instance.is_condition_met(s.condition)
        ]
        return instance
