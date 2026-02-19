"""Service to coordinate other services for cluster recovery."""

from google.api_core.exceptions import NotFound

from ..models.vault import VaultCredentials
from .cluster import GKEPhalanxClusterService
from .google_cloud import GoogleCloudService
from .recovery_environment import RecoveryEnvironmentService

__all__ = ["GKERecoveryService"]


class GKERecoveryService:
    """Service to coordinate other services for cluster recovery.

    Parameters
    ----------
    source_cluster
        The Google Cloud name of the old cluster.
    destination_cluster
        The Google Cloud name of the new cluster.
    environment
        The name of the Phalanx environment to load config from.
    git_branch
        The name of the Git branch to sync from in ArgoCD.
    google_cloud_service
        Performs operations on Google Cloud resources.
    old_cluster_service
        Performs kubectl operations against the old cluster.
    new_cluster_service
        Performs kubectl operations against the new cluster.
    recovery_environment_service
        Performs ArgoCD and Helm operations (and some kubectl operations)
        against the new cluster.
    source_environment_service
        Performs ArgoCD operations against the source cluster.
    vault_credentials
        Credentials to read from the Vault instance that backs the cluster
        environment.
    """

    def __init__(
        self,
        *,
        source_cluster: str,
        destination_cluster: str,
        environment: str,
        git_branch: str,
        google_cloud_service: GoogleCloudService,
        new_cluster_service: GKEPhalanxClusterService,
        old_cluster_service: GKEPhalanxClusterService,
        recovery_environment_service: RecoveryEnvironmentService,
        source_environment_service: RecoveryEnvironmentService,
        vault_credentials: VaultCredentials,
    ) -> None:
        self._source_cluster = source_cluster
        self._destination_cluster = destination_cluster
        self._environment_name = environment
        self._git_branch = git_branch
        self._google_cloud = google_cloud_service
        self._new_cluster = new_cluster_service
        self._old_cluster = old_cluster_service
        self._environment = recovery_environment_service
        self._source_environment = source_environment_service
        self._vault_credentials = vault_credentials

    def recover(self) -> None:
        self._google_cloud.backup_and_restore_pvcs(
            source_cluster=self._source_cluster,
            destination_cluster=self._destination_cluster,
        )
        self._new_cluster.retain_pvs()

        self._old_cluster.scale_down_all()

        self._environment.start_recover(
            self._environment_name,
            self._vault_credentials,
            self._git_branch,
        )

    def preflight_check(self) -> list[str]:
        """Check that everything is in a good state to start recovery."""
        errors: list[str] = [
            *self._check_kubectl_connect(),
            *self._check_static_ips(),
            *self._check_firewall_rules(),
            *self._check_source_synced(),
        ]
        return errors

    def _check_kubectl_connect(self) -> list[str]:
        """Check that kubectl can connect to clusters."""
        errors: list[str] = []

        try:
            self._old_cluster.kube_version()
            print(
                f"Source cluster with context: {self._old_cluster.context}"
                f" reachable with kubectl."
            )
        except Exception:
            errors.append(
                f"Could not connect to source cluster with kubectl using"
                f" context: {self._old_cluster.context}. If this cluster"
                f" exists, you may need to update your kubeconfig file with"
                f" credentials with `gcloud container clusters"
                f" get-credentials`."
            )

        try:
            self._new_cluster.kube_version()
            print(
                f"Destination cluster with context:"
                f" {self._new_cluster.context} reachable with kubectl."
            )
        except Exception:
            errors.append(
                f"Could not connect to destination cluster with kubectl using"
                f" context: {self._new_cluster.context}. If this cluster"
                f" exists, you may need to update your kubeconfig file with"
                f" credentials with `gcloud container clusters"
                f" get-credentials`."
            )
        return errors

    def _check_static_ips(self) -> list[str]:
        """Check that any source loadBalancerIP is static in Google Cloud.

        Ignore anything in the rubin-rag namespace. There is no way to declare
        static IPs for the Weviate LoadBalancer services with the Weviate helm
        chart, and we probably don't want those services public anyway. For
        now, it's fine if those public IPs change.
        """
        errors: list[str] = []
        services = self._old_cluster.get_phalanx_load_balancer_services()
        _addresses = self._google_cloud.list_static_ip_addresses()
        addresses = [address.address for address in _addresses]

        for service in services:
            if service.namespace == "rubin-rag":
                print(
                    f"Ignoring LoadBalancer Service "
                    f" {service.namespace}/{service.name} in source cluster"
                    f" with context: {self._old_cluster.context} and current"
                    f" external IP {service.status_load_balancer_ip} because"
                    f" we don't care if rubin-rag public IPs change, and there"
                    f" is no easy way to declare loadBalancerIPs on the"
                    f" services."
                )
                continue
            if not service.load_balancer_ip:
                errors.append(
                    f"LoadBalancer Service: {service.namespace}/{service.name}"
                    f" in source cluster with context:"
                    f" {self._old_cluster.context} does not declare a"
                    f" loadBalancerIP."
                )
            elif str(service.load_balancer_ip) not in addresses:
                errors.append(
                    f"LoadBalancer Service: {service.namespace}/{service.name}"
                    f" in source cluster with context: "
                    f" {self._old_cluster.context} declares loadBalancerIP:"
                    f" {service.load_balancer_ip!s}, but that IP is not static"
                    f" in Google Cloud."
                )
            else:
                print(
                    f"LoadBalancer Service {service.namespace}/{service.name}"
                    f" in source cluster with context:"
                    f" {self._old_cluster.context} declares loadBalancerIP:"
                    f"{service.load_balancer_ip!s}, and that IP is static in"
                    f" Google Cloud."
                )
        return errors

    def _check_firewall_rules(self) -> list[str]:
        """Check that the appropriate Google Cloud firewall rules exist."""
        errors: list[str] = []
        try:
            rule = self._google_cloud.get_cert_manager_firewall_rule()
        except NotFound:
            errors.append("Terraform firewall rule not found.")
            return errors

        try:
            source_cluster = self._google_cloud.get_cluster(
                self._source_cluster
            )
            source_cidr_block = (
                source_cluster.private_cluster_config.master_ipv4_cidr_block
            )
            if source_cidr_block not in rule.source_ranges:
                errors.append(
                    f"Source cluster: {self._source_cluster} master IPv4 CIDR"
                    f" block: {source_cidr_block} not in firewall rule:"
                    f" {rule.name} source ranges: {rule.source_ranges}"
                )
            source_tag = f"gke-{self._source_cluster}"
            if source_tag not in rule.target_tags:
                errors.append(
                    f"Source cluster: {self._source_cluster} target tag"
                    f" {source_tag} not in firewall rule: {rule.name} target"
                    f" tags: {rule.target_tags}"
                )
        except NotFound:
            msg = f"Source GKE cluster: {self._source_cluster} not found."
            errors.append(msg)

        try:
            destination_cluster = self._google_cloud.get_cluster(
                self._destination_cluster
            )

            private_config = destination_cluster.private_cluster_config
            destination_cidr_block = private_config.master_ipv4_cidr_block
            if destination_cidr_block not in rule.source_ranges:
                errors.append(
                    f"Destination cluster: {self._destination_cluster} master"
                    f" IPv4 CIDR block: {destination_cidr_block} not in"
                    f" firewall rule: {rule.name} source ranges: "
                    f" {rule.source_ranges}"
                )
            destination_tag = f"gke-{self._destination_cluster}"
            if destination_tag not in rule.target_tags:
                errors.append(
                    f"Destination cluster: {self._destination_cluster} target"
                    f" tag {destination_tag} not in firewall rule: {rule.name}"
                    f" target tags: {rule.target_tags}"
                )
        except NotFound:
            errors.append(
                f"Destination GKE cluster: {self._destination_cluster} not"
                f" found."
            )

        return errors

    def _check_source_synced(self) -> list[str]:
        """Make sure all ArgoCD apps in source cluster are in sync."""
        errors: list[str] = []
        apps = self._source_environment.list_argocd_apps_except_nublado_users(
            environment_name=self._environment_name,
            vault_credentials=self._vault_credentials,
        )
        wrong_refs = apps.get_different_ref(self._git_branch)
        for app in wrong_refs:
            ref = app.spec.source.target_revision
            msg = (
                f"{app.metadata.name} is not configured to sync to:"
                f" {self._git_branch} in ArgoCD in source cluster with"
                f" context: {self._old_cluster.context}. It is configured to"
                f" sync to {ref}."
            )
            errors.append(msg)

        unsynced = apps.get_unsynced()
        for app in unsynced:
            if app in wrong_refs:
                continue
            msg = (
                f"{app.metadata.name} is unsynced in ArgoCD in source cluster"
                f" with context: {self._old_cluster.context}"
            )
            errors.append(msg)
        return errors
