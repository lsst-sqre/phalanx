"""Models representing Kubernetes resources."""

from enum import Enum
from ipaddress import IPv4Address
from typing import Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from ..constants import (
    PREVIOUS_LOAD_BALANCER_IP_ANNOTATION,
    PREVIOUS_REPLICA_COUNT_ANNOTATION,
)

__all__ = [
    "CronJob",
    "Deployment",
    "NamespacedResource",
    "ResourceList",
    "Service",
    "ServiceIPPatch",
    "ServiceIPSpecPatch",
    "ServiceType",
    "ServiceTypePatch",
    "ServiceTypeSpecPatch",
    "StatefulSet",
    "Workload",
]


class ServiceType(Enum):
    """Valid values for the spec.type field of a Service."""

    CLUSTER_IP = "ClusterIP"
    """ClusterIP Service type."""

    LOAD_BALANCER = "LoadBalancer"
    """LoadBalacner Service type."""


class NamespacedResource(BaseModel):
    """Properties common to a namespaced Kubernetes resource."""

    model_config = ConfigDict(validate_by_name=True)

    kind: str
    """The kind of Kubernetes resource."""

    namespace: str = Field(validation_alias=AliasPath("metadata", "namespace"))
    """The namespace the resource is in."""

    name: str = Field(validation_alias=AliasPath("metadata", "name"))
    """The name of the resource."""

    finalizers: list[str] = Field(
        default=[], validation_alias=AliasPath("metadata", "finalizers")
    )
    """Finalizers on this resource."""

    def get_kind_name(self) -> str:
        """Get the kind-qualified name of this resource.

        Returns
        -------
        str
            The kind-qualified name of this resource.
        """
        return f"{self.kind}/{self.name}"


class ResourceList[T: NamespacedResource](BaseModel):
    """A list of resources returned from a kubectl command."""

    items: list[T]
    """A list of Kubernetes resources."""

    kind: Literal["List"]
    """The kind field will always be List."""


class CronJob(NamespacedResource):
    """A CronJob kubernetes resource."""

    kind: Literal["CronJob"]
    """The kind field will always be CronJob."""


class Workload(NamespacedResource):
    """A Kubernetes resource that can be scaled up and down."""

    replicas: int = Field(
        validation_alias=AliasPath("spec", "replicas"),
    )
    previous_replica_count: int | None = Field(
        default=None,
        validation_alias=AliasPath(
            "metadata", "annotations", PREVIOUS_REPLICA_COUNT_ANNOTATION
        ),
    )
    """The original number of replicas if we explicitly scaled down."""


class Deployment(Workload):
    """A Deployment kubernetes resource."""

    kind: Literal["Deployment"]
    """The kind field will always be Deployment."""


class StatefulSet(Workload):
    """A StatefulSet kubernetes resource."""

    kind: Literal["StatefulSet"]
    """The kind field will always be StatefulSet."""

    pervious_replica_count: int | None = Field(
        default=None,
        validation_alias=AliasPath(
            "metadata", "annotations", PREVIOUS_REPLICA_COUNT_ANNOTATION
        ),
    )
    """The original number of replicas if we explicitly scaled down."""


class Service(NamespacedResource):
    """A Service."""

    kind: Literal["Service"]
    """The kind of a Service is always Service."""

    previous_loadbalancer_ip: IPv4Address | None = Field(
        default=None,
        validation_alias=AliasPath(
            "metadata", "annotations", PREVIOUS_LOAD_BALANCER_IP_ANNOTATION
        ),
    )
    """The original loadBalancerIP, if we previously released it."""

    spec_load_balancer_ip: IPv4Address | None = Field(
        default=None,
        validation_alias=AliasPath("spec", "loadBalancerIP"),
    )
    """The load balancer IP set in the spec"""

    status_load_balancer_ip: IPv4Address | None = Field(
        default=None,
        validation_alias=AliasPath(
            "status", "loadBalancer", "ingress", 0, "ip"
        ),
    )
    """The load balancer IP in the ingress in the status."""


class ServiceIPSpecPatch(BaseModel):
    """A patch to a Service spec containing an IP address."""

    model_config = ConfigDict(validate_by_name=True)

    load_balancer_ip: IPv4Address = Field(serialization_alias="loadBalancerIP")
    """The IP address to assign to a Service in this patch."""


class ServiceIPPatch(BaseModel):
    """A model to validate a patch to assign an IP address to a Service."""

    spec: ServiceIPSpecPatch
    """The spec containing the IP addess to patch."""


class ServiceTypeSpecPatch(BaseModel):
    """A patch to a Service spec containing an IP address."""

    model_config = ConfigDict(validate_by_name=True)

    type: ServiceType
    """The spec.type of the Service."""


class ServiceTypePatch(BaseModel):
    """A model to validate a patch to assign an type  to a Service."""

    spec: ServiceTypeSpecPatch
    """The spec containing the IP addess to patch."""
