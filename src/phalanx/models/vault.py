"""Models representing Vault objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from base64 import b64encode
from datetime import datetime

import yaml
from pydantic import BaseModel, Field

from ..constants import (
    VAULT_APPROLE_SECRET_TEMPLATE,
    VAULT_TOKEN_SECRET_TEMPLATE,
)

__all__ = [
    "VaultAppRole",
    "VaultAppRoleCredentials",
    "VaultAppRoleMetadata",
    "VaultCredentials",
    "VaultToken",
    "VaultTokenCredentials",
    "VaultTokenMetadata",
]


class VaultAppRoleMetadata(BaseModel):
    """Metadata about a new or existing Vault AppRole."""

    role_id: str
    """Unique identifier of the AppRole."""

    policies: list[str]
    """Policies applied to this AppRole."""

    token_ttl: int | str = Field(
        0,
        title="Token lifetime",
        description=(
            "Either an integer number of seconds or a duration string."
            " 0 means there is no limit other than Vault defaults."
        ),
    )

    token_max_ttl: int | str = Field(
        0,
        title="Maximum token lifetime",
        description=(
            "Maximum token lifetime even after renewal. Either an integer"
            " number of seconds or a duration string. 0 means there is no"
            " limit other than Vault defaults."
        ),
    )


class VaultAppRole(VaultAppRoleMetadata):
    """Newly-created Vault AppRole for secret access."""

    secret_id: str
    """Authentication credentials for the AppRole."""

    secret_id_accessor: str
    """Accessor for the AppRole authentication credentials."""

    def to_kubernetes_secret(self, name: str) -> str:
        """Format the data as a secret for vault-secrets-operator.

        Parameters
        ----------
        name
            Name of the secret to create.

        Returns
        -------
        str
            YAML creating a Kubernetes ``Secret`` resource for `Vault Secrets
            Operator`_, suitable for passing to :command:`kubectl apply`.
        """
        role_id = b64encode(self.role_id.encode()).decode()
        secret_id = b64encode(self.secret_id.encode()).decode()
        return VAULT_APPROLE_SECRET_TEMPLATE.format(
            name=name, role_id=role_id, secret_id=secret_id
        )

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.model_dump())


class VaultCredentials(BaseModel, ABC):
    """Credentials used for Vault access.

    Can hold either AppRole credentials or a simple token, but always holds
    one or the other.
    """

    @abstractmethod
    def to_kubernetes_secret(self, name: str) -> str:
        """Format the data as a secret for vault-secrets-operator.

        Parameters
        ----------
        name
            Name of the secret to create.

        Returns
        -------
        str
            YAML creating a Kubernetes ``Secret`` resource for `Vault Secrets
            Operator`_, suitable for passing to :command:`kubectl apply`.
        """


class VaultAppRoleCredentials(VaultCredentials):
    """Credentials for Vault access using an AppRole."""

    role_id: str
    """Unique identifier of the AppRole."""

    secret_id: str
    """Authentication credentials for the AppRole."""

    def to_kubernetes_secret(self, name: str) -> str:
        role_id = b64encode(self.role_id.encode()).decode()
        secret_id = b64encode(self.secret_id.encode()).decode()
        return VAULT_APPROLE_SECRET_TEMPLATE.format(
            name=name, role_id=role_id, secret_id=secret_id
        )


class VaultTokenCredentials(VaultCredentials):
    """Credentials for Vault access using a token."""

    token: str
    """Vault token."""

    def to_kubernetes_secret(self, name: str) -> str:
        token = b64encode(self.token.encode()).decode()
        return VAULT_TOKEN_SECRET_TEMPLATE.format(name=name, token=token)


class VaultTokenMetadata(BaseModel):
    """Metadata about a new or existing Vault token."""

    display_name: str
    """Display name of the token."""

    accessor: str
    """Accessor for the token, used to get metadata or revoke it."""

    expires: datetime | None
    """When the token expires, if it does."""

    policies: list[str]
    """Policies applied to this token."""


class VaultToken(VaultTokenMetadata):
    """Newly-created Vault token for secret access."""

    token: str
    """Secret token."""

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.model_dump())
