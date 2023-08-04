"""Store, retrieve, and manipulate data stored in Vault."""

from __future__ import annotations

from contextlib import suppress

import hvac
from hvac.exceptions import InvalidPath
from pydantic import SecretStr

from ..exceptions import VaultNotFoundError
from ..models.environments import EnvironmentVaultConfig
from ..models.vault import VaultAppRole, VaultToken

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

    def create_token(self, policies: list[str], lifetime: str) -> VaultToken:
        """Create a new Vault token.

        Parameters
        ----------
        policies
            Policies to assign to that token.
        lifetime
            Lifetime of the token as a Vault duration string.

        Returns
        -------
        VaultToken
            Newly-created Vault token.
        """
        token = self._vault.auth.token.create(policies=policies, ttl=lifetime)
        return VaultToken(
            token=token["auth"]["client_token"],
            accessor=token["auth"]["accessor"],
            policies=token["auth"]["token_policies"],
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
        dict of pydantic.SecretStr
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

    def list_application_secrets(self) -> list[str]:
        """List the available application secrets in Vault.

        Returns
        -------
        list of str
            Names of available application secrets.
        """
        try:
            r = self._vault.secrets.kv.list_secrets(self._path)
        except InvalidPath as e:
            raise VaultNotFoundError(self._url, self._path) from e
        return r["data"]["keys"]

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

    def get_vault_client(self, env: EnvironmentVaultConfig) -> VaultClient:
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
