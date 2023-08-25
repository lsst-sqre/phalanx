"""Store, retrieve, and manipulate data stored in Vault."""

from __future__ import annotations

from contextlib import suppress

import hvac
from hvac.exceptions import InvalidPath
from pydantic import SecretStr

from ..exceptions import VaultNotFoundError
from ..models.environments import EnvironmentBaseConfig
from ..models.vault import (
    VaultAppRole,
    VaultAppRoleMetadata,
    VaultToken,
    VaultTokenMetadata,
)

__all__ = ["VaultClient", "VaultStorage"]


class VaultClient:
    """Store, retrieve, and manipulate data stored in Vault.

    This client is specific to a particular Phalanx environment. It is
    created using the metadata of a Phalanx environment by `VaultStorage`.

    The Vault authentication token is taken from either the ``VAULT_TOKEN``
    environment variable or a :file:`.vault-token` file in the user's home
    directory.

    Parameters
    ----------
    url
        URL of the Vault server.
    path
        Path within that Vault server where secrets for an environment are
        stored.
    """

    def __init__(self, url: str, path: str) -> None:
        self._url = url
        _, self._path = path.split("/", 1)
        self._vault = hvac.Client(url)
        self._vault.secrets.kv.default_kv_version = 2

    def create_policy(self, name: str, policy: str) -> None:
        """Create a policy allowing read of secrets for this environment.

        Parameters
        ----------
        name
            Name of policy to create.
        policy
            Text of the policy.
        """
        self._vault.sys.create_or_update_policy(name, policy)

    def create_approle(self, name: str, policies: list[str]) -> VaultAppRole:
        """Create a new Vault AppRole for secret access.

        Parameters
        ----------
        name
            Name of the AppRole to create.
        policies
            Policies to assign to that AppRole.

        Returns
        -------
        VaultAppRole
            Newly-created AppRole.
        """
        self._vault.auth.approle.create_or_update_approle(
            role_name=name,
            token_policies=policies,
            token_type="service",
        )
        r = self._vault.auth.approle.read_role_id(name)
        role_id = r["data"]["role_id"]
        r = self._vault.auth.approle.generate_secret_id(name)
        secret_id = r["data"]["secret_id"]
        secret_id_accessor = r["data"]["secret_id_accessor"]
        r = self._vault.auth.approle.read_role(name)
        token_policies = r["data"]["token_policies"]
        return VaultAppRole(
            role_id=role_id,
            secret_id=secret_id,
            secret_id_accessor=secret_id_accessor,
            policies=token_policies,
        )

    def create_token(
        self, display_name: str, policies: list[str], lifetime: str
    ) -> VaultToken:
        """Create a new Vault token.

        Parameters
        ----------
        display_name
            Display name of the token.
        policies
            Policies to assign to that token.
        lifetime
            Lifetime of the token as a Vault duration string.

        Returns
        -------
        VaultToken
            Newly-created Vault token.
        """
        token = self._vault.auth.token.create(
            display_name=display_name, policies=policies, ttl=lifetime
        )
        accessor = token["auth"]["accessor"]
        r = self._vault.auth.token.lookup_accessor(accessor)
        return VaultToken(
            display_name=r["data"]["display_name"],
            token=token["auth"]["client_token"],
            accessor=accessor,
            policies=token["auth"]["token_policies"],
            expires=r["data"]["expire_time"],
        )

    def delete_application_secret(self, application: str) -> None:
        """Delete the secrets for an application currently stored in Vault.

        If the secret does not exist, still returns success without raising an
        exception.

        Parameters
        ----------
        application
            Name of the application.
        """
        path = f"{self._path}/{application}"
        with suppress(InvalidPath):
            self._vault.secrets.kv.delete_latest_version_of_secret(path)

    def get_application_secret(self, application: str) -> dict[str, SecretStr]:
        """Get the secrets for an application currently stored in Vault.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        dict of pydantic.types.SecretStr
            Mapping from secret key to its secret from Vault.

        Raises
        ------
        VaultNotFoundError
            Raised if the requested secret was not found in Vault.
        """
        path = f"{self._path}/{application}"
        try:
            r = self._vault.secrets.kv.read_secret(
                path, raise_on_deleted_version=True
            )
        except InvalidPath as e:
            raise VaultNotFoundError(self._url, path) from e
        return {k: SecretStr(v) for k, v in r["data"]["data"].items()}

    def get_approle(self, name: str) -> VaultAppRoleMetadata | None:
        """Retrieve metadata about a Vault AppRole if it exists.

        Parameters
        ----------
        approle
            Name of the AppRole.

        Returns
        -------
        VaultAppRoleMetadata or None
            Metadata about the AppRole if it exists, else `None`.
        """
        try:
            r = self._vault.auth.approle.read_role_id(name)
            role_id = r["data"]["role_id"]
            r = self._vault.auth.approle.read_role(name)
        except InvalidPath:
            return None
        return VaultAppRoleMetadata(
            role_id=role_id, policies=r["data"]["token_policies"]
        )

    def get_environment_secrets(self) -> dict[str, dict[str, SecretStr]]:
        """Get the secrets for an environment currently stored in Vault.

        Returns
        -------
        dict of dict
            Mapping from application to secret key to its secret from Vault.
        """
        vault_secrets = {}
        for application in self.list_application_secrets():
            with suppress(VaultNotFoundError):
                vault_secret = self.get_application_secret(application)
                vault_secrets[application] = vault_secret
        return vault_secrets

    def get_policy(self, name: str) -> str | None:
        """Get the contents of a Vault policy.

        Parameters
        ----------
        name
            Name of the policy.

        Returns
        -------
        str or None
            Text of the policy, or `None` if it does not exist.
        """
        try:
            r = self._vault.sys.read_policy(name)
        except InvalidPath:
            return None
        return r["rules"]

    def get_token(self, accessor: str) -> VaultTokenMetadata | None:
        """Get a token by accessor.

        Parameters
        ----------
        accessor
            Accessor for the token.

        Returns
        -------
        VaultTokenMetadata or None
            Metadata for the token, or `None` if no token exists with that
            accessor.
        """
        try:
            r = self._vault.auth.token.lookup_accessor(accessor)
        except InvalidPath:
            return None
        return VaultTokenMetadata(
            display_name=r["data"]["display_name"],
            accessor=accessor,
            expires=r["data"]["expire_time"],
            policies=r["data"]["policies"],
        )

    def list_application_secrets(self) -> list[str]:
        """List the available application secrets in Vault.

        Returns
        -------
        list of str
            Names of available application secrets.

        Raises
        ------
        VaultNotFoundError
            Raised if the path for application secrets does not exist.
        """
        try:
            r = self._vault.secrets.kv.list_secrets(self._path)
        except InvalidPath as e:
            raise VaultNotFoundError(self._url, self._path) from e
        return r["data"]["keys"]

    def list_token_accessors(self) -> list[str]:
        """List the accessors of all known tokens.

        Returns
        -------
        list of str
            Accessors for all known tokens.
        """
        r = self._vault.auth.token.list_accessors()
        return r["data"]["keys"]

    def revoke_approle_secret_ids(self, name: str) -> None:
        """Revoke all existing SecretIDs for a Vault AppRole.

        Parameters
        ----------
        name
            Name of the AppRole.
        """
        r = self._vault.auth.approle.list_secret_id_accessors(name)
        for accessor in r["data"]["keys"]:
            self._vault.auth.approle.destroy_secret_id_accessor(name, accessor)

    def revoke_token(self, accessor: str) -> None:
        """Revoke a token by accessor.

        Parameters
        ----------
        accessor
            Accessor of token.
        """
        self._vault.auth.token.revoke_accessor(accessor)

    def store_application_secret(
        self, application: str, values: dict[str, SecretStr]
    ) -> None:
        """Store the full set of secrets for an application.

        Parameters
        ----------
        application
            Name of the application.
        values
            Secret key and value pairs.
        """
        path = f"{self._path}/{application}"
        secret = {k: v.get_secret_value() for k, v in values.items()}
        self._vault.secrets.kv.create_or_update_secret(path, secret)

    def update_application_secret(
        self, application: str, key: str, value: SecretStr
    ) -> None:
        """Update the value of a specific secret key.

        Parameters
        ----------
        application
            Name of the application.
        key
            Key within that application's secret to update.
        value
            New value for that secret key.
        """
        path = f"{self._path}/{application}"
        self._vault.secrets.kv.patch(path, {key: value.get_secret_value()})


class VaultStorage:
    """Create Vault clients for specific environments."""

    def get_vault_client(self, env: EnvironmentBaseConfig) -> VaultClient:
        """Return a Vault client configured for the given environment.

        Parameters
        ----------
        env
            Phalanx environment.

        Returns
        -------
        VaultClient
            Vault client configured to manage secrets for that environment.
        """
        return VaultClient(env.vault_url, env.vault_path_prefix)
