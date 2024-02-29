"""Pydantic models for Phalanx environments."""

from __future__ import annotations

from enum import Enum

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    ConfigDict,
    Field,
    GetJsonSchemaHandler,
    field_validator,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from safir.pydantic import CamelCaseModel

from .applications import Application, ApplicationInstance
from .secrets import Secret

__all__ = [
    "ControlSystemConfig",
    "Environment",
    "EnvironmentBaseConfig",
    "EnvironmentConfig",
    "EnvironmentDetails",
    "GCPMetadata",
    "GafaelfawrGitHubGroup",
    "GafaelfawrGitHubTeam",
    "GafaelfawrScope",
    "IdentityProvider",
    "OnepasswordConfig",
    "PhalanxConfig",
]


class GCPMetadata(CamelCaseModel):
    """Google Cloud Platform hosting metadata.

    Holds information about where in Google Cloud Platform this Phalanx
    environment is hosted. This supports generating documentation that
    includes this metadata, making it easier for administrators to know what
    options to pass to :command:`gcloud` to do things such as get Kubernetes
    credentials.
    """

    project_id: str = Field(
        ...,
        title="GCP project ID",
        description="Project ID of GCP project hosting this environment",
    )

    region: str = Field(
        ...,
        title="GCP region",
        description="GCP region in which this environment is hosted",
    )

    cluster_name: str = Field(
        ...,
        title="Kubernetes cluster name",
        description="Name of the GKE cluster hosting this environment",
    )


class OnepasswordConfig(CamelCaseModel):
    """Configuration for 1Password static secrets source."""

    connect_url: AnyHttpUrl = Field(
        ...,
        title="1Password Connect URL",
        description="URL to the 1Password Connect API server",
    )

    vault_title: str = Field(
        ...,
        title="1Password vault title",
        description=(
            "Title of the 1Password vault from which to retrieve secrets"
        ),
    )


class ControlSystemConfig(CamelCaseModel):
    """Configuration for the Control System."""

    app_namespace: str | None = Field(
        None,
        title="Application Namespace",
        description=(
            "Set the namespace for the control system components. Each control"
            " system application consists of many components that need to know"
            " what namespace to which they belong."
        ),
    )

    image_tag: str | None = Field(
        None,
        title="Image Tag",
        description=("The image tag to use for control system images."),
    )

    site_tag: str | None = Field(
        None,
        title="Site Tag",
        description=(
            "The tag that tells the control system component where it is"
            " running."
        ),
    )

    topic_name: str | None = Field(
        None,
        title="Topic Identifier",
        description="The Kafka identifier for control system topics.",
    )

    kafka_broker_address: str | None = Field(
        None,
        title="Kafka Broker Address",
        description=(
            "The Kafka broker address for the control system components."
        ),
    )

    kafka_topic_replication_factor: int | None = Field(
        None,
        title="Kafka Topic Replication Factor",
        description=(
            "The Kafka topic replication factor for control system components."
        ),
    )

    schema_registry_url: str | None = Field(
        None,
        title="Schema Registry URL",
        description=(
            "The Schema Registry URL for the control system components."
        ),
    )

    s3_endpoint_url: str | None = Field(
        None,
        title="S3 Endpoint URL",
        description="The S3 URL for the environment specific LFA.",
    )


