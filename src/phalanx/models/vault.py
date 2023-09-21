"""Models representing Vault objects."""

from __future__ import annotations

from base64 import b64encode
from datetime import datetime

import yaml
from pydantic import BaseModel

from ..constants import VAULT_SECRET_TEMPLATE

__all__ = [
    "VaultAppRole",
    "VaultAppRoleMetadata",
    "VaultToken",
    "VaultTokenMetadata",
]


class VaultAppRoleMetadata(BaseModel):
    """Metadata about a new or existing Vault AppRole."""

    role_id: str
    """Unique identifier of the AppRole."""

    policies: list[str]
    """Policies applied to this AppRole."""


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
            YAML creating a Kubernetes ``Secret`` resource for
            vault-secrets-operator_, suitable for passing to :command:`kubectl
            apply`.
        """
        role_id = b64encode(self.role_id.encode()).decode()
        secret_id = b64encode(self.secret_id.encode()).decode()
        return VAULT_SECRET_TEMPLATE.format(
            name=name, role_id=role_id, secret_id=secret_id
        )

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.model_dump())


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
