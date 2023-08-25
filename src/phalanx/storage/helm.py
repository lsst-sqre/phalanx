"""Interface to Helm operations."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..exceptions import HelmFailedError
from ..storage.config import ConfigStorage

__all__ = ["HelmStorage"]


class HelmStorage:
    """Interface to Helm operations.

    Provides an interface to use Helm to create and process templates and to
    use Helm to install charts in a Kubernetes cluster.

    Parameters
    ----------
    config_storage
        Storage object for the Phalanx configuration.
    """

    def __init__(self, config_storage: ConfigStorage) -> None:
        self._config = config_storage

    def create(self, application: str, starter: str) -> None:
        """Use :command:`helm create` to create a new application chart.

        Parameters
        ----------
        application
            Name of the new application.
        starter
            Name of the Helm starter template to use.

        Raises
        ------
        UnknownStarterError
            Raised if the specified Helm starter was not found.
        """
        starter_path = self._config.get_starter_path(starter)
        application_path = self._config.get_application_chart_path(application)
        self._run_helm(
            "create",
            "-p",
            str(starter_path),
            application,
            cwd=application_path.parent,
        )

    def _run_helm(
        self, command: str, *args: str, cwd: Path | None = None
    ) -> None:
        """Run Helm, checking for errors.

        Any output from Helm is printed to standard output and standard error.

        Parameters
        ----------
        command
            Helm subcommand to run.
        *args
            Arguments for that subcommand.
        cwd
            If provided, change working directories to this path before
            running the Helm command.

        Raises
        ------
        HelmFailedError
            Raised if Helm fails.
        """
        try:
            subprocess.run(["helm", command, *args], check=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            raise HelmFailedError(command, args, e) from e