class EnvironmentBaseConfig(CamelCaseModel):
    """Configuration common to `~phalanx.models.environments.EnvironmentConfig`
    and `~phalanx.models.environments.Environment`.
    """

    name: str = Field(..., title="Name", description="Name of the environment")

    fqdn: str = Field(
        ...,
        title="Domain name",
        description=(
            "Fully-qualified domain name on which the environment listens"
        ),
    )

    butler_repository_index: str | None = Field(
        None,
        title="Butler repository index URL",
        description="URL to Butler repository index",
    )

    butler_server_repositories: dict[str, AnyUrl] | None = Field(
        None,
        title="Butler repositories accessible via Butler server",
        description=(
            "A mapping from label to repository URI for Butler repositories"
            "served by Butler server in this environment."
        ),
    )

    gcp: GCPMetadata | None = Field(
        None,
        title="GCP hosting metadata",
        description=(
            "If this environment is hosted on Google Cloud Platform,"
            " metadata about the hosting project, location, and other details."
            " Used to generate additional environment documentation."
        ),
    )

    onepassword: OnepasswordConfig | None = Field(
        None,
        title="1Password configuration",
        description=(
            "Configuration for using 1Password as a static secrets source"
        ),
    )

    vault_url: AnyHttpUrl | None = Field(
        None,
        title="Vault server URL",
        description=(
            "URL of the Vault server. This is required in the merged values"
            " file that includes environment overrides, but the environment"
            " override file doesn't need to set it, so it's marked as"
            " optional for schema checking purposes to allow the override"
            " file to be schema-checked independently."
        ),
    )

    vault_path_prefix: str = Field(
        ...,
        title="Vault path prefix",
        description="Prefix of Vault paths, including the KV v2 mount point",
    )

    control_system: ControlSystemConfig | None = None

    @field_validator("onepassword", mode="before")
    @classmethod
    def _validate_onepassword(
        cls, v: dict[str, str] | None
    ) -> dict[str, str] | None:
        if not v:
            return v
        if not isinstance(v, dict):
            raise ValueError("onepassword is not a dictionary")  # noqa: TRY004

        # The validator is called multiple times, before and after alias
        # resolution, so needs to handle both possible spellings.
        if not v.get("connectUrl") and not v.get("connect_url"):
            return None

        return v

    @property
    def vault_path(self) -> str:
        """Vault path without the initial Kv2 mount point."""
        _, path = self.vault_path_prefix.split("/", 1)
        return path

    @property
    def vault_read_approle(self) -> str:
        """Name of the Vault read AppRole for this environment."""
        # AppRole names cannot contain /, so we'll use only the final
        # component of the path for the AppRole name.
        vault_path = self.vault_path
        if "/" in vault_path:
            _, approle_name = vault_path.rsplit("/", 1)
            return approle_name
        else:
            return vault_path

    @property
    def vault_write_token(self) -> str:
        """Display name of the Vault write token for this environment.

        Unlike AppRole names, this could include a slash, but use the same
        base name as the AppRole for consistency and simplicity. Vault always
        prepends ``token-``, which we strip off when creating the token.
        """
        return f"token-{self.vault_read_approle}"

    @property
    def vault_read_policy(self) -> str:
        """Name of the Vault read policy for this environment."""
        return f"{self.vault_path}/read"

    @property
    def vault_write_policy(self) -> str:
        """Name of the Vault write policy for this environment."""
        return f"{self.vault_path}/write"


class EnvironmentConfig(EnvironmentBaseConfig):
    """Configuration for a Phalanx environment.

    This is a model for the :file:`values-{environment}.yaml` files for each
    environment and is also used to validate those files. For the complete
    configuration for an environment, initialize this model with the merger of
    :file:`values.yaml` and :file:`values-{environment}.yaml`.

    Fields listed here are not available to application linting. If the field
    value has to be injected during linting, the field needs to be defined in
    `EnvironmentBaseConfig` instead.
    """

    applications: dict[str, dict[str, bool]] = Field(
        ...,
        title="Enabled applications by project",
        description=(
            "Dict of projects and applications and whether they are enabled"
        ),
    )

    repo_url: str | None = Field(
        None,
        title="URL of Git repository",
        description=(
            "URL of the Git repository holding Argo CD configuration. This is"
            " required in the merged values file that includes environment"
            " overrides, but the environment override file doesn't need to"
            " set it, so it's marked as optional for schema checking purposes"
            " to allow the override file to be schema-checked independently."
        ),
    )

    target_revision: str | None = Field(
        None,
        title="Git repository branch",
        description=(
            "Branch of the Git repository holding Argo CD configuration. This"
            " is required in the merged values file that includes environment"
            " overrides, but the environment override file doesn't need to set"
            " it, so it's marked as optional for schema checking purposes to"
            " allow the override file to be schema-checked independently."
        ),
    )

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = handler(core_schema)
        schema = handler.resolve_ref_schema(schema)
        schema["$id"] = "https://phalanx.lsst.io/schemas/environment.json"
        return schema

    @property
    def enabled_applications(self) -> list[str]:
        """Names of all applications enabled for this environment."""
        enabled_apps = []

        for apps in self.applications.values():
            for app, enabled in apps.items():
                if enabled:
                    enabled_apps.append(app)

        return sorted(enabled_apps)


