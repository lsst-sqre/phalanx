"""Service for manipulating Phalanx environments during cluster recovery.

This is very similar to installing an environment for the first time, but there
are differences in the order that specific resources and namespaces must be
installed.
"""

import time
from datetime import timedelta

from ..exceptions import ArgoCDStatusTimedOutError
from ..models.argocd import ApplicationList
from ..models.environments import Environment
from ..models.vault import VaultCredentials
from .environment import EnvironmentService

__all__ = ["RecoveryEnvironmentService"]


class RecoveryEnvironmentService(EnvironmentService):
    """Phalanx environment operations only for use during cluster recovery."""

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

        # Get the sasquatch Kafka cluster ID from the old cluster. We need to
        # force the new cluster Strimzi Kafka to have this same ID so that it
        # will match the data on the restored PVs.
        sasquatch_cluster_id = (
            self._kubernetes.get_sasquatch_kafka_cluster_id()
        )
        print(f"Sasquatch Kafka cluster id: {sasquatch_cluster_id}")

        # Get the plain-text Argo CD admin password from Vault and tell GitHub
        # Actions to mask it.
        argocd_password = self._get_argocd_password(vault)

        # Update Helm dependencies.
        self._update_helm_dependencies(["vault-secrets-operator", "argocd"])

        self._install_vault_secrets_operator(
            environment, vault_credentials, vault.url
        )
        self._install_argocd(environment)
        self._install_app_of_apps(environment, git_branch, argocd_password)
        self._sync_argocd()

        # Wait for every ArgoCD Application resource to list all of its
        # resources its status. We need this to sync individual kinds of
        # resources across all apps.
        self._wait_for_app_statuses(environment)

        # Some KafkaUsers require Secrets that are provisioned from
        # VaultSecrets
        self._sync_kind("VaultSecret", environment)

        # Patch the sasquatch ArgoCD application so that the Kafka resource
        # will have the pause annotation set when it is synced
        self._set_pause_sasquatch(environment_name, vault_credentials)

        if "sasquatch" in environment.applications:
            self._sync_strimzi(environment)

        # Sync Strimzi resources to avoid a race condition when creating the
        # Kafka Cluster that will delete topics and users
        self._sync_kind("KafkaUser", environment)
        self._sync_kind("KafkaTopic", environment)
        self._sync_kind("KafkaAccess", environment)
        self._sync_kind("Kafka", environment)
        self._kubernetes.set_sasquatch_cluster_id(sasquatch_cluster_id)

        # We need cert-manager to provision the cert any external endpoints
        # that the KafkaNodePool provisions
        self._sync_cert_manager(environment)

        self._sync_kind("Certificate", environment)
        self._sync_kind("KafkaNodePool", environment)

        # Remove the patch we did to the sasquatch ArgoCD Application that adds
        # the pause annotation to the Kafka resource
        self._unset_pause_sasquatch()

        # :fingers-crossed:
        self._kubernetes.resume_sasquatch_kafka_reconciliation()

        breakpoint()
        # At this point, we should have a running Kafka

        self._sync_infrastructure_applications(environment)

        # We need grafana because the sasquatch app may include a Grafana
        # DataSource when syncing InfluxDB
        self._sync_grafana(environment)

        # Sync all of the other stuff in the sasquatch mega-app, like the
        # schema manager, so that apps can send metrics
        self._sync_sasquatch(environment)

        breakpoint()

        # Some of the helm pre-install hooks run jobs that require other
        # resources to exist.
        self._sync_kind("ServiceAccount", environment)
        self._sync_kind("ConfigMap", environment)
        self._sync_repertoire(environment)

        # Restart gafaelfawr now that it can send metrics, now have a working
        # Kafka and schema manager
        self._restart_gafaelfawr()

        self._sync_remaining_applications(environment)

    def list_argocd_apps_except_nublado_users(
        self,
        environment_name: str,
        vault_credentials: VaultCredentials,
    ) -> ApplicationList:
        """List any ArgoCD applications except nublado-users.

        We don't care about nublado-users because ArgoCD doesn't provision any
        resources in it, and most functionality that uses this method expect
        there to be resources in the app.
        """
        environment = self._config.load_environment(environment_name)
        app_of_apps = environment.app_of_apps_name
        if not app_of_apps:
            raise ValueError(f"appOfAppsName not set for {environment.name}")
        vault = self._vault_storage.get_vault_client(
            environment, credentials=vault_credentials
        )
        argocd_password = self._get_argocd_password(vault)
        self._argocd.login("admin", argocd_password)
        return self._argocd.list_applications_except_nublado_users(app_of_apps)

    def _sync_cert_manager(self, environment: Environment) -> None:
        """Sync cert-manager.

        When recovering a cluster, we may need cert-manager before we need the
        rest of the infrastructure applications.

        Parameters
        ----------
        environment
            The environment configuration object.
        """
        for application in ("cert-manager",):
            if application in environment.applications:
                self._argocd.sync(application)

    def _sync_repertoire(self, environment: Environment) -> None:
        """Sync Repertoire.

        These should be synced before most other apps so that apps that they
        can get service discovery information.

        Parameters
        ----------
        environment
            The environment configuration object.
        """
        if "repertoire" in environment.applications:
            self._argocd.sync("repertoire")

    def _set_pause_sasquatch(
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

    def _unset_pause_sasquatch(self) -> None:
        """Unset the helm value in sasquatch to pause Kafka reconciliation.

        Why not just use kubectl to modify the annotation directly on the
        Kafka resource? Because during the recovery process, we need to
        sync sasquatch for the first time with reconciliation paused.
        """
        self._argocd.unset_helm_value(
            application="sasquatch",
            key="strimzi-kafka.kafka.pauseReconciliation",
        )

    def _wait_for_app_statuses(
        self,
        environment: Environment,
        interval: timedelta = timedelta(seconds=5),
        attempts: int = 120,
    ) -> ApplicationList:
        """Wait for the statuses of all apps to be set.

        When the app-of-apps is installed, it takes a while for the status of
        all of the app's resources to appear in the Kubernetes resources. We
        need these statuses because we need to sync specific kinds of resources
        across all apps, and we need to find which apps have the resources by
        using the status.
        """
        app_of_apps = environment.app_of_apps_name
        if not app_of_apps:
            raise ValueError(f"appOfAppsName not set for {environment.name}")

        for _ in range(attempts):
            try:
                return self._argocd.list_applications_except_nublado_users(
                    app_of_apps
                )
            except ValueError:
                seconds = int(interval.total_seconds())
                print(
                    f"Argo CD app statuses not ready, trying again in"
                    f" {seconds} seconds"
                )
                time.sleep(interval.total_seconds())
                continue
        raise ArgoCDStatusTimedOutError(attempts, interval)

    def _sync_kind(self, kind: str, environment: Environment) -> None:
        """Sync all resources of a given kind for all apps."""
        app_of_apps = environment.app_of_apps_name
        if not app_of_apps:
            raise ValueError(f"appOfAppsName not set for {environment.name}")
        all_apps = self._argocd.list_applications_except_nublado_users(
            app_of_apps
        )
        apps = all_apps.with_resource(kind)
        for app in apps:
            self._argocd.sync(app.metadata.name, kind=kind)
