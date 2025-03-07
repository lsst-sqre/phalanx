"""Service to manipulate Phalanx secrets."""

from __future__ import annotations

import binascii
import os
from base64 import b64decode
from collections import defaultdict
from dataclasses import dataclass, field

import yaml
from pydantic import SecretStr

from ..constants import ONEPASSWORD_ENCODED_WARNING
from ..exceptions import (
    MalformedOnepasswordSecretError,
    MissingOnepasswordSecretsError,
    NoOnepasswordConfigError,
    NoVaultCredentialsError,
    UnresolvedSecretsError,
    VaultNotFoundError,
)
from ..models.environments import Environment, EnvironmentBaseConfig
from ..models.secrets import (
    PullSecret,
    ResolvedSecrets,
    Secret,
    SourceSecretGenerateRules,
    StaticSecret,
    StaticSecrets,
)
from ..models.vault import VaultTokenCredentials
from ..storage.config import ConfigStorage
from ..storage.onepassword import OnepasswordStorage
from ..storage.vault import VaultClient, VaultStorage
from ..yaml import YAMLFoldedString

__all__ = [
    "SecretsAuditReport",
    "SecretsService",
]


@dataclass
class SecretsAuditReport:
    """Results of auditing secrets against the contents of Vault."""

    missing: list[str] = field(default_factory=list)
    """Secrets missing from Vault."""

    mismatch: list[str] = field(default_factory=list)
    """Secrets that are incorrect in Vault."""

    unknown: list[str] = field(default_factory=list)
    """Unexpected secrets in Vault."""

    def to_text(self) -> str:
        """Format as a textual report for output."""
        report = ""
        if self.missing:
            secrets = "\n• ".join(sorted(self.missing))
            report += "Missing secrets:\n• " + secrets + "\n"
        if self.mismatch:
            if self.missing:
                report += "\n"
            secrets = "\n• ".join(sorted(self.mismatch))
            heading = "Secrets that do not have their expected value:"
            report += f"{heading}\n• " + secrets + "\n"
        if self.unknown:
            if self.missing or self.mismatch:
                report += "\n"
            secrets = "\n• ".join(sorted(self.unknown))
            report += "Unknown secrets in Vault:\n• " + secrets + "\n"
        return report


