"""Store, retrieve, and manipulate data stored in Vault."""

from __future__ import annotations

import hvac
from pydantic import SecretStr

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
        """
        path = f"{self._path}/{application}"
        r = self._vault.secrets.kv.read_secret(
            path=path, raise_on_deleted_version=True
        )
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
            vault_secret = self.get_application_secrets(application.name)
            vault_secrets[application.name] = vault_secret
        return vault_secrets


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
