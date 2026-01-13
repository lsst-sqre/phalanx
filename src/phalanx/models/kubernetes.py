"""Models representing Kubernetes resources."""

from typing import Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from ..constants import PREVIOUS_REPLICA_COUNT_ANNOTATION

__all__ = [
    "CronJob",
    "Deployment",
    "NamespacedResource",
    "ResourceList",
    "StatefulSet",
    "Workload",
]


class NamespacedResource(BaseModel):
    """Properties common to a namespaced Kubernetes resource."""

    model_config = ConfigDict(validate_by_name=True)

    kind: str
    """The kind of Kubernetes resource."""

    namespace: str = Field(validation_alias=AliasPath("metadata", "namespace"))
    """The namespace the resource is in."""

    name: str = Field(validation_alias=AliasPath("metadata", "name"))
    """The name of the resource."""


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
