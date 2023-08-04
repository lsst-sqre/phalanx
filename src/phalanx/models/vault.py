"""Models representing Vault objects."""

from __future__ import annotations

import yaml
from pydantic import BaseModel

__all__ = ["VaultToken"]


class VaultAppRole(BaseModel):
    """Newly-created Vault AppRole for secret access."""

    role_id: str
    """Unique identifier of the AppRole."""

    secret_id: str
    """Authentication credentials for the AppRole."""

    secret_id_accessor: str
    """Accessor for the AppRole authentication credentials."""

    policies: list[str]
    """Policies applied to this AppRole."""

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.dict())


class VaultToken(BaseModel):
    """Newly-created Vault token for secret access."""

    token: str
    """Secret token."""

    accessor: str
    """Accessor for the token, used to get metadata or revoke it."""

    policies: list[str]
    """Policies applied to this token."""

    def to_yaml(self) -> str:
        """Format the data in YAML."""
        return yaml.dump(self.dict())
