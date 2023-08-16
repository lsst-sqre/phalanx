"""Constants for the Phalanx support code.

Things that arguably could be configurable but haven't yet been made into
actual configuration options.
"""

from __future__ import annotations

__all__ = [
    "VAULT_WRITE_TOKEN_LIFETIME",
]

VAULT_WRITE_TOKEN_LIFETIME = "3650d"
"""Default lifetime to set for Vault write tokens."""
