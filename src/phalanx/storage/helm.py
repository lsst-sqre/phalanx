"""Interface to Helm operations."""

from __future__ import annotations

import subprocess
import sys
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

    def dependency_update(self, application: str) -> None:
        """Download chart dependencies for an application.

        Tell Helm to update any third-party chart dependencies for an
        application and store them in the :file:`charts` subdirectory. This is
        a prerequisite for :command:`helm lint` or :command:`helm template`.

        Assumes that remote repositories have already been refreshed with
        `repo_update` and tells Helm to skip that.

        Parameters
        ----------
        application
            Application whose dependencies should be updated.
        """
        application_path = self._config.get_application_chart_path(application)
        self._run_helm(
            "dependency", "update", "--skip-refresh", cwd=application_path
        )

    def lint_application(
        self, application: str, environment: str, values: dict[str, str]
    ) -> bool:
        """Lint an application chart with Helm.

        Assumes that :command:`helm dependency update` has already been run to
        download any third-party charts. Any output is sent to standard output
        and standard error, and if Helm fails, a failure message will be
        printed to standard error.

        Parameters
        ----------
        application
            Name of the application.
        environment
            Name of the environment in which to lint that application chart,
            used to select the :file:`values-{environment}.yaml` file to add.
        values
            Extra key/value pairs to set, reflecting the settings injected by
            Argo CD.

        Returns
        -------
        bool
            Whether linting passed.
        """
        application_path = self._config.get_application_chart_path(application)
        set_arg = ",".join(f"{k}={v}" for k, v in values.items())
        try:
            result = self._capture_helm(
                "lint",
                "--strict",
                "--values",
                "values.yaml",
                "--values",
                f"values-{environment}.yaml",
                "--set",
                set_arg,
                cwd=application_path,
            )
        except HelmFailedError as e:
            self._print_lint_output(application, environment, e.stdout)
            if e.stderr:
                sys.stderr.write(e.stderr)
            msg = (
                f"Error: Application {application} in environment"
                f" {environment} has errors\n"
            )
            sys.stderr.write(msg)
            return False
        else:
            self._print_lint_output(application, environment, result.stdout)
            if result.stderr:
                sys.stderr.write(result.stderr)
            return True

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

    def repo_update(self) -> None:
        """Update Helm's cache of upstream repository indices."""
        self._run_helm("repo", "update")

    def _capture_helm(
        self, command: str, *args: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess:
        """Run Helm, checking for errors and capturing the output.

        Parameters
        ----------
        command
            Helm subcommand to run.
        *args
            Arguments for that subcommand.
        cwd
            If provided, change working directories to this path before
            running the Helm command.

        Returns
        -------
        subprocess.CompletedProcess
            Results of the process, containing the standard output and
            standard error streams.

        Raises
        ------
        HelmFailedError
            Raised if Helm fails.
        """
        try:
            result = subprocess.run(
                ["helm", command, *args],
                check=True,
                cwd=cwd,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise HelmFailedError(command, args, e) from e
        return result

    def _print_lint_output(
        self, application: str, environment: str, output: str | None
    ) -> None:
        """Print filtered output from Helm's lint.

        :command:`helm lint` has no apparent way to disable certain checks,
        and there are some warnings that we will never care about. It also
        doesn't have very useful output formatting.

        Parameters
        ----------
        application
            Name of the application.
        environment
            Name of the environment in which to lint that application chart,
        output
            Raw output from :command:`helm lint`.
        """
        if not output:
            return
        for line in output.removesuffix("\n").split("\n"):
            if "icon is recommended" in line:
                continue
            if line == "":
                continue
            if "1 chart(s) linted" in line:
                continue
            if "==> Linting ." in line:
                print(f"==> Linting {application} (environment {environment})")
            else:
                print(line)

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
