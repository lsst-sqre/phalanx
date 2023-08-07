"""Service to manage Vault authentication."""

from __future__ import annotations

import jinja2
from safir.datetime import current_datetime, format_datetime_for_logging

from ..constants import VAULT_WRITE_TOKEN_WARNING_LIFETIME
from ..models.environments import EnvironmentConfig
from ..models.vault import VaultAppRole, VaultToken, VaultTokenMetadata
from ..storage.config import ConfigStorage
from ..storage.vault import VaultClient, VaultStorage

__all__ = ["VaultService"]


class VaultService:
    """Service to manage Vault authentication.

    Parameters
    ----------
    config_storage
        Storage object for the Phalanx configuration.
    vault_storage
        Storage object for Vault.
    """

    def __init__(
        self, config_storage: ConfigStorage, vault_storage: VaultStorage
    ) -> None:
        self._config = config_storage
        self._vault = vault_storage
        self._templates = jinja2.Environment(
            loader=jinja2.PackageLoader("phalanx", "data"),
            undefined=jinja2.StrictUndefined,
            autoescape=jinja2.select_autoescape(disabled_extensions=["tmpl"]),
        )

    def audit(self, environment: str) -> str:
        """Audit the Vault authentication configuration for an environment.

        Parameters
        ----------
        environment
            Name of the environment.

        Returns
        -------
        str
            Human-readable text report of any problems found.
        """
        config = self._config.load_environment_config(environment)
        vault_client = self._vault.get_vault_client(config)
        report = ""
        result = self._audit_read_approle(vault_client, config)
        if result:
            report += result
        result = self._audit_write_token(vault_client, config)
        if result:
            report += result
        return report

    def create_read_approle(self, environment: str) -> VaultAppRole:
        """Create a new Vault read AppRole for the given environment.

        This will create (or update) a read policy whose name is the Vault
        secrets path with the first component (the mount) removed and
        ``/read`` appended, and an AppRole, whose name will be the last
        component of the Vault secrets path.

        Conventionally, the Vault secrets path will be :samp:`phalanx/{fqdn}`
        where the last component is the FQDN of the deployed Phalanx
        environment, so the policy name will be :samp:`phalanx/{fqdn}/read`
        and the AppRole name will be :samp:`{fqdn}`.

        Parameters
        ----------
        environment
            Name of the environment.

        Returns
        -------
        VaultAppRole
            Newly-created Vault AppRole.
        """
        config = self._config.load_environment_config(environment)
        vault_client = self._vault.get_vault_client(config)
        template = self._templates.get_template("vault-read-policy.tmpl")
        policy = template.render({"path": config.vault_path})
        vault_client.create_policy(config.vault_read_policy, policy)
        return vault_client.create_approle(
            config.vault_read_approle, [config.vault_read_policy]
        )

    def create_write_token(
        self, environment: str, lifetime: str
    ) -> VaultToken:
        """Create a new Vault write token for the given environment.

        This will create (or update) a read policy whose name is the Vault
        secrets path with the first component (the mount) removed and
        ``/write`` appended

        Parameters
        ----------
        environment
            Name of the environment.
        lifetime
            Token lifetime in Vault duration format.

        Returns
        -------
        VaultToken
            Newly-created Vault token.
        """
        config = self._config.load_environment_config(environment)
        vault_client = self._vault.get_vault_client(config)
        template = self._templates.get_template("vault-write-policy.tmpl")
        policy = template.render({"path": config.vault_path})
        vault_client.create_policy(config.vault_write_policy, policy)
        return vault_client.create_token(
            config.vault_write_token, [config.vault_write_policy], lifetime
        )

    def _audit_read_approle(
        self, vault_client: VaultClient, config: EnvironmentConfig
    ) -> str | None:
        """Audit a read approle for any errors.

        Parameters
        ----------
        vault_client
            Vault client.
        config
            Phalanx configuration for the relevant environment.

        Returns
        -------
        str or None
            Human-readable report of any errors, or `None` if no errors were
            found.
        """
        approle = vault_client.get_approle(config.vault_read_approle)
        if not approle:
            return f"No read AppRole ({config.vault_read_approle})\n"

        expected_policies = {config.vault_read_policy}
        errors = self._audit_policies(approle.policies, expected_policies)
        template = self._templates.get_template("vault-read-policy.tmpl")
        expected = template.render({"path": config.vault_path})
        policy = vault_client.get_policy(config.vault_read_policy)
        if policy != expected:
            name = config.vault_read_policy
            errors.append(f"Policy {name} doesn't have expected contents")

        if errors:
            items = "\n• ".join(errors)
            name = config.vault_read_approle
            return f"Problems with read AppRole ({name}):\n• " + items + "\n"
        else:
            return None

    def _audit_write_token(
        self, vault_client: VaultClient, config: EnvironmentConfig
    ) -> str | None:
        """Audit a write token for any errors.

        Parameters
        ----------
        vault_client
            Vault client.
        config
            Phalanx configuration for the relevant environment.

        Returns
        -------
        str or None
            Human-readable report of any errors, or `None` if no errors were
            found.
        """
        tokens = self._find_write_tokens(vault_client, config)
        if not tokens:
            return f"No write token ({config.vault_write_token})\n"
        report = ""
        if len(tokens) > 1:
            report = "Multiple write tokens found\n"

        template = self._templates.get_template("vault-write-policy.tmpl")
        expected = template.render({"path": config.vault_path})
        policy = vault_client.get_policy(config.vault_write_policy)

        now = current_datetime()
        policies = {config.vault_write_policy}
        for token in tokens:
            errors = []
            if token.expires < now:
                expiration = format_datetime_for_logging(token.expires)
                errors.append(f"Token expired at {expiration}")
            elif token.expires < now + VAULT_WRITE_TOKEN_WARNING_LIFETIME:
                expiration = format_datetime_for_logging(token.expires)
                errors.append(f"Token will expire at {expiration}")
            errors.extend(self._audit_policies(token.policies, policies))
            if policy != expected:
                name = config.vault_write_policy
                errors.append(f"Policy {name} doesn't have expected contents")

            if errors:
                items = "\n• ".join(errors)
                summary = f"Problems with write token ({token.display_name})"
                report += f"{summary}:\n• " + items + "\n"

        return report

    def _audit_policies(
        self, policies: list[str], expected: set[str]
    ) -> list[str]:
        """Audit policies against an expected set.

        Parameters
        ----------
        policies
            Policies attached to an AppRole or token.
        expected
            Expected set of policies, without ``default``.

        Returns
        -------
        list of str
            Any errors found, or the empty list if none were found.
        """
        found = set(policies)
        errors = [f"Missing policy {p}" for p in expected if p not in found]
        found -= expected | {"default"}
        errors.extend([f"Unexpected policy {p}" for p in found])
        return errors

    def _find_write_tokens(
        self, vault_client: VaultClient, config: EnvironmentConfig
    ) -> list[VaultTokenMetadata]:
        """Find the write token for a given environment.

        The write token is located by iterating through all token accessors
        and finding all tokens whose display name match the expected display
        name of the write token for that environment.

        Parameters
        ----------
        vault_client
            Vault client.
        config
            Phalanx configuration for the environment.

        Returns
        -------
        list of VaultTokenMetadata
            List of tokens with the appropriate write policy.
        """
        accessors = vault_client.list_token_accessors()
        tokens = []
        for accessor in accessors:
            token = vault_client.get_token(accessor)
            if token and token.display_name == config.vault_write_token:
                tokens.append(token)
        return tokens
