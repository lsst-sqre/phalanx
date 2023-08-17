"""Pydantic models for Phalanx environments."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field
from safir.pydantic import CamelCaseModel

from .applications import Application, ApplicationInstance
from .secrets import Secret

__all__ = [
    "Environment",
    "EnvironmentConfig",
    "EnvironmentDetails",
    "EnvironmentVaultConfig",
    "GafaelfawrGitHubGroup",
    "GafaelfawrGitHubTeam",
    "GafaelfawrScope",
    "IdentityProvider",
    "PhalanxConfig",
]


class EnvironmentVaultConfig(CamelCaseModel):
    """Vault configuration for a specific environment."""

    vault_url: str
    """URL of Vault server for this environment."""

    vault_path_prefix: str
    """Prefix of Vault paths, including the Kv2 mount point."""

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
        name as the AppRole for consistency and simplicity.
        """
        return self.vault_read_approle

    @property
    def vault_read_policy(self) -> str:
        """Name of the Vault read policy for this environment."""
        return f"{self.vault_path}/read"

    @property
    def vault_write_policy(self) -> str:
        """Name of the Vault write policy for this environment."""
        return f"{self.vault_path}/write"


class EnvironmentConfig(EnvironmentVaultConfig):
    """Configuration for a Phalanx environment.

    This is a partial model for the environment :file:`values.yaml` file.
    It cannot currently be used as a real model because enabled applications
    are stored as a list rather than the data structure used in
    :file:`values.yaml`.
    """

    name: str
    """Name of the environment."""

    fqdn: str
    """Fully-qualified domain name of the environment."""

    applications: list[str] = Field(
        [], description="List of enabled applications"
    )


class Environment(EnvironmentVaultConfig):
    """A Phalanx environment and its associated settings."""

    name: str
    """Name of the environment."""

    applications: dict[str, ApplicationInstance]
    """Applications enabled for that environment, by name."""

    class Config:
        allow_population_by_field_name = True

    def all_applications(self) -> list[ApplicationInstance]:
        """Return all enabled applications in sorted order."""
        return sorted(self.applications.values(), key=lambda a: a.name)

    def all_secrets(self) -> list[Secret]:
        """Return all secrets regardless of application."""
        secrets = []
        for application in self.all_applications():
            secrets.extend(application.secrets)
        return secrets


class IdentityProvider(Enum):
    """Type of identity provider used by Gafaelfawr."""

    CILOGON = "CILogon"
    GITHUB = "GitHub"
    OIDC = "OpenID Connect"


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


class EnvironmentDetails(BaseModel):
    """Full details about an environment, including auth and Argo CD.

    Used primarily for documentation generation, which needs details from the
    Argo CD and Gafaelfawr configurations for that environment.  Use
    `EnvironmentConfig` instead when only the basic environment configuration
    is needed.
    """

    name: str
    """Name of the environment."""

    fqdn: str
    """Fully-qualified domain name of the environment."""

    applications: list[Application] = Field(
        [], description="List of enabled applications"
    )

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
