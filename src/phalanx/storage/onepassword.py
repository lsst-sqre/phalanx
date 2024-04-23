"""Retrieve secrets stored in 1Password via 1Password Connect."""

from __future__ import annotations

import os
from collections import defaultdict

from onepasswordconnectsdk import new_client
from onepasswordconnectsdk.client import FailedToRetrieveItemException
from pydantic import SecretStr

from ..exceptions import (
    MissingOnepasswordSecretsError,
    NoOnepasswordCredentialsError,
)
from ..models.environments import EnvironmentBaseConfig
from ..models.secrets import PullSecret, StaticSecret, StaticSecrets

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

        Raises
        ------
        MissingOnepasswordSecretsError
            Raised if any of the items or fields expected to be in 1Password
            are not present.
        """
        applications: defaultdict[str, dict[str, StaticSecret]]
        applications = defaultdict(dict)

        # This method originally used the load_dict bulk query interface, but
        # the onepasswordconnectsdk Python library appears to turn that into
        # separate queries per item anyway, it can't handle fields whose names
        # contain periods, and it means we don't know what items are missing
        # for error reporting. It seems better to do the work directly.
        not_found = []
        for application, secrets in query.items():
            try:
                item = self._onepassword.get_item(application, self._vault_id)
            except FailedToRetrieveItemException:
                not_found.append(application)
                continue
            for secret in secrets:
                found = False
                for field in item.fields:
                    if field.label == secret:
                        static_secret = StaticSecret(value=field.value)
                        applications[application][secret] = static_secret
                        found = True
                        break
                if not found:
                    not_found.append(f"{application} {secret}")

        # If any secrets weren't found, raise an exception with the list of
        # secrets that weren't found.
        if not_found:
            raise MissingOnepasswordSecretsError(not_found)

        # Return the static secrets.
        return StaticSecrets(
            applications=applications,
            pull_secret=self._get_pull_secret(),
            vault_write_token=self._get_vault_write_token(),
        )

    def _get_pull_secret(self) -> PullSecret | None:
        """Get the pull secret for an environment from 1Password.

        Returns
        -------
        dict of StaticSecret or None
            The constructed pull secret in a form suitable for adding to
            Vault, or `None` if there is no pull secret for this environment.
        """
        try:
            item = self._onepassword.get_item("pull-secret", self._vault_id)
        except FailedToRetrieveItemException:
            return None

        # Extract the usernames and passwords from the 1Password item.
        secrets: defaultdict[str, dict[str, str]] = defaultdict(dict)
        section = {s.id: s.label for s in item.sections}
        for field in item.fields:
            if field.label not in ("username", "password"):
                continue
            section_id = field.section.id if field.section else None
            registry = section[section_id]
            if field.label == "username":
                secrets[registry]["username"] = field.value
            elif field.label == "password":
                secrets[registry]["password"] = field.value

        # Return the result converted to the appropriate model.
        return PullSecret.model_validate({"registries": secrets})

    def _get_vault_write_token(self) -> SecretStr | None:
        """Get the Vault write token for an environment from 1Password.

        Returns
        -------
        SecretStr or None
            Vault write token for the configured environment, or `None` if
            it isn't present in 1Password.
        """
        try:
            item = self._onepassword.get_item(
                "vault-write-token", self._vault_id
            )
        except FailedToRetrieveItemException:
            return None
        for field in item.fields:
            if field.label == "vault-token":
                return SecretStr(field.value)
        return None


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
