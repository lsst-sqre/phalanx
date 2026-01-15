"""Interface to Argo CD operations."""

from datetime import timedelta

from pydantic import SecretStr

from phalanx.models.argocd import ApplicationList

from ..exceptions import CommandFailedError
from ..models.applications import Project
from .command import Command

__all__ = ["ArgoCDStorage"]


class ArgoCDStorage:
    """Interface to Argo CD operations.

    Calls the :command:`argocd` command-line client. Used by the installer and
    for cluster recovery.

    Parameters
    ----------
    context
        The kubectl context to specify for all argocd commands. If this is
        None, then the current context will be used.
    """

    def __init__(self, context: str | None = None) -> None:
        common_args = ["--kube-context", context] if context else []
        self._argocd = Command("argocd", common_args=common_args)

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

    def login(self, username: str, password: SecretStr) -> None:
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
            password.get_secret_value(),
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

    def set_helm_value(self, application: str, key: str, value: str) -> None:
        """Set a helm value for an ArgoCD project.

        This is only used in the cluster recovery process, where we want to
        change some helm values the first time we sync an application, after
        the app-of-apps has already been synced.

        Parameters
        ----------
        application
            Application to change.
        key
            The helm key to change.
        value:
            The Helm value to set.

        Raises
        ------
        CommandFailedError
            Raised if Argo CD fails.
        """
        self._argocd.run(
            "app",
            "set",
            application,
            "--helm-set",
            f"{key}={value}",
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        )

    def sync(
        self,
        application: str,
        *,
        timeout: timedelta = timedelta(minutes=2),
        kind: str | None = None,
    ) -> None:
        """Sync all or part of a specific Argo CD application.

        Parameters
        ----------
        application
            Name of the application.
        timeout
            How long to wait for the sync to complete.
        kind
            If given, only this kind of resource will be synced.

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
        # As of Argo CD 2.10.5, the first sync of Argo CD, cert-manager, and
        # Gafaelfawr always fails with a spurious error claiming the
        # infrastructure project had not been created. This is transient; the
        # second execution succeeds. Therefore, on CommandFailedError, try
        # running the same command again.
        args = [
            "app",
            "sync",
            application,
            "--timeout",
            str(int(timeout.total_seconds())),
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        ]
        if kind:
            args += ["--resource", f"*:{kind}:*"]

        try:
            self._argocd.run(*args)
        except CommandFailedError:
            self._argocd.run(*args)

    def sync_all(
        self,
        app_of_apps_name: str,
        *,
        timeout: timedelta = timedelta(seconds=30),
    ) -> None:
        """Sync all or part of all Argo CD applications under an app of apps.

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
        args = [
            "app",
            "sync",
            "-l",
            f"argocd.argoproj.io/instance={app_of_apps_name}",
            "--timeout",
            str(int(timeout.total_seconds())),
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
        ]
        self._argocd.run(*args)

    def list_applications(self, app_of_apps_name: str) -> ApplicationList:
        """List all of the applications managed by an app of apps.

        Parameters
        ----------
        app_of_apps_name
            Name of the parent app of apps.

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
        args = [
            "app",
            "list",
            "-l",
            f"argocd.argoproj.io/instance={app_of_apps_name}",
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
            "-o",
            "json",
        ]
        output = self._argocd.capture(*args)
        return ApplicationList.model_validate_json(output.stdout)