class Environment(EnvironmentBaseConfig):
    """A Phalanx environment and its associated settings."""

    applications: dict[str, ApplicationInstance]
    """Applications enabled for that environment, by name."""

    model_config = ConfigDict(populate_by_name=True)

    def all_applications(self) -> list[ApplicationInstance]:
        """Return all enabled applications in sorted order."""
        return sorted(self.applications.values(), key=lambda a: a.name)

    def all_secrets(self) -> list[Secret]:
        """Return all secrets regardless of application."""
        secrets: list[Secret] = []
        for application in self.all_applications():
            secrets.extend(application.secrets.values())
        return secrets


class IdentityProvider(Enum):
    """Type of identity provider used by Gafaelfawr."""

    CILOGON = "CILogon"
    GITHUB = "GitHub"
    OIDC = "OpenID Connect"
    NONE = "None"


class GafaelfawrGitHubTeam(BaseModel):
    """Designates a GitHub team for use as a Gafaelfawr group."""

    organization: str
    """GitHub organization."""

    team: str
    """GitHub team within that organization."""


class GafaelfawrGitHubGroup(BaseModel):
    """A group based on a GitHub team."""

    github: GafaelfawrGitHubTeam
    """Specification for the team."""

    def to_rst(self) -> str:
        organization = self.github.organization
        team = self.github.team
        url = f"https://github.com/orgs/{organization}/teams/{team}"
        return f":fab:`github` `{organization}/{team} <{url}>`__"


class GafaelfawrScope(BaseModel):
    """A Gafaelfawr scope and its associated groups."""

    scope: str
    """Name of the scope."""

    groups: list[str | GafaelfawrGitHubGroup]
    """List of groups that grant that scope."""

    def groups_as_rst(self) -> list[str]:
        """Format the groups as a list of reStructuredText elements."""
        result = []
        for group in self.groups:
            if isinstance(group, GafaelfawrGitHubGroup):
                result.append(group.to_rst())
            else:
                result.append(f"``{group}``")
        return result


class EnvironmentDetails(EnvironmentBaseConfig):
    """Full details about an environment, including auth and Argo CD.

    Used primarily for documentation generation, which needs details from the
    Argo CD and Gafaelfawr configurations for that environment. Use
    `~phalanx.models.environments.EnvironmentConfig` instead when only the
    basic environment configuration is needed.
    """

    applications: list[Application]
    """List of enabled applications."""

    argocd_url: str | None
    """URL for the Argo CD UI."""

    argocd_rbac: list[list[str]]
    """Argo CD RBAC configuration as a list of parsed CSV lines."""

    identity_provider: IdentityProvider
    """Type of identity provider used by Gafaelfawr in this environment."""

    gafaelfawr_scopes: list[GafaelfawrScope]
    """Gafaelfawr scopes and their associated groups."""

    @property
    def argocd_rbac_csv(self) -> list[str]:
        """RBAC configuration formatted for an reStructuredText csv-table."""
        result = []
        for rule in self.argocd_rbac:
            formatted = [f"``{r}``" for r in rule]
            result.append(",".join(formatted))
        return result


class PhalanxConfig(BaseModel):
    """Root container for the entire Phalanx configuration."""

    environments: list[EnvironmentDetails]
    """Phalanx environments."""

    applications: list[Application]
    """All Phalanx applications enabled for any environment."""
