"""Models representing Vault objects."""

from __future__ import annotations

from datetime import datetime

import yaml
from pydantic import BaseModel

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

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.model_dump())


class VaultTokenMetadata(BaseModel):
    """Metadata about a new or existing Vault token."""

    display_name: str
    """Display name of the token."""

    accessor: str
    """Accessor for the token, used to get metadata or revoke it."""

    expires: datetime
    """When the token expires."""

    policies: list[str]
    """Policies applied to this token."""


class VaultToken(VaultTokenMetadata):
    """Newly-created Vault token for secret access."""

    token: str
    """Secret token."""

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.model_dump())
