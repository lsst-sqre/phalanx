"""Constants for the Phalanx support code.

Things that arguably could be configurable but haven't yet been made into
actual configuration options.
"""

from __future__ import annotations

from datetime import timedelta

__all__ = [
    "HELM_DOCLINK_ANNOTATION",
    "PULL_SECRET_DESCRIPTION",
    "VAULT_WRITE_TOKEN_LIFETIME",
    "VAULT_WRITE_TOKEN_WARNING_LIFETIME",
]

HELM_DOCLINK_ANNOTATION = "phalanx.lsst.io/docs"
"""Annotation in :file:`Chart.yaml` for application documentation links."""

PULL_SECRET_DESCRIPTION = (
    "Pull secrets for Docker registries. Each key under registries is the name"
    " of a Docker registry that needs a pull secret. The value should have two"
    " keys, username and password, that provide the HTTP Basic Auth"
    " credentials for that registry."
)
"""Description to put in the static secrets YAML file for ``pull-secret``."""

VAULT_WRITE_TOKEN_LIFETIME = "3650d"
"""Default lifetime to set for Vault write tokens."""

VAULT_WRITE_TOKEN_WARNING_LIFETIME = timedelta(days=7)
"""Remaining lifetime at which to warn that a token is about to expire."""
