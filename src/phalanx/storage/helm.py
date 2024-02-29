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

    def create(
        self, project: str, application: str, starter: HelmStarter
    ) -> None:
        """Use :command:`helm create` to create a new application chart.

        Parameters
        ----------
        project
            Name of the project.
        application
            Name of the new application.
        starter
            Name of the Helm starter template to use.
        """
        starter_path = self._config.get_starter_path(starter)
        application_path = self._config.get_new_application_chart_path(
            project, application
        )
        self._run_helm(
            "create",
            "-p",
            str(starter_path),
            application,
            cwd=application_path.parent,
        )

    def dependency_update(
        self, application: str, *, quiet: bool = False
    ) -> None:
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
        quiet
            Whether to suppress Helm's standard output.
        """
        application_path = self._config.get_application_chart_path(application)
        self._run_helm(
            "dependency",
            "update",
            "--skip-refresh",
            cwd=application_path,
            quiet=quiet,
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

        # helm lint complains about any chart without a templates directory,
        # but many of our charts are wrappers around third-party charts and
        # intentionally don't have such a directory. To silence the warning,
        # create an empty templates directory if needed. Git ignores empty
        # directories, so this is essentially a no-op in a Git checkout.
        if not (application_path / "templates").exists():
            (application_path / "templates").mkdir()

        # Run helm lint with the appropriate flag for the environment in which
        # the chart is being linted.
        set_arg = ",".join(f"{k}={v}" for k, v in values.items())
        try:
            result = self._capture_helm(
                "lint",
                application,
                "--strict",
                "--values",
                f"{application}/values.yaml",
                "--values",
                f"{application}/values-{environment}.yaml",
                "--set",
                set_arg,
                cwd=application_path.parent,
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

    def lint_environment(self, environment: str) -> bool:
        """Lint the top-level chart for an environment with Helm.

        Any output is sent to standard output and standard error, and if Helm
        fails, a failure message will be printed to standard error.

        Parameters
        ----------
        environment
            Name of the environment.

        Returns
        -------
        bool
            Whether linting passed.
        """
        path = self._config.get_environment_chart_path()
        try:
            result = self._capture_helm(
                "lint",
                path.name,
                "--strict",
                "--values",
                f"{path.name}/values.yaml",
                "--values",
                f"{path.name}/values-{environment}.yaml",
                cwd=path.parent,
            )
        except HelmFailedError as e:
            self._print_lint_output(None, environment, e.stdout)
            if e.stderr:
                sys.stderr.write(e.stderr)
            msg = (
                f"Error: Top-level chart for environment {environment} has"
                " errors\n"
            )
            sys.stderr.write(msg)
            return False
        else:
            self._print_lint_output(None, environment, result.stdout)
            if result.stderr:
                sys.stderr.write(result.stderr)
            return True

    def repo_add(self, url: str, *, quiet: bool = False) -> None:
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
        quiet
            Whether to suppress Helm's standard output.

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
        self._run_helm("repo", "add", name, url, quiet=quiet)

    def repo_update(self, *, quiet: bool = False) -> None:
        """Update Helm's cache of upstream repository indices.

        Parameters
        ----------
        quiet
            Whether to suppress Helm's standard output.
        """
        self._run_helm("repo", "update", quiet=quiet)

    def template_application(
        self, application: str, environment: str, values: dict[str, str]
    ) -> str:
        """Expand an application chart into its Kubernetes resources.

        Runs :command:`helm template` to expand a chart into its Kubernetes
        resources for a given environment. Assumes that :command:`helm
        dependency update` has already been run to download any third-party
        charts. Any output to standard error is passed along.

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
        str
            Kubernetes resources created by the chart.

        Raises
        ------
        HelmFailedError
            Raised if Helm fails.
        """
        application_path = self._config.get_application_chart_path(application)
        set_arg = ",".join(f"{k}={v}" for k, v in values.items())
        try:
            result = self._capture_helm(
                "template",
                application,
                str(application_path),
                "--include-crds",
                "--values",
                f"{application}/values.yaml",
                "--values",
                f"{application}/values-{environment}.yaml",
                "--set",
                set_arg,
                cwd=application_path.parent,
            )
        except HelmFailedError as e:
            if e.stderr:
                sys.stderr.write(e.stderr)
            raise
        if result.stderr:
            sys.stderr.write(result.stderr)
        return result.stdout

    def template_environment(self, environment: str) -> str:
        """Expand the top-level chart into its Kubernetes resources.

        Runs :command:`helm template` to expand the top-level chart into its
        Kubernetes resources for a given environment. Any output to standard
        error is passed along.

        Parameters
        ----------
        environment
            Name of the environment for which to expand the chart.

        Returns
        -------
        str
            Kubernetes resources created by the chart.

        Raises
        ------
        HelmFailedError
            Raised if Helm fails.
        """
        path = self._config.get_environment_chart_path()
        try:
            result = self._capture_helm(
                "template",
                "science-platform",
                str(path),
                "--include-crds",
                "--values",
                "environments/values.yaml",
                "--values",
                f"environments/values-{environment}.yaml",
                cwd=path.parent,
            )
        except HelmFailedError as e:
            if e.stderr:
                sys.stderr.write(e.stderr)
            raise
        if result.stderr:
            sys.stderr.write(result.stderr)
        return result.stdout

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
        self, application: str | None, environment: str, output: str | None
    ) -> None:
        """Print filtered output from Helm's lint.

        :command:`helm lint` has no apparent way to disable certain checks,
        and there are some warnings that we will never care about. It also
        doesn't have very useful output formatting.

        Parameters
        ----------
        application
            Name of the application, or `None` if linting the top-level chart.
        environment
            Name of the environment in which to lint that application chart,
        output
            Raw output from :command:`helm lint`.
        """
        if not output:
            return
        if application:
            prelude = f"==> Linting {application} (environment {environment})"
        else:
            prelude = f"==> Linting top-level chart for {environment}"
        for line in output.removesuffix("\n").split("\n"):
            if "icon is recommended" in line:
                continue
            if line == "":
                continue
            if "1 chart(s) linted" in line:
                continue
            if line.startswith("==> Linting"):
                print(prelude)
            else:
                print(line)

    def _run_helm(
        self,
        command: str,
        *args: str,
        cwd: Path | None = None,
        quiet: bool = False,
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
        cmdline = ["helm", command, *args]
        stdout = subprocess.DEVNULL if quiet else None
        try:
            subprocess.run(cmdline, check=True, stdout=stdout, cwd=cwd)
        except subprocess.CalledProcessError as e:
            raise HelmFailedError(command, args, e) from e
