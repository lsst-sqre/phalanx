"""Models representing ArgoCD entities."""

from pydantic import BaseModel, RootModel

__all__ = ["Application", "ApplicationList", "Metadata", "Resource", "Status"]


class Metadata(BaseModel):
    """Metadata for an ArgoCD application."""

    name: str
    """The name of this application."""


class Resource(BaseModel):
    """Info about a Kubernetes resource in an ArgoCD application."""

    name: str
    """The Kubernetes metadata.name of this resource."""

    kind: str
    """The Kubernetes kind of this resource"""


class Status(BaseModel):
    """Info about the status of an ArgoCD application."""

    resources: list[Resource]
    """The Kubernetes resources managed by this ArgoCD application."""


class Application(BaseModel):
    """An ArgoCD application."""

    metadata: Metadata
    """Metadata about this ArgoCD application."""

    status: Status
    """Info about the status of this ArgoCD application and its resources."""

    def has_resource(self, kind: str) -> bool:
        """Tell if the application manages a particular kind of resource."""
        return any(
            resource
            for resource in self.status.resources
            if resource.kind == kind
        )


class ApplicationList(RootModel[list[Application]]):
    """A list of ArgoCD applications."""

    def with_resource(self, kind: str) -> list[Application]:
        """Return all of the applications that manage a kind of resource."""
        return [
            application
            for application in self.root
            if application.has_resource(kind)
        ]
