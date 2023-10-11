"""Service for manipulating Phalanx environments."""

from __future__ import annotations

from ..storage.config import ConfigStorage
from ..storage.helm import HelmStorage

__all__ = ["EnvironmentService"]


class EnvironmentService:
    """Service for manipulating Phalanx environments.

    Parameters
    ----------
    config_storage
        Storage object for the Phalanx configuration.
    helm_storage
        Interface to Helm actions.
    """

    def __init__(
        self, config_storage: ConfigStorage, helm_storage: HelmStorage
    ) -> None:
        self._config = config_storage
        self._helm = helm_storage

    def lint(self, environment: str | None = None) -> bool:
        """Lint the Helm chart for environments.

        Parameters
        ----------
        environment
            If given, lint only the specified environment.

        Returns
        -------
        bool
            Whether linting passed.
        """
        if environment:
            return self._helm.lint_environment(environment)
        success = True
        for environment in self._config.list_environments():
            success &= self._helm.lint_environment(environment)
        return success
