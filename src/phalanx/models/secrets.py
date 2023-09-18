"""Pydantic models for Phalanx application secrets."""

from __future__ import annotations

import json
import secrets
from base64 import b64encode
from datetime import UTC, datetime
from enum import Enum
from typing import Literal, Self

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

from ..constants import PULL_SECRET_DESCRIPTION
from ..yaml import YAMLFoldedString
from .gafaelfawr import Token

__all__ = [
    "ConditionalMixin",
    "ConditionalSecretConfig",
    "ConditionalSecretCopyRules",
    "ConditionalSecretGenerateRules",
    "ConditionalSimpleSecretGenerateRules",
    "ConditionalSourceSecretGenerateRules",
    "PullSecret",
    "RegistryPullSecret",
    "ResolvedSecrets",
    "Secret",
    "SecretConfig",
    "SecretCopyRules",
    "SecretGenerateRules",
    "SecretGenerateType",
    "SecretOnepasswordConfig",
    "SimpleSecretGenerateRules",
    "SourceSecretGenerateRules",
    "StaticSecret",
    "StaticSecrets",
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

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


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

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def generate(self) -> SecretStr:
        """Generate a new secret following these rules."""
        match self.type:
            case SecretGenerateType.password:
                return SecretStr(secrets.token_hex(32))
            case SecretGenerateType.gafaelfawr_token:
                return SecretStr(str(Token()))
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


class SecretOnepasswordConfig(BaseModel):
    """Configuration for how a static secret is stored in 1Password."""

    encoded: bool = False
    """Whether the 1Password copy of the secret is encoded in base64.

    1Password doesn't support newlines in secrets, so secrets that contain
    significant newlines have to be encoded when storing them in 1Password.
    This flag indicates that this has been done, and therefore when retrieving
    the secret from 1Password, its base64-encoding must be undone.
    """


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

    onepassword: SecretOnepasswordConfig = SecretOnepasswordConfig()
    """Configuration for how the secret is stored in 1Password."""

    value: SecretStr | None = None
    """Secret value."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class ConditionalSecretConfig(SecretConfig, ConditionalMixin):
    """Possibly conditional specification for an application secret."""

    copy_rules: ConditionalSecretCopyRules | None = Field(
        None,
        description="Rules for where the secret should be copied from",
        alias="copy",
    )

    generate: ConditionalSecretGenerateRules | None = None
    """Rules for how the secret should be generated."""

    @model_validator(mode="after")
    def _validate_generate(self) -> Self:
        has_copy = self.copy_rules and not self.copy_rules.condition
        has_generate = self.generate and not self.generate.condition
        if has_copy and has_generate:
            msg = (
                "both copy and generate may not be set unconditionally for the"
                " same secret"
            )
            raise ValueError(msg)
        if (has_copy or has_generate) and self.value:
            msg = "value may not be set if copy or generate is set"
            raise ValueError(msg)
        return self


class Secret(SecretConfig):
    """Specification for an application secret for a specific environment.

    The same as `SecretConfig` except augmented with the secret application
    and key for internal convenience.
    """

    key: str
    """Key of the secret."""

    application: str
    """Application of the secret."""


class RegistryPullSecret(BaseModel):
    """Pull secret for a specific Docker Repository."""

    username: str = Field(
        ..., title="Username", description="HTTP Basic Auth username"
    )

    password: SecretStr = Field(
        ..., title="Password", description="HTTP Basic Auth password"
    )

    model_config = ConfigDict(extra="forbid")


class PullSecret(BaseModel):
    """Specification for a Docker pull secret."""

    description: YAMLFoldedString = Field(
        YAMLFoldedString(PULL_SECRET_DESCRIPTION),
        title="Description of pull secret",
        description=(
            "Description of the pull secret for humans reading the YAML file"
        ),
    )

    registries: dict[str, RegistryPullSecret] = Field(
        {},
        title="Pull secret by registry",
        description="Pull secrets for each registry that needs one",
    )
    model_config = ConfigDict(extra="forbid")

    def to_dockerconfigjson(self) -> str:
        """Convert to the serialized format used by Docker."""
        docker_config = {}
        for registry, data in self.registries.items():
            password = data.password.get_secret_value()
            auth = b64encode(f"{data.username}:{password}".encode()).decode()
            docker_config[registry] = {
                "auth": auth,
                "username": data.username,
                "password": password,
            }
        return json.dumps({"auths": docker_config})


class ResolvedSecrets(BaseModel):
    """All resolved secrets for a given Phalanx environment.

    Secret resolution means that the configuration has been translated into a
    secret value.
    """

    applications: dict[str, dict[str, SecretStr]] = Field(
        {},
        title="Secrets by application and key",
        description=(
            "Mapping of application to secret key to that resolved secret"
        ),
    )

    pull_secret: PullSecret | None = Field(
        None,
        title="Pull secret",
        description="Pull secret for the environment, if needed",
    )


class StaticSecret(BaseModel):
    """Value of a static secret provided in a YAML file."""

    description: YAMLFoldedString | None = Field(
        None,
        title="Description of secret",
        description="Intended for human writers and ignored by tools",
    )

    value: SecretStr | None = Field(
        None,
        title="Value of secret",
        description="Value of the secret, or `None` if it's not known",
    )

    model_config = ConfigDict(extra="forbid")


class StaticSecrets(BaseModel):
    """Model for the YAML file containing static secrets.

    This doubles as the model used to pass static secrets around internally,
    in which case the description fields of the `StaticSecret` members are
    ignored.
    """

    applications: dict[str, dict[str, StaticSecret]] = Field(
        {},
        title="Secrets by application and key",
        description=(
            "Mapping of application to secret key to that static secret"
        ),
    )

    pull_secret: PullSecret | None = Field(
        None,
        title="Pull secret",
        description="Pull secret for this environment, if any is needed",
        alias="pull-secret",
    )

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def for_application(self, application: str) -> dict[str, StaticSecret]:
        """Return any known secrets for an application.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        dict of StaticSecret
            Mapping of secret keys to `StaticSecret` objects. If the
            application has no static secrets, returns an empty dictionary.
        """
        return self.applications.get(application, {})
