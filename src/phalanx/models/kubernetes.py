"""Models representing Kubernetes resources."""

from typing import Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

__all__ = ["CronJob", "Resources"]


class CronJob(BaseModel):
    """A CronJob kubernetes resource."""

    model_config = ConfigDict(validate_by_name=True)

    kind: Literal["CronJob"]
    """The kind field will always be CronJob."""

    namespace: str = Field(validation_alias=AliasPath("metadata", "namespace"))
    """The namespace the resource is in."""

    name: str = Field(validation_alias=AliasPath("metadata", "name"))
    """The name of the resource."""


class Resources(BaseModel):
    """A list of resources returned from a kubectl command."""

    # This will eventually be a union of different types
    items: list[CronJob]
    """A list of Kubernetes resources."""

    kind: Literal["List"]
    """The kind field will always be List."""
