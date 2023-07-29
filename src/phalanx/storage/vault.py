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
            Mapping from secret key to its Vault from vault.
        """
        path = f"{self._path}/{application}"
        r = self._vault.secrets.kv.read_secret(
            path=path, raise_on_deleted_version=True
        )
        return {k: SecretStr(v) for k, v in r["data"]["data"].items()}


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
