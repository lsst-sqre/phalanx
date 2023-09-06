"""Retrieve secrets stored in 1Password via 1Password Connect."""

from __future__ import annotations

import os
from collections import defaultdict

from onepasswordconnectsdk import load_dict, new_client
from onepasswordconnectsdk.client import FailedToRetrieveItemException

from ..exceptions import NoOnepasswordCredentialsError
from ..models.environments import EnvironmentBaseConfig
from ..models.secrets import StaticSecret, StaticSecrets

__all__ = ["OnepasswordClient", "OnepasswordStorage"]


class OnepasswordClient:
    """Retrieve secrets stored in 1Password via 1Password Connect.

    This client is specific to a particular Phalanx environment. It is created
    using the metadata of a Phalanx environment by `OnepasswordStorage`.

    The 1Password Connect authentication token is taken from the
    ``OP_CONNECT_TOKEN`` environment variable, which must be set.

    Parameters
    ----------
    url
        URL of the 1Password Connect server.
    vault_title
        Title of vault within that 1Password Connect server from which to
        retrieve secrets.
    """

    def __init__(self, url: str, vault_title: str) -> None:
        token = os.getenv("OP_CONNECT_TOKEN")
        if not token:
            raise NoOnepasswordCredentialsError
        self._onepassword = new_client(url, token)
        self._vault_id = self._onepassword.get_vault_by_title(vault_title).id

    def get_secrets(self, query: dict[str, list[str]]) -> StaticSecrets:
        """Get static secrets for an environment from 1Password.

        Parameters
        ----------
        query
            Query for secrets in the form of a dictionary of applications to
            lists of secret keys for that application that should be
            retrieved.

        Returns
        -------
        dict of dict
            Retrieved static secrets as a dictionary of applications to secret
            keys to `~phalanx.models.secrets.StaticSecret` objects.
        """
        request: dict[tuple[str, str], dict[str, str]] = {}
        extra = []
        for application, secrets in query.items():
            for secret in secrets:
                if "." in secret:
                    extra.append((application, secret))
                else:
                    request[(application, secret)] = {
                        "opitem": application,
                        "opfield": f".{secret}",
                        "opvault": self._vault_id,
                    }
        response = load_dict(self._onepassword, request)
        result: StaticSecrets = defaultdict(dict)
        for key, value in response.items():
            application, secret = key
            result[application][secret] = StaticSecret(value=value)

        # Separately handle the secret field names that contain periods, since
        # that conflicts with the syntax used by load_dict.
        for application, secret in extra:
            item = self._onepassword.get_item(application, self._vault_id)
            found = False
            for field in item.fields:
                if field.label == secret:
                    static_secret = StaticSecret(value=field.value)
                    result[application][secret] = static_secret
                    found = True
                    break
            if not found:
                msg = f"Item {application} has no field {secret}"
                raise FailedToRetrieveItemException(msg)

        return result


class OnepasswordStorage:
    """Create 1Password Connect clients for specific environments."""

    def get_onepassword_client(
        self, env: EnvironmentBaseConfig
    ) -> OnepasswordClient:
        """Return a 1Password client configured for the given environment.

        Parameters
        ----------
        env
            Phalanx environment.

        Returns
        -------
        OnepasswordClient
            1Password Connect client configured for that environment.

        Raises
        ------
        ValueError
            Raised if this environment is not configured to use 1Password.
        """
        if not env.onepassword:
            raise ValueError(f"{env.name} does not use 1Password")
        return OnepasswordClient(
            str(env.onepassword.connect_url), env.onepassword.vault_title
        )
