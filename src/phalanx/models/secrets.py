"""Pydantic models for Phalanx application secrets."""

from __future__ import annotations

import os
import secrets
from base64 import urlsafe_b64encode
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import BaseModel, Extra, Field, SecretStr, validator

__all__ = [
    "ConditionalMixin",
    "ConditionalSecretConfig",
    "ConditionalSecretCopyRules",
    "ConditionalSecretGenerateRules",
    "ConditionalSimpleSecretGenerateRules",
    "ConditionalSourceSecretGenerateRules",
    "ResolvedSecret",
    "Secret",
    "SecretConfig",
    "SecretCopyRules",
    "SecretGenerateRules",
    "SecretGenerateType",
    "SimpleSecretGenerateRules",
    "SourceSecretGenerateRules",
]


class ConditionalMixin(BaseModel):
    """Mix-in class for elements that may have a condition."""

    condition: str | None = Field(
        None,
        description=(
            "Configuration only applies if this Helm chart setting is set to a"
            " true value"
        ),
        title="Condition",
        alias="if",
    )


class SecretCopyRules(BaseModel):
    """Rules for copying a secret value from another secret."""

    application: str
    """Application from which the secret should be copied."""

    key: str
    """Secret key from which the secret should be copied."""

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


class ConditionalSecretCopyRules(SecretCopyRules, ConditionalMixin):
    """Possibly conditional rules for copying a secret value from another."""


class SecretGenerateType(str, Enum):
    """Type of secret for generated secrets."""

    password = "password"
    gafaelfawr_token = "gafaelfawr-token"
    fernet_key = "fernet-key"
    rsa_private_key = "rsa-private-key"
    bcrypt_password_hash = "bcrypt-password-hash"
    mtime = "mtime"


class SimpleSecretGenerateRules(BaseModel):
    """Rules for generating a secret value with no source information."""

    type: Literal[
        SecretGenerateType.password,
        SecretGenerateType.gafaelfawr_token,
        SecretGenerateType.fernet_key,
        SecretGenerateType.rsa_private_key,
    ]
    """Type of secret."""

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid

    def generate(self) -> SecretStr:
        """Generate a new secret following these rules."""
        match self.type:
            case SecretGenerateType.password:
                return SecretStr(secrets.token_hex(32))
            case SecretGenerateType.gafaelfawr_token:
                key = urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
                secret = urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
                return SecretStr(f"gt-{key}.{secret}")
            case SecretGenerateType.fernet_key:
                return SecretStr(Fernet.generate_key().decode())
            case SecretGenerateType.rsa_private_key:
                private_key = rsa.generate_private_key(
                    backend=default_backend(),
                    public_exponent=65537,
                    key_size=2048,
                )
                private_key_bytes = private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
                return SecretStr(private_key_bytes.decode())


class ConditionalSimpleSecretGenerateRules(
    SimpleSecretGenerateRules, ConditionalMixin
):
    """Conditional rules for generating a secret value with no source."""


class SourceSecretGenerateRules(BaseModel):
    """Rules for generating a secret from another secret."""

    type: Literal[
        SecretGenerateType.bcrypt_password_hash,
        SecretGenerateType.mtime,
    ]
    """Type of secret."""

    source: str
    """Key of secret on which this secret is based.

    This may only be set by secrets of type ``bcrypt-password-hash`` or
    ``mtime``.
    """

    def generate(self, source: SecretStr) -> SecretStr:
        match self.type:
            case SecretGenerateType.bcrypt_password_hash:
                password_hash = bcrypt.hashpw(
                    source.get_secret_value().encode(),
                    bcrypt.gensalt(rounds=15),
                )
                return SecretStr(password_hash.decode())
            case SecretGenerateType.mtime:
                date = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
                return SecretStr(date)


class ConditionalSourceSecretGenerateRules(
    SourceSecretGenerateRules, ConditionalMixin
):
    """Conditional rules for generating a secret from another secret."""


SecretGenerateRules = SimpleSecretGenerateRules | SourceSecretGenerateRules
ConditionalSecretGenerateRules = (
    ConditionalSimpleSecretGenerateRules | ConditionalSourceSecretGenerateRules
)


class SecretConfig(BaseModel):
    """Specification for an application secret."""

    description: str
    """Description of the secret."""

    copy_rules: SecretCopyRules | None = Field(
        None,
        description="Rules for where the secret should be copied from",
        alias="copy",
    )

    generate: SecretGenerateRules | None = None
    """Rules for how the secret should be generated."""

    value: SecretStr | None = None
    """Secret value."""

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


class ConditionalSecretConfig(SecretConfig, ConditionalMixin):
    """Possibly conditional specification for an application secret."""

    copy_rules: ConditionalSecretCopyRules | None = Field(
        None,
        description="Rules for where the secret should be copied from",
        alias="copy",
    )

    generate: ConditionalSecretGenerateRules | None = None
    """Rules for how the secret should be generated."""

    @validator("generate")
    def _validate_generate(
        cls,
        v: ConditionalSecretGenerateRules | None,
        values: dict[str, Any],
    ) -> ConditionalSecretGenerateRules | None:
        has_copy = "copy" in values and "condition" not in values["copy"]
        if v and has_copy:
            msg = "both copy and generate may not be set for the same secret"
            raise ValueError(msg)
        return v

    @validator("value")
    def _validate_value(
        cls, v: SecretStr | None, values: dict[str, Any]
    ) -> SecretStr | None:
        has_copy = values.get("copy") and "condition" not in values["copy"]
        has_generate = (
            values.get("generate") and "condition" not in values["generate"]
        )
        if v and (has_copy or has_generate):
            msg = "value may not be set if copy or generate is set"
            raise ValueError(msg)
        return v


class Secret(SecretConfig):
    """Specification for an application secret for a specific environment.

    The same as `SecretConfig` except augmented with the secret application
    and key for internal convenience.
    """

    key: str
    """Key of the secret."""

    application: str
    """Application of the secret."""


class ResolvedSecret(BaseModel):
    """A secret that has been resolved for a given application instance.

    Secret resolution means that the configuration has been translated into
    either a secret value or knowledge that the secret is a static secret that
    must come from elsewhere.
    """

    key: str
    """Key of the secret."""

    application: str
    """Application for which the secret is required."""

    value: SecretStr | None = None
    """Value of the secret if known."""


class StaticSecret(BaseModel):
    """Value of a static secret provided in a YAML file."""

    description: str | None = None
    """Description of the secret (ignored)."""

    value: SecretStr | None
    """Value of the secret, or `None` if it's not known."""
