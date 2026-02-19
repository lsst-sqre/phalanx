"""Models representing ArgoCD entities."""

from pydantic import BaseModel, ConfigDict, RootModel
from pydantic.alias_generators import to_camel

__all__ = ["Application", "ApplicationList", "Metadata", "Resource", "Status"]


class YAMLModel(BaseModel):
    """A model that accepts camelCase keys."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Metadata(YAMLModel):
    """Metadata for an ArgoCD application."""

    name: str
    """The name of this application."""


class Resource(YAMLModel):
    """Info about a Kubernetes resource in an ArgoCD application."""

    name: str
    """The Kubernetes metadata.name of this resource."""

    kind: str
    """The Kubernetes kind of this resource"""

    status: str | None = None
    """The sync status of this resource."""


class SyncStatus(YAMLModel):
    """The sync status an entire ArgoCD application."""

    status: str


class Status(YAMLModel):
    """Info about the status of an ArgoCD application."""

    resources: list[Resource]
    """The Kubernetes resources managed by this ArgoCD application."""

    sync: SyncStatus
    """The sync status of this application."""


class Source(YAMLModel):
    """Info about where an ArgoCD application is synced from."""

    target_revision: str


class Spec(YAMLModel):
    """The specification of an ArgoCD application."""

    source: Source


class Application(YAMLModel):
    """An ArgoCD application."""

    metadata: Metadata
    """Metadata about this ArgoCD application."""

    status: Status
    """Info about the status of this ArgoCD application and its resources."""

    spec: Spec
    """The specification of this ArgoCD application."""

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

    def get_unsynced(self) -> list[Application]:
        """Return a list of applications that is not synced."""
        return [
            app
            for app in self.root
            if (
                app.metadata.name == "sasquatch"
                and not self._is_sasquatch_synced(app)
            )
            or app.status.sync.status != "Synced"
        ]

    def get_different_ref(self, ref: str) -> list[Application]:
        """Return all applications that are synced to a different ref."""
        return [
            app for app in self.root if app.spec.source.target_revision != ref
        ]

    def _is_sasquatch_synced(self, app: Application) -> bool:
        """Return True if all except PVCs are synced in the sasquatch app.

        There is an issue in our Strimzi sasquatch cluster where some PVCs
        always show as out of sync.

        Parameters
        ----------
        app
            The sasquatch ArgoCD application.
        """
        return not any(
            resource
            for resource in app.status.resources
            if resource.kind != "PersistentVolumeClaim"
            and resource.status != "Synced"
        )
