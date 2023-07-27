"""Parsing and analysis of Phalanx configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..exceptions import InvalidSecretConfigError, UnknownEnvironmentError
from ..models.applications import Application, ApplicationInstance
from ..models.environments import Environment, EnvironmentConfig
from ..models.secrets import ConditionalSecretConfig, Secret

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

    def _is_condition_satisfied(
        self, instance: ApplicationInstance, condition: str | None
    ) -> bool:
        """Evaluate a secret condition on an application instance.

        This is a convenience wrapper around
        `ApplicationInstance.is_is_values_setting_true` that also treats a
        `None` condition parameter as true.

        Parameters
        ----------
        instance
            Application instance for a specific environment.
        condition
            Condition, or `None` if there is no condition.

        Returns
        -------
        bool
            `True` if condition is `None` or corresponds to a values setting
            whose value is true, `False` otherwise.
        """
        if not condition:
            return True
        else:
            return instance.is_values_setting_true(condition)

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
                env_values = yaml.safe_load(fh)
                if env_values:
                    environment_values[env_name] = env_values

        # Load the secrets configuration.
        secrets_path = base_path / "secrets.yaml"
        secrets = {}
        if secrets_path.exists():
            with secrets_path.open("r") as fh:
                raw_secrets = yaml.safe_load(fh)
            secrets = {
                k: ConditionalSecretConfig.parse_obj(s)
                for k, s in raw_secrets.items()
            }

        # Load the environment-specific secrets configuration.
        environment_secrets = {}
        for path in base_path.glob("secrets-*.yaml"):
            env_name = path.stem[len("secrets-") :]
            with path.open("r") as fh:
                raw_secrets = yaml.safe_load(fh)
            environment_secrets[env_name] = {
                k: ConditionalSecretConfig.parse_obj(s)
                for k, s in raw_secrets.items()
            }

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

        Raises
        ------
        InvalidSecretConfigError
            Raised if the secret configuration has conflicting rules.
        """
        # Merge values with any environment overrides.
        values = application.values
        if environment_name in application.environment_values:
            env_values = application.environment_values[environment_name]
            values = _merge_overrides(values, env_values)

        # Create an initial application instance without secrets so that we
        # can use its class methods.
        instance = ApplicationInstance(
            name=application.name,
            environment=environment_name,
            values=values,
        )

        # Merge secrets with any environment secrets.
        secrets = application.secrets
        if environment_name in application.environment_secrets:
            secrets = application.secrets.copy()
            secrets.update(application.environment_secrets[environment_name])

        # Evaluate the conditions on all of the secrets. Both the top-level
        # condition and any conditions on the copy and generate rules will be
        # resolved, so that any subsequent processing based on the instance no
        # longer needs to worry about conditions.
        required_secrets = []
        for key, config in secrets.items():
            if not self._is_condition_satisfied(instance, config.condition):
                continue
            copy = config.copy_rules
            if copy:
                condition = copy.condition
                if not self._is_condition_satisfied(instance, condition):
                    copy = None
            generate = config.generate
            if generate:
                condition = generate.condition
                if not self._is_condition_satisfied(instance, condition):
                    generate = None
            if copy and generate:
                msg = "Copy and generate rules conflict"
                raise InvalidSecretConfigError(instance.name, key, msg)
            secret = Secret(
                application=application.name,
                key=key,
                description=config.description,
                copy_rules=copy,
                generate=generate,
                value=config.value,
            )
            required_secrets.append(secret)

        # Add the secrets to the new instance and return it.
        instance.secrets = required_secrets
        return instance
