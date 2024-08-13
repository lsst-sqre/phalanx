"""Service for manipulating Phalanx environments."""

from __future__ import annotations

from datetime import timedelta

from pydantic import SecretStr

from ..exceptions import VaultNotFoundError
from ..github import action_group, add_mask
from ..models.applications import Project
from ..models.environments import Environment
from ..models.vault import VaultCredentials
from ..storage.argocd import ArgoCDStorage
from ..storage.config import ConfigStorage
from ..storage.helm import HelmStorage
from ..storage.kubernetes import KubernetesStorage
from ..storage.vault import VaultClient, VaultStorage

__all__ = ["EnvironmentService"]


class EnvironmentService:
    """Service for manipulating Phalanx environments.

    Parameters
    ----------
    config_storage
        Storage object for the Phalanx configuration.
    argocd_storage
        Interface to Argo CD actions.
    kubernetes_storage
        Interface to direct Kubernetes object manipulation.
    helm_storage
        Interface to Helm actions.
    vault_storage
        Factory class for Vault clients.
    """

    def __init__(
        self,
        *,
        config_storage: ConfigStorage,
        argocd_storage: ArgoCDStorage,
        kubernetes_storage: KubernetesStorage,
        helm_storage: HelmStorage,
        vault_storage: VaultStorage,
    ) -> None:
        self._config = config_storage
        self._argocd = argocd_storage
        self._kubernetes = kubernetes_storage
        self._helm = helm_storage
        self._vault_storage = vault_storage

    def install(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
        git_branch: str | None = None,
    ) -> None:
        """Install a Phalanx environment.

        Parameters
        ----------
        environment_name
            Environment to install.
        vault_credentials
            Credentials to use for Vault access. These will be installed in
            the cluster as a ``Secret`` used by vault-secrets-operator.
        git_branch
            Git branch to point Argo CD at. If not given, defaults to the
            current branch.

        Raises
        ------
        CommandFailedError
            Raised if one of the underlying commands fails.
        ValueError
            Raised if ``appOfAppsName`` is not set in the environment
            configuration.
        VaultNotFoundError
            Raised if a necessary secret was not found in Vault.
        """
        environment = self._config.load_environment(environment_name)
        vault = self._vault_storage.get_vault_client(
            environment, credentials=vault_credentials
        )

        # Get information about the local repository.
        if not git_branch:
            git_branch = self._config.get_git_branch()

        # Get the plain-text Argo CD admin password from Vault and tell GitHub
        # Actions to mask it.
        argocd_password = self._get_argocd_password(vault)

        # Update Helm dependencies.
        self._update_helm_dependencies(["vault-secrets-operator", "argocd"])

        # Perform the installation.
        self._install_vault_secrets_operator(
            environment, vault_credentials, vault.url
        )
        self._install_argocd(environment)
        self._install_app_of_apps(environment, git_branch, argocd_password)
        self._sync_argocd()
        self._sync_infrastructure_applications(environment)
        self._sync_remaining_applications(environment)

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
        for env in self._config.list_environments():
            success &= self._helm.lint_environment(env)
        return success

    def template(self, environment_name: str) -> str:
        """Expand the templates of the top-level chart.

        Run :command:`helm template` for a top-level chart, passing in the
        appropriate parameters for the given environment.

        Parameters
        ----------
        environment_name
            Environment for which to expand the top-level chart.

        Returns
        -------
        str
            Output from :command:`helm template`.

        Raises
        ------
        CommandFailedError
            Raised if Helm fails.
        ValueError
            Raised if ``appOfAppsName`` is not set in the environment
            configuration.
        """
        environment = self._config.load_environment(environment_name)
        if not environment.app_of_apps_name:
            raise ValueError(f"appOfAppsName not set for {environment_name}")
        return self._helm.template_environment(
            environment.name, environment.app_of_apps_name
        )

    @staticmethod
    def _get_argocd_password(vault: VaultClient) -> SecretStr:
        """Retrieve the Argo CD admin password from Vault.

        Parameters
        ----------
        vault
            Vault client to use for retrieving secrets.

        Returns
        -------
        str
            The plain-text Argo CD admin password.

        Raises
        ------
        VaultNotFoundError
            Raised if the admin plain-text password is not found in Vault.
        """
        argocd_secret = vault.get_application_secret("argocd")
        argocd_password = argocd_secret.get("admin.plaintext_password")
        if not argocd_password:
            raise VaultNotFoundError(
                vault.url, f"{vault.path}/argocd", "admin.plaintext_password"
            )
        add_mask(argocd_password)
        return argocd_password

    def _install_vault_secrets_operator(
        self,
        environment: Environment,
        vault_credentials: VaultCredentials,
        vault_url: str,
    ) -> None:
        """Install the vault-secrets-operator application.

        Argo CD depends on this, so it has to be installed and configured with
        its Vault secret first.

        Parameters
        ----------
        environment
            The environment configuration object.
        vault_credentials
            Credentials to use for Vault access.
        vault_url
            URL of the Vault server.
        """
        with action_group("Install vault-secrets-operator"):
            self._kubernetes.create_namespace(
                "vault-secrets-operator", ignore_fail=True
            )
            self._kubernetes.create_vault_secret(
                "vault-credentials",
                "vault-secrets-operator",
                vault_credentials,
            )
            self._helm.dependency_update("vault-secrets-operator")
            self._helm.upgrade_application(
                "vault-secrets-operator",
                environment.name,
                {"vault-secrets-operator.vault.address": vault_url},
            )

    def _install_argocd(self, environment: Environment) -> None:
        """Install the Argo CD application.

        Parameters
        ----------
        environment
            The environment configuration object.
        """
        with action_group("Install Argo CD"):
            self._helm.dependency_update("argocd")
            self._helm.upgrade_application(
                "argocd",
                environment.name,
                {"global.vaultSecretsPath": environment.vault_path_prefix},
            )

    def _install_app_of_apps(
        self,
        environment: Environment,
        git_branch: str,
        argocd_password: SecretStr,
    ) -> None:
        """Create and sync the top-level Argo CD application.

        Parameters
        ----------
        environment
            The environment configuration object.
        git_branch
            The branch of the Git repository to use.
        argocd_password
            The plain-text Argo CD admin password.
        """
        app_of_apps = environment.app_of_apps_name
        if not app_of_apps:
            raise ValueError(f"appOfAppsName not set for {environment.name}")
        with action_group(f"Install {app_of_apps} app-of-apps"):
            self._argocd.login("admin", argocd_password)
            self._argocd.create_environment(
                environment.name,
                app_of_apps,
                git_url=self._config.get_git_url(),
                git_branch=git_branch,
            )
            self._argocd.sync(app_of_apps)
            project = Project.infrastructure
            self._argocd.set_project(app_of_apps, project)

    def _sync_argocd(self) -> None:
        """Sync the Argo CD application.

        Sync and wait for it to finish syncing so that the pods don't restart
        in the middle of proxying another Argo CD operation.
        """
        with action_group("Sync Argo CD"):
            self._argocd.sync("argocd")
            for deployment in (
                "deployment/argocd-server",
                "deployment/argocd-repo-server",
                "statefulset/argocd-application-controller",
            ):
                self._kubernetes.wait_for_rollout(deployment, "argocd")

    def _sync_infrastructure_applications(
        self, environment: Environment
    ) -> None:
        """Sync infrastructure applications that other applications depend on.

        Parameters
        ----------
        environment
            The environment configuration object.
        """
        with action_group("Sync infrastructure applications"):
            for application in (
                "ingress-nginx",
                "cert-manager",
                "postgres",
                "gafaelfawr",
            ):
                if application in environment.applications:
                    self._argocd.sync(application)

    def _sync_remaining_applications(self, environment: Environment) -> None:
        """Sync remaining applications that were not already synced.

        Parameters
        ----------
        environment
            The environment configuration object.
        """
        app_of_apps = environment.app_of_apps_name
        if not app_of_apps:
            raise ValueError(f"appOfAppsName not set for {environment.name}")
        with action_group("Sync remaining applications"):
            self._argocd.sync_all(app_of_apps, timeout=timedelta(minutes=5))

    def _update_helm_dependencies(self, app_names: list[str]) -> None:
        """Update Helm dependencies for the specified applications.

        Parameters
        ----------
        app_names
            List of application names whose dependencies should be updated.
        """
        # Add the dependency repositories of the applications we're installing
        # directly with Helm, and refresh the Helm dependency cache.
        with action_group("Update Helm dependencies"):
            repo_urls = set()
            for app_name in app_names:
                app_urls = self._config.get_dependency_repositories(app_name)
                repo_urls.update(app_urls)
            for url in sorted(repo_urls):
                self._helm.repo_add(url)
            self._helm.repo_update()
