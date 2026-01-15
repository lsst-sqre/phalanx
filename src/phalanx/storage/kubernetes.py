"""Storage layer for direct Kubernetes operations."""

import time
from ipaddress import IPv4Address
from math import ceil

from phalanx.exceptions import ResourceNoFinalizersTimeoutError

from ..models.kubernetes import (
    CronJob,
    Deployment,
    NamespacedResource,
    ResourceList,
    Service,
    ServiceIPPatch,
    ServiceIPSpecPatch,
    StatefulSet,
    Workload,
)
from ..models.vault import VaultCredentials
from .command import Command

__all__ = ["KubernetesStorage"]


class KubernetesStorage:
    """Storage layer for direct Kubernetes operations.

    Used primarily by the installer. This uses :command:`kubectl` directly
    rather than one of the Python Kubernetes libraries since it seemed simpler
    at the time.

    Parameters
    ----------
    context
        The kubectl context to specify for all kubectl commands. If this is
        None, then the current context will be used.
    """

    def __init__(self, context: str | None = None) -> None:
        common_args = ["--context", context] if context else []
        self._kubectl = Command("kubectl", common_args=common_args)

    def create_namespace(
        self, namespace: str, *, ignore_fail: bool = False
    ) -> None:
        """Create a Kubernetes namespace.

        Parameters
        ----------
        namespace
            Namespace to create.
        ignore_fail
            If `True`, ignore failures, such as when the namespace already
            exists.

        Raises
        ------
        CommandFailedError
            Raised if the namespace creation fails, and ``ignore_fail`` was
            not set to `True`.
        """
        self._kubectl.run("create", "ns", namespace, ignore_fail=ignore_fail)

    def create_vault_secret(
        self, name: str, namespace: str, credentials: VaultCredentials
    ) -> None:
        """Create a Kubernetes ``Secret`` resource for Vault credentials.

        Parameters
        ----------
        name
            Name of the secret.
        namespace
            Namespace of the secret.
        credentials
            Vault credentials to store in the secret.
        """
        args = ["apply", "-f", "-"]
        self._kubectl.run(*args, stdin=credentials.to_kubernetes_secret(name))

    def get_current_context(self) -> str:
        """Get the current context (the default Kubernetes cluster).

        Returns
        -------
        str
            Name of the current Kubernetes context.
        """
        result = self._kubectl.capture("config", "current-context")
        return result.stdout.strip()

    def wait_for_rollout(self, name: str, namespace: str) -> None:
        """Wait for a Kubernetes rollout to complete.

        Parameters
        ----------
        name
            Name of the rollout. This should be the type of object (usually
            either ``deployment`` or ``statefulset``, followed by a slash and
            the name of the object.
        namespace
            Namespace in which the rollout is happening.
        """
        self._kubectl.run("-n", namespace, "rollout", "status", name)

    def restart(self, name: str, namespace: str) -> None:
        """Restart a kubernetes workload and wait for it to be ready again.

        Parameters
        ----------
        name
            Name of the workload. This should be the type of object (usually
            either ``deployment`` or ``statefulset``, followed by a slash and
            the name of the object.
        namespace
            Namespace in which the workload exists.
        """
        self._kubectl.run("-n", namespace, "rollout", "restart", name)
        self.wait_for_rollout(name=name, namespace=namespace)

    def get_phalanx_cronjobs(self) -> list[CronJob]:
        """Get the names of all CronJobs in all Phalanx apps.

        We say a CronJob is in a Phalanx app if it has an ArgoCD label.

        Returns
        -------
        list[CronJob]
            A list of all of the CronJobs provisioned by Phalanx apps.
        """
        raw = self._kubectl.capture(
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )
        cronjobs = ResourceList[CronJob].model_validate_json(raw.stdout)
        return cronjobs.items

    def get_phalanx_deployments(self) -> list[Deployment]:
        """Get the names of all Deployments in all Phalanx apps.

        We say a Deployment is in a Phalanx app if it has an ArgoCD label.

        Returns
        -------
        list[Deployment]
            A list of all of the Deployments provisioned by Phalanx apps.
        """
        raw = self._kubectl.capture(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )
        deployments = ResourceList[Deployment].model_validate_json(raw.stdout)
        return deployments.items

    def get_phalanx_stateful_sets(self) -> list[StatefulSet]:
        """Get the names of all StatefulSets in all Phalanx apps.

        We say a StatefulSet is in a Phalanx app if it has an ArgoCD label.

        Returns
        -------
        list[StatefulSet]
            A list of all of the StatefulSets provisioned by Phalanx apps.
        """
        raw = self._kubectl.capture(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )
        statefulsets = ResourceList[StatefulSet].model_validate_json(
            raw.stdout
        )
        return statefulsets.items

    def suspend_cronjobs(self, cronjobs: list[CronJob]) -> None:
        """Suspend all given cronjobs.

        Parameters
        ----------
        cronjobs
            A list of CronJobs to suspend.
        """
        patch = '{"spec" : {"suspend" : true }}'

        for job in cronjobs:
            self._kubectl.run(
                "patch",
                "CronJob",
                job.name,
                "--namespace",
                job.namespace,
                "--patch",
                patch,
            )

    def resume_cronjobs(self, cronjobs: list[CronJob]) -> None:
        """Resume all given cronjobs.

        Parameters
        ----------
        cronjobs
            A list of CronJobs to resume.
        """
        patch = '{"spec" : {"suspend" : false }}'

        for job in cronjobs:
            self._kubectl.run(
                "patch",
                "CronJob",
                job.name,
                "--namespace",
                job.namespace,
                "--patch",
                patch,
            )

    def annotate(
        self,
        resource: NamespacedResource,
        key: str,
        value: str,
        *,
        overwrite: bool = False,
    ) -> None:
        """Add an annotation to a namespaced resource.

        Parameters
        ----------
        resource
            The Kubernetes resource to annotate.
        key
            The name of the annotation.
        value
            The value of the annotation.
        overwrite
            Whether or not to overwrite the annotation if it already exists.
        """
        args = [
            "annotate",
            resource.kind,
            resource.name,
            f"{key}={value}",
            "--namespace",
            resource.namespace,
        ]

        if overwrite:
            args.append("--overwrite")

        self._kubectl.run(*args)

    def deannotate(self, resource: NamespacedResource, key: str) -> None:
        """Remove an annotation from a namespaced resource.

        Parameters
        ----------
        resource
            The Kubernetes resource from which to remove the annotation.
        key
            The name of the annotation.
        """
        self._kubectl.run(
            "annotate",
            resource.kind,
            resource.name,
            f"{key}-",
            "--namespace",
            resource.namespace,
        )

    def scale(self, workload: Workload, replicas: int) -> None:
        """Scale the replica count of a workload.

        Parameters
        ----------
        workload
            The Kubernetes workload to scale.
        replicas
            The desired replica count.
        """
        resource = workload.get_kind_name()

        self._kubectl.run(
            "scale",
            resource,
            "--replicas",
            str(replicas),
            "--namespace",
            workload.namespace,
        )

    def get_phalanx_load_balancer_services(self) -> list[Service]:
        """Get all Services of type LoadBalancer for all Phalanx apps.

        We say a Service is in a Phalanx app if it has an ArgoCD label.

        Returns
        -------
        list[Service]
            A list of all of the LoadBalancer Services provisioned by Phalanx
            apps.
        """
        raw = self._kubectl.capture(
            "get",
            "Service",
            "--field-selector",
            "spec.type=LoadBalancer",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )
        return ResourceList[Service].model_validate_json(raw.stdout).items

    def get_service(self, name: str, namespace: str) -> Service:
        """Get a Service by namespace and name.

        Returns
        -------
        Service
            A Service.
        """
        raw = self._kubectl.capture(
            "get",
            "Service",
            name,
            "--namespace",
            namespace,
            "-o",
            "json",
        )
        return Service.model_validate_json(raw.stdout)

    def get_resource(
        self, kind: str, name: str, namespace: str
    ) -> NamespacedResource:
        """Get a resource by namespace and name.

        Returns
        -------
        NamespacedResource
            A namespaced resource.
        """
        raw = self._kubectl.capture(
            "get",
            kind,
            name,
            "--namespace",
            namespace,
            "-o",
            "json",
        )
        return Service.model_validate_json(raw.stdout)

    def wait_for_service_ingress(self, service: Service) -> None:
        """Wait for a LoadBalancer Service to have an associated ingress.

        Parameters
        ----------
        service
            The service to wait for.
        """
        self._kubectl.run(
            "wait",
            "--for=jsonpath={.status.loadBalancer.ingress}",
            service.get_kind_name(),
            "--namespace",
            service.namespace,
            "--timeout",
            "5m",
        )

    def wait_for_resource_no_finalizers(
        self, resource: NamespacedResource, finalizers: list[str]
    ) -> None:
        """Wait for a resource to NOT have the given finalizers.

        This is useful for waiting for some controller to do some
        reconcilliation triggered by changing a resource.

        Parameters
        ----------
        resource
            The service to wait for.

        Raises
        ------
        ResourceNoFinalizersTimeoutError
            The associated finalizers are not removed after waiting.
        """
        timeout_seconds = 60 * 5  # 5 minutes
        wait_seconds = 5
        retries = ceil(timeout_seconds / wait_seconds)

        for _ in range(retries):
            resource = self.get_resource(
                kind=resource.kind,
                name=resource.name,
                namespace=resource.namespace,
            )
            if set(resource.finalizers).isdisjoint(set(finalizers)):
                return
            time.sleep(wait_seconds)

        raise ResourceNoFinalizersTimeoutError(
            resource, finalizers, timeout_seconds
        )

    def remove_service_load_balancer_ip(self, service: Service) -> None:
        """Remove the IP address associated with a LoadBalancerService.

        If the services is associated with a cloud load balancer with a static
        IP, and you want the IP to be released in the cloud, you also need to
        modify the type of the load balancer to be a ClusterIP.

        Parameters
        ----------
        service
            The LoadBalancer Service to remove the IP from.
        """
        patch = '{"spec" : {"loadBalancerIP" : null }}'

        self._kubectl.run(
            "patch",
            "Service",
            service.name,
            "--namespace",
            service.namespace,
            "--patch",
            patch,
        )

    def add_service_load_balancer_ip(
        self, service: Service, ip: IPv4Address
    ) -> None:
        """Assign an IP address associated with a LoadBalancerService.

        Parameters
        ----------
        service
            The LoadBalancer Service to assign the IP to.
        ip
            The IP address to set the spec.loadBalancerIP field to.
        """
        patch = ServiceIPPatch(spec=ServiceIPSpecPatch(load_balancer_ip=ip))

        self._kubectl.run(
            "patch",
            "Service",
            service.name,
            "--namespace",
            service.namespace,
            "--patch",
            patch.model_dump_json(by_alias=True),
        )

    def set_service_to_cluster_ip(self, service: Service) -> None:
        """Set the type of a Service to ClusterIP.

        Parameters
        ----------
        service
            The service to change.
        """
        self._kubectl.run(
            "patch",
            "Service",
            service.name,
            "--namespace",
            service.namespace,
            "--patch",
            '{"spec": {"type": "ClusterIP" } }',
        )

    def set_service_to_load_balancer(self, service: Service) -> None:
        """Set the type of a Service to LoadBalancer.

        Parameters
        ----------
        service
            The service to change.
        """
        self._kubectl.run(
            "patch",
            "Service",
            service.name,
            "--namespace",
            service.namespace,
            "--patch",
            '{"spec": {"type": "LoadBalancer" } }',
        )
