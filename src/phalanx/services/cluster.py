"""Service for manipulating Phalanx Kubernetes clusters directly."""

import traceback

from ..constants import (
    GKE_LOAD_BALANCER_SERVICE_FINALIZERS,
    PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION,
    PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
    PREVIOUS_REPLICA_COUNT_ANNOTATION,
    SASQUATCH_NAMESPACE,
)
from ..exceptions import (
    InvalidLoadBalancerServiceStateError,
    InvalidScaleStateError,
    ServiceMissingTrafficPolicyError,
)
from ..models.kubernetes import NamespacedResource, Service, Workload
from ..storage.kubernetes import KubernetesStorage

__all__ = ["GKEPhalanxClusterService"]


_SASQUATCH_KAFKA = NamespacedResource(
    kind="Kafka", namespace=SASQUATCH_NAMESPACE, name="sasquatch"
)
"""The Sasquatch Kafka resource."""


class GKEPhalanxClusterService:
    """Kubernetes operations on a GKE Phalanx cluster.

    These operations are not in the EnviromentService because:

    * They do not necessarily correspond 1-1 to a Phalanx enviroment.
    * They are often part of tasks that involve multiple clusters, so passing
      an explicit context is less error prone, and allows the operations to be
      automated without having to manually change the kubectl current context.
    * Some of the operations are specific to Google Cloud GKE clusters, like
      waiting for an associated cloud load balancer to be destroyed when
      converting a Service from LoadBalancer to ClusterIP.

    For example, when recovering a GCP cluster from backups while the old
    cluster still exists, you will need to work with two clusters, both of
    which are associated with the same environment.

    Parameters
    ----------
    kubernetes_storage
        Interface to direct Kubernetes object manipulation.
    """

    def __init__(self, kubernetes_storage: KubernetesStorage) -> None:
        self._kubernetes = kubernetes_storage
        self.context = self._kubernetes.context

    def suspend_cronjobs(self) -> None:
        """Suspend all CronJobs in all Phalanx apps."""
        cronjobs = self._kubernetes.get_phalanx_cronjobs()
        return self._kubernetes.suspend_cronjobs(cronjobs)

    def resume_cronjobs(self) -> None:
        """Resume all CronJobs in all Phalanx apps."""
        cronjobs = self._kubernetes.get_phalanx_cronjobs()
        return self._kubernetes.resume_cronjobs(cronjobs)

    def scale_down_workloads(self) -> None:
        """Scale down (almost) all Phalanx workloads.

        During cluster rebuilds when there is an old and a new cluster, certain
        workloads can't be running in both clusters at the same time, or else
        state external to the cluster could be corrupted.

        We'll leave ArgoCD running so the scaled-down cluster can still be
        inspected.

        Raises
        ------
        InvalidScaleStateError
            If the workload resource has a previous replica count annotation,
            but its current replica count is not zero.
        """
        workloads = self._get_workloads_except_argocd()
        sasquatch_workloads = [
            workload
            for workload in workloads
            if workload.namespace == SASQUATCH_NAMESPACE
        ]

        for workload in sasquatch_workloads:
            workloads.remove(workload)

        # Scale down other workloads before sasquatch so we don't get errors
        # about metrics.
        for workload in workloads:
            try:
                self._check_workload_state(workload)
            except Exception:
                traceback.print_exc()
                continue

            self._kubernetes.annotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
                value=str(workload.replicas),
            )
            self._kubernetes.scale(workload, 0)

        for workload in sasquatch_workloads:
            try:
                self._check_workload_state(workload)
            except Exception:
                traceback.print_exc()
                continue

            self._kubernetes.annotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
                value=str(workload.replicas),
            )
            self._kubernetes.scale(workload, 0)

        for workload in sasquatch_workloads:
            self._kubernetes.wait_for_rollout(
                namespace=workload.namespace, name=workload.get_kind_name()
            )

    def scale_up_workloads(self) -> None:
        """Scale up (almost) all Phalanx workloads to their previous counts.

        This is only intended to be run after a scale down operation.

        Raises
        ------
        InvalidScaleStateError
            If the workload resource has a previous replica count annotation,
            but its current replica count is not zero.

        """
        # Scale up all sasquatch workloads so we don't have apps starting
        # without metrics
        workloads = self._get_workloads_except_argocd()
        sasquatch_workloads = [
            workload
            for workload in workloads
            if workload.namespace == SASQUATCH_NAMESPACE
        ]

        for workload in sasquatch_workloads:
            workloads.remove(workload)

        for workload in sasquatch_workloads:
            self._check_workload_state(workload)
            if workload.previous_replica_count is None:
                continue
            self._kubernetes.scale(workload, workload.previous_replica_count)
            self._kubernetes.deannotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
            )

        # Scale up all of the other workloads
        for workload in workloads:
            try:
                self._check_workload_state(workload)
            except Exception:
                traceback.print_exc()
                continue

            if workload.previous_replica_count is None:
                continue
            self._kubernetes.scale(workload, workload.previous_replica_count)
            self._kubernetes.deannotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
            )

    def scale_up_all(self) -> None:
        """Scale up all Phalanx workloads and resume all crons."""
        self._kubernetes.resume_sasquatch_kafka_reconciliation()
        self.restore_service_ips()
        self.scale_up_workloads()
        self.resume_cronjobs()

    def scale_down_all(self) -> None:
        """Scale down all Phalanx workloads except ArgoCD and crons."""
        self._kubernetes.pause_sasquatch_kafka_reconciliation()
        self.release_service_ips()
        self.suspend_cronjobs()
        self.scale_down_workloads()

    def get_phalanx_load_balancer_services(self) -> list[Service]:
        """Get all Services of type LoadBalancer for all Phalanx apps.

        We say a Service is in a Phalanx app if it has an ArgoCD label.

        Returns
        -------
        list[Service]
            A list of all of the LoadBalancer Services provisioned by Phalanx
            apps.
        """
        return self._kubernetes.get_phalanx_load_balancer_services()

    def release_service_ips(self) -> list[Service]:
        """Release all IPs on LoadBalancer Services for all Phalanx apps.

        This will clear any spec.loadBalancerIPs, then change the Service type
        from LoadBalancer to ClusterIP, then back to LoadBalancer.

        This can be used when recovering a Phalanx cluster to another GKE
        cluster while the old cluster is still running.

        Returns
        -------
        list[Service]
            A list of Services with refreshed IPs.

        Raises
        ------
        InvalidLoadBalancerServiceStateError
            If the service resource does not have exactly one of
            spec.loadBalancerIP or an annotation for the previous
            loadBalancerIP set.

        ServiceMissingTrafficPolicyError
            If the service resource does not have an externalTrafficPolicy.
        """
        new_services = []
        services = self._kubernetes.get_phalanx_load_balancer_services()
        for service in services:
            self._check_service_state(service)
            if not service.external_traffic_policy:
                continue
            self._kubernetes.annotate(
                service,
                key=PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
                value=str(service.load_balancer_ip),
            )
            self._kubernetes.annotate(
                service,
                key=PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION,
                value=service.external_traffic_policy.value,
            )
            self._kubernetes.remove_service_load_balancer_ip(service)
            self._refresh_service_ingress(service)
            self._kubernetes.update_service_external_traffic_policy(
                service, service.external_traffic_policy
            )
            new_service = self._kubernetes.get_service(
                name=service.name, namespace=service.namespace
            )
            new_services.append(new_service)

        return new_services

    def restore_service_ips(self) -> list[Service]:
        """Restore all IPs on LoadBalancer Services for all Phalanx apps.

        This is only intended to be run after a release operation because it
        depends on an annotation set during that operation.

        Raises
        ------
        InvalidLoadBalancerServiceStateError
            If the service resource does not have exactly one of
            spec.loadBalancerIP or an annotation for the previous
            loadBalancerIP set.

        """
        new_services = []
        services = self._kubernetes.get_phalanx_load_balancer_services()
        for service in services:
            if (
                not service.previous_loadbalancer_ip
                or not service.previous_external_traffic_policy
            ):
                continue
            try:
                self._check_service_state(service)
            except Exception:
                traceback.print_exc()
                continue
            self._kubernetes.add_service_load_balancer_ip(
                service, service.previous_loadbalancer_ip
            )
            self._kubernetes.deannotate(
                service,
                key=PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
            )
            self._kubernetes.deannotate(
                service,
                key=PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION,
            )
            self._refresh_service_ingress(service)
            self._kubernetes.update_service_external_traffic_policy(
                service, service.previous_external_traffic_policy
            )
            new_service = self._kubernetes.get_service(
                name=service.name, namespace=service.namespace
            )
            new_services.append(new_service)

        return new_services

    def retain_pvs(self) -> None:
        """Set the persistentVolumeReclaimPolicy to Retain for all PVs."""
        self._kubernetes.retain_pvs()

    def _refresh_service_ingress(self, service: Service) -> None:
        """Destroy and recreate the ingress associated with a Service."""
        self._kubernetes.set_service_to_cluster_ip(service)
        self._kubernetes.wait_for_resource_no_finalizers(
            service, GKE_LOAD_BALANCER_SERVICE_FINALIZERS
        )
        self._kubernetes.set_service_to_load_balancer(service)
        self._kubernetes.wait_for_service_ingress(service)

    def _check_service_state(self, service: Service) -> None:
        """Ensure a LoadBalancer Service is not in an incorrect state."""
        exactly_one = (
            service.load_balancer_ip,
            service.previous_loadbalancer_ip,
        )
        if all(exactly_one) or not any(exactly_one):
            raise InvalidLoadBalancerServiceStateError(service)

        if not service.external_traffic_policy:
            raise ServiceMissingTrafficPolicyError(service)

    def _get_workloads_except_argocd(self) -> list[Workload]:
        """Get all Phalanx workloads in the cluster except ArgoCD workloads.

        Returns
        -------
        list[Workload]
            A list of Phalanx workloads execpt for ArgoCD workloads.
        """
        deployments = self._kubernetes.get_phalanx_deployments()
        statefulsets = self._kubernetes.get_phalanx_stateful_sets()

        return [
            workload
            for workload in deployments + statefulsets
            if workload.namespace != "argocd"
        ]

    def _check_workload_state(self, workload: Workload) -> None:
        """Make sure the workload is in an OK state to be scaled.

        Parameters
        ----------
        workload
          The workload to check the state of.

        """
        if workload.previous_replica_count:
            if workload.replicas != 0:
                raise InvalidScaleStateError(workload)

    def kube_version(self) -> None:
        """Print the version of the kubectl client and kubernetes server.

        Useful for checking that kubectl can connect to a cluster using a given
        context.
        """
        self._kubernetes.version()
