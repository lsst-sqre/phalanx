"""Interface to Helm operations."""

from __future__ import annotations

import subprocess
from pathlib import Path
from urllib.parse import urlparse

from ..exceptions import HelmFailedError
from ..models.helm import HelmStarter
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

    def create(self, application: str, starter: HelmStarter) -> None:
        """Use :command:`helm create` to create a new application chart.

        Parameters
        ----------
        application
            Name of the new application.
        starter
            Name of the Helm starter template to use.
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

    def repo_add(self, url: str) -> None:
        """Add a Helm chart repository to Helm's cache.

        Used primarily to enable Helm linting and templating, since both
        require any third-party chart repositories be added first.

        Annoyingly, Helm requires you to name repositories, but chart
        configurations don't include repository names. Automating adding Helm
        repositories therefore requires making up a name. This uses some
        arbitrary heuristics that produce consistent names and hopefully won't
        produce conflicts.

        Parameters
        ----------
        url
            Chart repository to add.

        Raises
        ------
        ValueError
            Raised if the Helm repository URL is invalid.
        """
        hostname = urlparse(url).hostname
        if not hostname:
            raise ValueError(f"Invalid Helm repository URL {url}")
        if hostname.endswith("github.io"):
            name = hostname.split(".", 1)[0]
        elif "." in hostname:
            name = hostname.split(".")[-2]
        else:
            name = hostname
        self._run_helm("repo", "add", name, url)

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
