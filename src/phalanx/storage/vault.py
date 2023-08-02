"""Store, retrieve, and manipulate data stored in Vault."""

from __future__ import annotations

import hvac
from hvac.exceptions import InvalidPath
from pydantic import SecretStr

from ..exceptions import VaultNotFoundError
from ..models.environments import Environment

__all__ = ["VaultClient", "VaultStorage"]


class VaultClient:
    """Store, retrieve, and manipulate data stored in Vault.

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
        mount, path = path.split("/", 1)
        self._vault = hvac.Client(url)
        self._vault.secrets.kv.default_kv_version = 2
        self._url = url
        self._path = path

    def get_application_secrets(
        self, application: str
    ) -> dict[str, SecretStr]:
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

    def get_environment_secrets(
        self, environment: Environment
    ) -> dict[str, dict[str, SecretStr]]:
        """Get the secrets for an environment currently stored in Vault.

        Parameters
        ----------
        environment
            Name of the environment.

        Returns
        -------
        dict of dict
            Mapping from application to secret key to its secret from Vault.
        """
        vault_secrets = {}
        for application in environment.all_applications():
            try:
                vault_secret = self.get_application_secrets(application.name)
                vault_secrets[application.name] = vault_secret
            except VaultNotFoundError:
                pass
        return vault_secrets

    def store_application_secrets(
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

    def update_secret(
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

    def get_vault_client(self, env: Environment) -> VaultClient:
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
