"""Pydantic models for Phalanx environments."""

from __future__ import annotations

from enum import Enum

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    GetJsonSchemaHandler,
    field_validator,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from safir.pydantic import CamelCaseModel

from .applications import Application, ApplicationInstance
from .secrets import Secret

__all__ = [
    "Environment",
    "EnvironmentBaseConfig",
    "EnvironmentConfig",
    "EnvironmentDetails",
    "GafaelfawrGitHubGroup",
    "GafaelfawrGitHubTeam",
    "GafaelfawrScope",
    "IdentityProvider",
    "OnepasswordConfig",
    "PhalanxConfig",
]


class OnepasswordConfig(CamelCaseModel):
    """Configuration for 1Password static secrets source."""

    connect_url: AnyHttpUrl
    """URL to the 1Password Connect API server."""

    vault_title: str
    """Title of the 1Password vault from which to retrieve secrets."""


class EnvironmentBaseConfig(CamelCaseModel):
    """Configuration common to `EnviromentConfig` and `Environment`."""

    name: str
    """Name of the environment."""

    fqdn: str
    """Fully-qualified domain name."""

    onepassword: OnepasswordConfig | None = None
    """Configuration for using 1Password as a static secrets source."""

    vault_url: str
    """URL of Vault server."""

    vault_path_prefix: str
    """Prefix of Vault paths, including the Kv2 mount point."""

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
    """

    applications: dict[str, bool]
    """List of applications and whether they are enabled."""

    butler_repository_index: str | None = None
    """URL to Butler repository index."""

    onepassword_uuid: str | None = None
    """UUID of 1Password item in which to find Vault tokens.

    This is used only by the old installer and will be removed once the new
    secrets management and 1Password integration is deployed everywhere.
    """

    repo_url: str | None = None
    """URL of the Git repository holding Argo CD configuration.

    This is required in the merged values file that includes environment
    overrides, but the environment override file doesn't need to set it, so
    it's marked as optional for schema checking purposes to allow the override
    file to be schema-checked independently.
    """

    target_revision: str | None = None
    """Branch of the Git repository holding Argo CD configuration.

    This is required in the merged values file that includes environment
    overrides, but the environment override file doesn't need to set it, so
    it's marked as optional for schema checking purposes to allow the override
    file to be schema-checked independently.
    """

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
        return sorted(k for k, v in self.applications.items() if v)


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
    Argo CD and Gafaelfawr configurations for that environment.  Use
    `EnvironmentConfig` instead when only the basic environment configuration
    is needed.
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
