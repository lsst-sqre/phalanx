"""Service for manipulating Phalanx environments."""

from __future__ import annotations

from datetime import timedelta

from ..exceptions import CommandFailedError, VaultNotFoundError
from ..github import action_group
from ..models.applications import Project
from ..models.vault import VaultCredentials
from ..storage.argocd import ArgoCDStorage
from ..storage.config import ConfigStorage
from ..storage.helm import HelmStorage
from ..storage.kubernetes import KubernetesStorage
from ..storage.vault import VaultStorage

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
        VaultNotFoundError
            Raised if a necessary secret was not found in Vault.
        """
        environment = self._config.load_environment(environment_name)
        vault = self._vault_storage.get_vault_client(
            environment, credentials=vault_credentials
        )

        # Get information about the local repository.
        git_url = self._config.get_git_url()
        if not git_branch:
            git_branch = self._config.get_git_branch()

        # Get the plain-text Argo CD admin password from Vault.
        argocd_secret = vault.get_application_secret("argocd")
        argocd_password = argocd_secret.get("admin.plaintext_password")
        if not argocd_password:
            raise VaultNotFoundError(
                vault.url, f"{vault.path}/argocd", "admin.plaintext_password"
            )

        # Add the dependency repositories of the applications we're installing
        # directly with Helm, and refresh the Helm dependency cache.
        with action_group("Update Helm dependencies"):
            repo_urls = set()
            for app_name in ("vault-secrets-operator", "argocd"):
                app_urls = self._config.get_dependency_repositories(app_name)
                repo_urls.update(app_urls)
            for url in sorted(repo_urls):
                self._helm.repo_add(url)
            self._helm.repo_update()

        # Install vault-secrets-operator. Argo CD depends on this, so it has
        # to be installed and configured with its Vault secret first.
        with action_group("Install vault-secrets-operator"):
            self._kubernetes.create_namespace(
                "vault-secrets-operator", ignore_fail=True
            )
            self._kubernetes.create_generic_secret(
                "vault-credentials",
                "vault-secrets-operator",
                vault_credentials.to_secret_data(),
            )
            self._helm.dependency_update("vault-secrets-operator")
            self._helm.upgrade_application(
                "vault-secrets-operator",
                environment.name,
                {"vault-secrets-operator.vault.address": vault.url},
            )

        # Install Argo CD.
        with action_group("Install Argo CD"):
            self._helm.dependency_update("argocd")
            self._helm.upgrade_application(
                "argocd",
                environment.name,
                {"global.vaultSecretsPath": environment.vault_path_prefix},
            )

        # Create and sync the top-level Argo CD application.
        with action_group("Install science-platform app-of-apps"):
            self._argocd.login("admin", argocd_password.get_secret_value())
            self._argocd.create_environment(
                environment.name,
                "science-platform",
                git_url=git_url,
                git_branch=git_branch,
            )
            self._argocd.sync("science-platform")
            project = Project.infrastructure
            self._argocd.set_project("science-platform", project)

        # Sync Argo CD and wait for it to finish syncing so that the pods
        # don't restart in the middle of proxying another Argo CD operation.
        with action_group("Sync Argo CD"):
            try:
                self._argocd.sync("argocd")
            except CommandFailedError:
                # As of Argo CD 2.10.5, the first execution always fails with
                # a spurious error claiming the infrastructure project had not
                # been created.  This is transient; the second execution
                # succeeds.
                self._argocd.sync("argocd")
            for deployment in (
                "deployment/argocd-server",
                "deployment/argocd-repo-server",
                "statefulset/argocd-application-controller",
            ):
                self._kubernetes.wait_for_rollout(deployment, "argocd")

        # Sync applications that others have dependencies on, if they're
        # enabled.
        with action_group("Sync infrastructure applications"):
            for application in (
                "ingress-nginx",
                "cert-manager",
                "postgres",
                "gafaelfawr",
            ):
                if application in environment.applications:
                    self._argocd.sync(application)

        # Sync everything else.
        with action_group("Sync remaining applications"):
            self._argocd.sync_all(
                "science-platform", timeout=timedelta(minutes=5)
            )

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

    def template(self, environment: str) -> str:
        """Expand the templates of the top-level chart.

        Run :command:`helm template` for a top-level chart, passing in the
        appropriate parameters for the given environment.

        Parameters
        ----------
        environment
            Environment for which to expand the top-level chart.

        Returns
        -------
        str
            Output from :command:`helm template`.

        Raises
        ------
        CommandFailedError
            Raised if Helm fails.
        """
        return self._helm.template_environment(environment)
