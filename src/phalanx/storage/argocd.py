"""Interface to Argo CD operations."""

from __future__ import annotations

from datetime import timedelta

from ..models.applications import Project
from .command import Command

__all__ = ["ArgoCDStorage"]


class ArgoCDStorage:
    """Interface to Argo CD operations.

    Calls the :command:`argocd` command-line client. Used primarily by the
    installer.
    """

    def __init__(self) -> None:
        self._argocd = Command("argocd")

    def create_environment(
        self,
        environment: str,
        app_of_apps_name: str,
        *,
        git_url: str,
        git_branch: str,
    ) -> None:
        """Manually create an Argo CD application.

        Used only by the installer for installing the app of apps to bootstrap
        the environment.

        Parameters
        ----------
        environment
            Name of the environment.
        app_of_apps_name
            Name of the app of apps Argo CD application.
        git_url
            URL to the Phalanx Git repository.
        git_branch
            Name of the branch in that repository from which to pull the Argo
            CD configuration.

        Raises
        ------
        CommandFailedError
            Raised if Argo CD fails.
        """
        self._argocd.run(
            "app",
            "create",
            app_of_apps_name,
            "--repo",
            git_url,
            "--path",
            "environments",
            "--dest-namespace",
            "argocd",
            "--dest-server",
            "https://kubernetes.default.svc",
            "--upsert",
            "--revision",
            git_branch,
            "--helm-set",
            f"repoUrl={git_url}",
            "--helm-set",
            f"targetRevision={git_branch}",
            "--values",
            "values.yaml",
            "--values",
            f"values-{environment}.yaml",
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        )

    def login(self, username: str, password: str) -> None:
        """Authenticate to Argo CD.

        Authenticates using username and password authentication with port
        forwarding. This normally must be done before any other Argo CD
        operations.

        Parameters
        ----------
        username
            Username for authentication. (Usually this will be ``admin``.)
        password
            Password for that user.

        Raises
        ------
        CommandFailedError
            Raised if Argo CD fails.
        """
        self._argocd.run(
            "login",
            "--plaintext",
            "--username",
            username,
            "--password",
            password,
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        )

    def set_project(self, application: str, project: Project) -> None:
        """Set the Argo CD project of an application.

        Parameters
        ----------
        application
            Application to change.
        project
            Project to move it into.

        Raises
        ------
        CommandFailedError
            Raised if Argo CD fails.
        """
        self._argocd.run(
            "app",
            "set",
            application,
            "--project",
            project.value,
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        )

    def sync(
        self, application: str, *, timeout: timedelta = timedelta(minutes=2)
    ) -> None:
        """Sync a specific Argo CD application.

        Parameters
        ----------
        application
            Name of the application.
        timeout
            How long to wait for the sync to complete.

        Raises
        ------
        CommandFailedError
            Raised if Argo CD fails.
        CommandTimedOutError
            Raised if the command timed out. The timeout is also passed to
            Argo CD as an option, so normally the command should fail and
            raise `~phalanx.exceptions.CommandFailedError` instead. This
            exception means the Argo CD timeout didn't work for some reason.
        """
        self._argocd.run(
            "app",
            "sync",
            application,
            "--timeout",
            str(int(timeout.total_seconds())),
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        )

    def sync_all(
        self,
        app_of_apps_name: str,
        *,
        timeout: timedelta = timedelta(seconds=30),
    ) -> None:
        """Sync all Argo CD applications under an app of apps.

        Parameters
        ----------
        app_of_apps_name
            Name of the parent app of apps.
        timeout
            How long to wait for the sync to complete.

        Raises
        ------
        CommandFailedError
            Raised if Argo CD fails.
        CommandTimedOutError
            Raised if the command timed out. The timeout is also passed to
            Argo CD as an option, so normally the command should fail and
            raise `~phalanx.exceptions.CommandFailedError` instead. This
            exception means the Argo CD timeout didn't work for some reason.
        """
        self._argocd.run(
            "app",
            "sync",
            "-l",
            f"argocd.argoproj.io/instance={app_of_apps_name}",
            "--timeout",
            str(int(timeout.total_seconds())),
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        )