class SecretsService:
    """Service to manipulate Phalanx secrets.

    Parameters
    ----------
    config_storage
        Storage object for the Phalanx configuration.
    onepassword_storage
        Storage object for 1Password.
    vault_storage
        Storage object for Vault.
    """

    def __init__(
        self,
        config_storage: ConfigStorage,
        onepassword_storage: OnepasswordStorage,
        vault_storage: VaultStorage,
    ) -> None:
        self._config = config_storage
        self._onepassword = onepassword_storage
        self._vault = vault_storage

    def audit(
        self,
        env_name: str,
        exclude: set[str],
        static_secrets: StaticSecrets | None = None,
    ) -> str:
        """Compare existing secrets to configuration and report problems.

        If the Vault path doesn't exist, assume that it hasn't been created
        yet and act as if there are no secrets in Vault. Unfortunately, we
        will also get this behavior if the Vault token doesn't have
        appropriate permissions, since the Vault server returns permission
        denied for unknown paths and there's no way to distinguish.

        Parameters
        ----------
        env_name
            Name of the environment to audit.
        exclude
            Applications to exclude from the audit.
        static_secrets
            User-provided static secrets.

        Returns
        -------
        str
            Audit report as a text document.
        """
        environment = self._config.load_environment(env_name)
        if not static_secrets:
            try:
                static_secrets = self._get_onepassword_secrets(environment)
            except MissingOnepasswordSecretsError as e:
                heading = "Missing static secrets from 1Password:"
                return f"{heading}\n• " + "\n• ".join(e.secrets) + "\n"
        vault_client = self._get_vault_client(environment, static_secrets)
        pull_secret = static_secrets.pull_secret if static_secrets else None

        # Retrieve all the current secrets from Vault and resolve all of the
        # secrets.
        secrets = environment.all_secrets(exclude)
        try:
            vault_secrets = vault_client.get_environment_secrets(exclude)
        except VaultNotFoundError:
            vault_secrets = {}
        try:
            resolved = self._resolve_secrets(
                secrets=secrets,
                environment=environment,
                vault_secrets=vault_secrets,
                static_secrets=static_secrets,
            )
        except UnresolvedSecretsError as e:
            return "Unresolved secrets:\n• " + "\n• ".join(e.secrets) + "\n"

        # Compare the resolved secrets to the Vault data.
        report = self._audit_secrets(
            resolved,
            vault_secrets,
            pull_secret,
            has_static_secrets=bool(static_secrets),
        )

        # Generate the textual report.
        return report.to_text()

    def generate_static_template(self, env_name: str) -> str:
        """Generate a template for providing static secrets.

        The template provides space for all static secrets required for a
        given environment. The resulting file, once the values have been
        added, can be used as input to other secret commands instead of an
        external secret source such as 1Password.

        Parameters
        ----------
        env_name
            Name of the environment.

        Returns
        -------
        dict
            YAML template the user can fill out, as a string.
        """
        environment = self._config.load_environment(env_name)
        warning = ONEPASSWORD_ENCODED_WARNING
        template: defaultdict[str, dict[str, StaticSecret]] = defaultdict(dict)
        for application in environment.all_applications():
            for secret in application.all_static_secrets():
                static_secret = StaticSecret(
                    description=YAMLFoldedString(secret.description),
                    value=None,
                )
                if secret.onepassword.encoded:
                    static_secret.warning = YAMLFoldedString(warning)
                template[secret.application][secret.key] = static_secret
        static_secrets = StaticSecrets(
            applications=template,
            pull_secret=PullSecret(),
            vault_write_token=None,
        )
        return yaml.dump(static_secrets.to_template(), width=70)

    def get_onepassword_static_secrets(self, env_name: str) -> StaticSecrets:
        """Retrieve static secrets for an environment from 1Password.

        Parameters
        ----------
        env_name
            Name of the environment.

        Returns
        -------
        StaticSecrets
            Static secrets for that environment with secret values retrieved
            from 1Password.
        """
        environment = self._config.load_environment(env_name)
        onepassword_secrets = self._get_onepassword_secrets(environment)
        if not onepassword_secrets:
            msg = f"Environment {env_name} not configured to use 1Password"
            raise NoOnepasswordConfigError(msg)
        return onepassword_secrets

    def list_secrets(self, env_name: str) -> list[Secret]:
        """List all required secrets for the given environment.

        Parameters
        ----------
        env_name
            Name of the environment.

        Returns
        -------
        list of Secret
            Secrets required for the given environment.
        """
        environment = self._config.load_environment(env_name)
        return environment.all_secrets()

    def sync(
        self,
        env_name: str,
        exclude: set[str],
        static_secrets: StaticSecrets | None = None,
        *,
        regenerate: bool = False,
        delete: bool = False,
    ) -> None:
        """Synchronize secrets for an environment with Vault.

        Any incorrect secrets will be replaced with the correct value and any
        missing secrets with generate rules will be generated. For generated
        secrets that already have a value in Vault, that value will be kept
        and not replaced.

        If the Vault path doesn't exist, assume that it hasn't been created
        yet and act as if there are no secrets in Vault.

        Parameters
        ----------
        env_name
            Name of the environment.
        exclude
            Applications to exclude from the sync.
        static_secrets
            User-provided static secrets.
        regenerate
            Whether to regenerate any generated secrets.
        delete
            Whether to delete unknown Vault secrets.
        """
        environment = self._config.load_environment(env_name)
        if not static_secrets:
            static_secrets = self._get_onepassword_secrets(environment)
        vault_client = self._get_vault_client(environment, static_secrets)
        secrets = environment.all_secrets(exclude)
        try:
            vault_secrets = vault_client.get_environment_secrets(exclude)
        except VaultNotFoundError:
            vault_secrets = {}

        # Resolve all of the secrets, regenerating if desired.
        resolved = self._resolve_secrets(
            secrets=secrets,
            environment=environment,
            vault_secrets=vault_secrets,
            static_secrets=static_secrets,
            regenerate=regenerate,
        )

        # Replace any Vault secrets that are incorrect. If there are no static
        # secrets, tell _clean_vault_secrets that we have a pull secret to
        # ensure that it doesn't delete any pull secret stored directly in
        # Vault.
        self._sync_application_secrets(vault_client, vault_secrets, resolved)
        has_pull_secret = bool(not static_secrets)
        if resolved.pull_secret and resolved.pull_secret.registries:
            has_pull_secret = True
            pull_secret = resolved.pull_secret
            self._sync_pull_secret(vault_client, vault_secrets, pull_secret)

        # Optionally delete any unrecognized Vault secrets.
        if delete:
            self._clean_vault_secrets(
                vault_client,
                vault_secrets,
                resolved,
                has_pull_secret=has_pull_secret,
            )

    def _audit_secrets(
        self,
        resolved: ResolvedSecrets,
        vault_secrets: dict[str, dict[str, SecretStr]],
        pull_secret: PullSecret | None,
        *,
        has_static_secrets: bool,
    ) -> SecretsAuditReport:
        """Compare resolved secrets with the contents of Vault.

        Parameters
        ----------
        resolved
            Resolved secrets for an environment.
        vault_secrets
            Vault secrets for that environment.
        pull_secret
            Pull secret for the environment, if one is needed.
        has_static_secrets
            Whether static secrets were provided. If no static secrets were
            provided, we should not complain about any pull secret that was
            found, even if we don't have one.

        Returns
        -------
        SecretsAuditReport
            Audit report.
        """
        missing = []
        mismatch = []
        for app_name, values in resolved.applications.items():
            for key, secret in values.items():
                if key not in vault_secrets.get(app_name, {}):
                    missing.append(f"{app_name} {key}")
                    continue
                if secret != vault_secrets[app_name][key]:
                    mismatch.append(f"{app_name} {key}")
                del vault_secrets[app_name][key]
        unknown = [
            f"{a} {k}"
            for a, lv in vault_secrets.items()
            for k in lv
            if a != "pull-secret"
        ]

        # The pull-secret has to be handled separately.
        if pull_secret and pull_secret.registries:
            if "pull-secret" in vault_secrets:
                value = SecretStr(pull_secret.to_dockerconfigjson())
                expected = {".dockerconfigjson": value}
                if expected != vault_secrets["pull-secret"]:
                    mismatch.append("pull-secret")
            else:
                missing.append("pull-secret")
        elif "pull-secret" in vault_secrets and has_static_secrets:
            unknown.append("pull-secret")

        # Return the report.
        return SecretsAuditReport(
            missing=missing, mismatch=mismatch, unknown=unknown
        )

    def _clean_vault_secrets(
        self,
        vault_client: VaultClient,
        vault_secrets: dict[str, dict[str, SecretStr]],
        resolved: ResolvedSecrets,
        *,
        has_pull_secret: bool,
    ) -> None:
        """Delete any unrecognized Vault secrets.

        Parameters
        ----------
        vault_client
            Client for talking to Vault for this environment.
        vault_secrets
            Current secrets in Vault for this environment.
        resolved
            Resolved secrets for this environment.
        has_pull_secret
            Whether there should be a pull secret for this environment.
        """
        for application, values in sorted(vault_secrets.items()):
            if application not in resolved.applications:
                if application == "pull-secret" and has_pull_secret:
                    continue
                print("Deleted Vault secret for", application)
                vault_client.delete_application_secret(application)
                continue
            expected = resolved.applications[application]
            to_delete = set(values.keys()) - set(expected.keys())
            if to_delete:
                for key in to_delete:
                    del values[key]
                vault_client.store_application_secret(application, values)
                for key in sorted(to_delete):
                    print("Deleted Vault secret for", application, key)

    def _decode_base64_secret(
        self, application: str, key: str, value: SecretStr
    ) -> SecretStr:
        """Decode a secret value that was encoded in base64.

        Parameters
        ----------
        application
            Name of the application owning the secret, for error reporting.
        key
            Key of the secret, for error reporting.
        value
            Value of the secret.

        Returns
        -------
        pydantic.SecretStr or None
            Decoded value of the secret.

        Raises
        ------
        MalformedOnepasswordSecretError
            Raised if the secret could not be decoded.
        """
        try:
            secret = value.get_secret_value()
            return SecretStr(b64decode(secret.encode()).decode())
        except (binascii.Error, UnicodeDecodeError) as e:
            msg = "value could not be base64-decoded to a valid secret string"
            raise MalformedOnepasswordSecretError(application, key, msg) from e

    def _get_onepassword_secrets(
        self, environment: Environment
    ) -> StaticSecrets | None:
        """Get static secrets for an environment from 1Password.

        Parameters
        ----------
        environment
            Environment for which to get static secrets.

        Returns
        -------
        dict of StaticSecret or None
            Static secrets for this environment retrieved from 1Password, or
            `None` if this environment doesn't use 1Password.

        Raises
        ------
        MalformedOnepasswordSecretError
            Raised if the secret could not be decoded.
        MissingOnepasswordSecretsError
            Raised if any of the items or fields expected to be in 1Password
            are not present.
        NoOnepasswordCredentialsError
            Raised if the environment uses 1Password but no 1Password
            credentials were available in the environment.
        """
        if not environment.onepassword:
            return None
        onepassword = self._onepassword.get_onepassword_client(environment)
        query = {}
        encoded = {}
        for application in environment.all_applications():
            static_secrets = application.all_static_secrets()
            if not static_secrets:
                continue
            query[application.name] = [s.key for s in static_secrets]
            encoded[application.name] = {
                s.key for s in static_secrets if s.onepassword.encoded
            }
        result = onepassword.get_secrets(query)

        # Fix any secrets that were encoded in base64 in 1Password.
        for app_name, secrets in encoded.items():
            for key in secrets:
                secret = result.applications[app_name][key]
                if secret.value:
                    secret.value = self._decode_base64_secret(
                        app_name, key, secret.value
                    )
        return result

    def _get_vault_client(
        self,
        environment: EnvironmentBaseConfig,
        static_secrets: StaticSecrets | None,
    ) -> VaultClient:
        """Get a Vault client for the given environment.

        Parameters
        ----------
        environment
            Environment configuration.
        static_secrets
            Static secrets for this environment.

        Returns
        -------
        VaultClient
            Vault client configured for that environment.

        Raises
        ------
        NoVaultCredentialsError
            Raised if VAULT_TOKEN is not set in the environment and the Vault
            write token could not be retrieved from the static secrets.
        """
        credentials = None
        if not os.getenv("VAULT_TOKEN"):
            if static_secrets and static_secrets.vault_write_token:
                token = static_secrets.vault_write_token.get_secret_value()
                credentials = VaultTokenCredentials(token=token)
            else:
                raise NoVaultCredentialsError
        return self._vault.get_vault_client(
            environment, credentials=credentials
        )

    def _resolve_secrets(
        self,
        *,
        secrets: list[Secret],
        environment: Environment,
        vault_secrets: dict[str, dict[str, SecretStr]],
        static_secrets: StaticSecrets | None = None,
        regenerate: bool = False,
    ) -> ResolvedSecrets:
        """Resolve the secrets for a Phalanx environment.

        Resolving secrets is the process where the secret configuration is
        resolved using per-environment Helm chart values to generate the list
        of secrets required for a given environment and their values.

        Parameters
        ----------
        secrets
            Secret configuration by application and key.
        environment
            Phalanx environment for which to resolve secrets.
        vault_secrets
            Current values from Vault. These will be used if compatible with
            the secret definitions.
        static_secrets
            User-provided static secrets.
        regenerate
            Whether to regenerate any generated secrets.

        Returns
        -------
        ResolvedSecrets
            Resolved secrets.

        Raises
        ------
        UnresolvedSecretsError
            Raised if some secrets could not be resolved.
        """
        if not static_secrets:
            static_secrets = StaticSecrets()
        resolved: defaultdict[str, dict[str, SecretStr]] = defaultdict(dict)
        unresolved = list(secrets)
        left = len(unresolved)
        while unresolved:
            secrets = unresolved
            unresolved = []
            for config in secrets:
                app_name = config.application
                vault_values = vault_secrets.get(app_name, {})
                static_values = static_secrets.for_application(app_name)
                static_value = None
                if config.key in static_values:
                    static_value = static_values[config.key].value
                secret = self._resolve_secret(
                    config=config,
                    resolved=resolved,
                    current_value=vault_values.get(config.key),
                    static_value=static_value,
                    regenerate=regenerate,
                )
                if secret:
                    resolved[config.application][config.key] = secret
                else:
                    unresolved.append(config)
            if len(unresolved) >= left:
                raise UnresolvedSecretsError(unresolved)
            left = len(unresolved)
        return ResolvedSecrets(
            applications=resolved, pull_secret=static_secrets.pull_secret
        )

    def _resolve_secret(
        self,
        *,
        config: Secret,
        resolved: dict[str, dict[str, SecretStr]],
        current_value: SecretStr | None,
        static_value: SecretStr | None,
        regenerate: bool = False,
    ) -> SecretStr | None:
        """Resolve a single secret.

        Parameters
        ----------
        config
            Configuration of the secret.
        resolved
            Other secrets for that environment that have already been
            resolved.
        current_value
            Current secret value in Vault, if known.
        static_value
            User-provided static secret value, if any.
        regenerate
            Whether to regenerate any generated secrets.

        Returns
        -------
        SecretStr or None
            Resolved value of the secret, or `None` if the secret cannot yet
            be resolved (because, for example, the secret from which it is
            copied has not yet been resolved).
        """
        value = None

        # See if the value comes from configuration, either hard-coded or via
        # copy or generate rules. If not, it must be a static secret, in which
        # case use the value from a static secret source, if available. If
        # none is available from a static secret source but we have a current
        # value, use that. Only fail if there is no static secret source and
        # no current value.
        if config.value:
            value = config.value
        elif config.copy_rules:
            application = config.copy_rules.application
            other = resolved.get(application, {}).get(config.copy_rules.key)
            if not other:
                return None
            value = other
        elif config.generate:
            if current_value and not regenerate:
                value = current_value
            elif isinstance(config.generate, SourceSecretGenerateRules):
                other_key = config.generate.source
                other = resolved.get(config.application, {}).get(other_key)
                if not other:
                    return None
                value = config.generate.generate(other)
            else:
                value = config.generate.generate()
        else:
            value = static_value or current_value

        # Return the resolved secret.
        return value

    def _sync_application_secrets(
        self,
        vault_client: VaultClient,
        vault_secrets: dict[str, dict[str, SecretStr]],
        resolved: ResolvedSecrets,
    ) -> None:
        """Sync the application secrets for an environment to Vault.

        Changes made to Vault will be reported to standard output. This will
        not delete any stray secrets in Vault, only add any missing ones.

        Parameters
        ----------
        vault_client
            Client for talking to Vault for this environment.
        vault_secrets
            Current secrets in Vault for this environment.
        resolved
            Resolved secrets for this environment.
        """
        for application, values in resolved.applications.items():
            if application not in vault_secrets:
                vault_client.store_application_secret(application, values)
                print("Created Vault secret for", application)
                continue
            vault_app_secrets = vault_secrets[application]
            for key, secret in values.items():
                if secret != vault_app_secrets.get(key):
                    vault_client.update_application_secret(
                        application, key, secret
                    )
                    print("Updated Vault secret for", application, key)

    def _sync_pull_secret(
        self,
        vault_client: VaultClient,
        vault_secrets: dict[str, dict[str, SecretStr]],
        pull_secret: PullSecret,
    ) -> None:
        """Sync the pull secret for an environment to Vault.

        Parameters
        ----------
        vault_client
            Client for talking to Vault for this environment.
        vault_secrets
            Current secrets in Vault for this environment.
        pull_secret
            Pull secret for the environment.
        """
        value = SecretStr(pull_secret.to_dockerconfigjson())
        secret = {".dockerconfigjson": value}
        if "pull-secret" not in vault_secrets:
            vault_client.store_application_secret("pull-secret", secret)
            print("Created Vault secret for pull-secret")
        elif secret != vault_secrets["pull-secret"]:
            vault_client.store_application_secret("pull-secret", secret)
            print("Updated Vault secret for pull-secret")
