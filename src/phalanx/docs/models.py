"""Models of the Phalanx environment and application configurations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml

ENVIRONMENTS_DIR = "science-platform"
"""Directory of the environments Helm chart in Phalanx."""

APPS_DIR = "services"
"""Root directory of the application Helm charts in Phalanx."""


@dataclass(kw_only=True)
class Application:
    """A model for a Phalanx-configured application."""

    name: str
    """Name of the application.

    This name is used to label directories, etc.
    """

    @classmethod
    def load(cls, *, app_dir: Path) -> Application:
        return cls(name=app_dir.name)


@dataclass(kw_only=True)
class Environment:
    """A model for an environment."""

    name: str
    """Name of the Phalanx environment.

    This name is used to label directories, values files, etc.
    """

    domain: str
    """The root domain where the environment is hosted."""

    vault_path_prefix: str
    """The Vault key prefix for this environment."""

    apps: List[Application]
    """The applications that are enabled for this service."""

    @classmethod
    def load(
        cls, *, env_values_path: Path, applications: List[Application]
    ) -> Environment:
        """Load an environment by inspecting the Phalanx repository."""
        # Extract name from dir/values-envname.yaml
        env_values = yaml.safe_load(env_values_path.read_text())
        name = env_values["environment"]

        # Get Application instances active in this environment
        apps: List[Application] = []
        for app in applications:
            try:
                if env_values[app.name]["enabled"] is True:
                    apps.append(app)
            except KeyError:
                continue
        apps.sort(key=lambda a: a.name)

        return Environment(
            name=name,
            domain=env_values["fqdn"],
            vault_path_prefix=env_values["vault_path_prefix"],
            apps=apps,
        )


@dataclass(kw_only=True)
class Phalanx:
    """Root container for Phalanx data."""

    environments: List[Environment] = field(default_factory=list)
    """Phalanx environments."""

    apps: List[Application] = field(default_factory=list)
    """Phalanx applications."""

    @classmethod
    def load_phalanx(cls, root_dir: Path) -> Phalanx:
        """Load the Phalanx git repository.

        Parameters
        ----------
        root_dir : `pathlib.Path`
            The path for the root directory of a Phalanx repository clone.

        Returns
        -------
        phalanx : `Phalanx`
            A model of the Phalanx platform, including environment and
            application configuration.
        """
        apps: List[Application] = []
        envs: List[Environment] = []

        # Gather applications
        for app_dir in root_dir.joinpath(APPS_DIR).iterdir():
            if not app_dir.is_dir():
                continue
            app = Application.load(app_dir=app_dir)
            apps.append(app)
        apps.sort(key=lambda a: a.name)

        # Gather environments
        for env_values_path in root_dir.joinpath(ENVIRONMENTS_DIR).glob(
            "values-*.yaml"
        ):
            if not env_values_path.is_file():
                continue
            env = Environment.load(
                env_values_path=env_values_path, applications=apps
            )
            envs.append(env)

        return cls(environments=envs, apps=apps)
