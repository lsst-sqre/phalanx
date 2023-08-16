"""Service to manage Vault tokens and policies."""

from __future__ import annotations

import jinja2

from ..models.vault import VaultAppRole, VaultToken
from ..storage.config import ConfigStorage
from ..storage.vault import VaultStorage

__all__ = ["VaultService"]


class VaultService:
    """Service to manage Vault tokens and policies.

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
        environment_config = self._config.load_environment_config(environment)
        vault_client = self._vault.get_vault_client(environment_config)

        # The first component of the Vault secrets path is the mount. The rest
        # is the path in Vault to the secrets, which we will also use for the
        # policy name. AppRole names cannot contain /, so we'll use only the
        # final component of the path for the AppRole name.
        _, vault_path = environment_config.vault_path_prefix.split("/", 1)
        policy_name = f"{vault_path}/read"
        if "/" in vault_path:
            _, approle_name = vault_path.rsplit("/", 1)
        else:
            approle_name = vault_path

        template = self._templates.get_template("vault-read-policy.tmpl")
        policy = template.render({"path": vault_path})
        vault_client.create_policy(policy_name, policy)
        return vault_client.create_approle(approle_name, [policy_name])

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
        environment_config = self._config.load_environment_config(environment)
        vault_client = self._vault.get_vault_client(environment_config)

        # The first component of the Vault secrets path is the mount. The rest
        # is the path in Vault to the secrets, which we will also use for the
        # policy name.
        _, vault_path = environment_config.vault_path_prefix.split("/", 1)
        policy_name = f"{vault_path}/write"

        template = self._templates.get_template("vault-write-policy.tmpl")
        policy = template.render({"path": vault_path})
        vault_client.create_policy(policy_name, policy)
        return vault_client.create_token([policy_name], lifetime)
