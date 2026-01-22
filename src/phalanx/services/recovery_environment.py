"""Service for manipulating Phalanx environments during cluster recovery.

This is very similar to installing an environment for the first time, but there
are differences in the order that specific resources and namespaces must be
installed.
"""

from ..models.environments import Environment
from ..models.vault import VaultCredentials
from .environment import EnvironmentService

__all__ = ["RecoveryEnvironmentService"]


class RecoveryEnvironmentService(EnvironmentService):
    """Phalanx environment operations only for use during cluster recovery."""

    def set_pause_sasquatch(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
    ) -> None:
        """Set a helm value in the sasquatch app to pause Kafka reconciliation.

        Why not just use kubectl to modify the annotation directly on the
        Kafka resource? Because during the recovery process, we need to
        sync sasquatch for the first time with reconciliation paused.
        """
        self._argocd_login(environment_name, vault_credentials)
        self._argocd.set_helm_value(
            application="sasquatch",
            key="strimzi-kafka.kafka.pauseReconciliation",
            value="true",
        )

    def unset_pause_sasquatch(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
    ) -> None:
        """Unset the helm value in sasquatch to pause Kafka reconciliation.

        Why not just use kubectl to modify the annotation directly on the
        Kafka resource? Because during the recovery process, we need to
        sync sasquatch for the first time with reconciliation paused.
        """
        self._argocd_login(environment_name, vault_credentials)
        self._argocd.unset_helm_value(
            application="sasquatch",
            key="strimzi-kafka.kafka.pauseReconciliation",
        )

    def start_recover(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
        git_branch: str | None = None,
    ) -> None:
        """Recover a Phalanx environment to another cluster with existing PVs.

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
        self.set_pause_sasquatch(environment_name, vault_credentials)
        self._sync_argocd()
        if "sasquatch" in environment.applications:
            self._sync_strimzi(environment)

        # Sync Strimzi resources to avoid a race condition when creating the
        # Kafka Cluster that will delete topics and users
        self._sync_all_kinds("VaultSecret", environment)
        self._sync_all_kinds("KafkaUser", environment)
        self._sync_all_kinds("KafkaTopic", environment)
        self._sync_all_kinds("KafkaAccess", environment)
        self._sync_infrastructure_applications(environment)
        if "sasquatch" in environment.applications:
            self._sync_sasquatch(environment)

    def finish_recover(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
        git_branch: str | None = None,
    ) -> None:
        """Recover a Phalanx environment to another cluster with existing PVs.

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
        self._argocd.login("admin", argocd_password)

        # Some of the helm pre-install hooks run jobs that require other
        # resources to exist.
        self._sync_all_kinds("ServiceAccount", environment)
        self._sync_all_kinds("ConfigMap", environment)
        self._restart_gafaelfawr()
        self._sync_remaining_applications(environment)

    def _sync_all_kinds(self, kind: str, environment: Environment) -> None:
        """Sync all resources of a given kind for all apps."""
        app_of_apps = environment.app_of_apps_name
        if not app_of_apps:
            raise ValueError(f"appOfAppsName not set for {environment.name}")
        all_apps = self._argocd.list_applications(app_of_apps)
        apps = all_apps.with_resource(kind)
        for app in apps:
            self._argocd.sync(app.metadata.name, kind=kind)
