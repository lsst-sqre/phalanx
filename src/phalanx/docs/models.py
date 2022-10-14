"""Models of the Phalanx environment and application configurations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

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

    env_values: Dict[str, Dict]
    """The parsed Helm values for each environment."""

    @classmethod
    def load(cls, *, app_dir: Path) -> Application:
        # Load values files for each environment
        env_values: Dict[str, Dict] = {}
        for values_path in app_dir.glob("values-*.yaml"):
            env_name = values_path.stem.removeprefix("values-")
            env_values[env_name] = yaml.safe_load(values_path.read_text())

        return cls(name=app_dir.name, env_values=env_values)


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

    @property
    def argocd_url(self) -> Optional[str]:
        """Path to the Argo CD UI."""
        argocd = self.get_app("argocd")
        if argocd is None:
            return None

        try:
            return argocd.env_values[self.name]["argo-cd"]["server"]["config"][
                "url"
            ]
        except KeyError:
            # Environments like minikube don't expose an argo cd URL
            return None

    @property
    def identity_provider(self) -> str:
        """A description of the identity provider for Gafaelfawr."""
        gafaelfawr = self.get_app("gafaelfawr")
        if gafaelfawr is None:
            return "Unknown"

        config_values = gafaelfawr.env_values[self.name]["config"]
        if "cilogon" in config_values:
            return "CILogon"

        if "github" in config_values:
            return "GitHub"

        if "oidc" in config_values:
            return "OIDC"

        return "Unknown"

    def get_app(self, name) -> Optional[Application]:
        """Get the named application."""
        for app in self.apps:
            if app.name == name:
                return app
        return None

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
            if app.name == "argocd":
                # argocd is a special case because it's not toggled per env
                apps.append(app)
                continue

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
