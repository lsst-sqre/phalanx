"""Mock 1Password Connect API for testing."""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator
from unittest.mock import patch

import yaml
from onepasswordconnectsdk.client import (
    FailedToRetrieveItemException,
    FailedToRetrieveVaultException,
)
from onepasswordconnectsdk.models import (
    Field,
    FieldSection,
    Item,
    Section,
    Vault,
)

from phalanx.models.secrets import StaticSecrets

from .data import phalanx_test_path

__all__ = [
    "MockOnepasswordClient",
    "patch_onepassword",
]


class MockOnepasswordClient:
    """Mock 1Password Connect client for testing."""

    def __init__(self) -> None:
        self._data: dict[str, dict[str, Item]] = {}
        self._uuids: dict[str, str] = {}

    def create_empty_test_vault(self, vault: str) -> None:
        """Create an empty 1Password vault for testing.

        This method is not part of the 1Password Connect API. It is intended
        for use by the test suite to set up a test.

        Parameters
        ----------
        vault
            Name of the 1Password vault.
        """
        self._data[vault] = {}

    def load_test_data(self, vault: str, environment: str) -> None:
        """Load 1Password test data for the given environment.

        This method is not part of the 1Password Connect API. It is intended
        for use by the test suite to set up a test.

        Parameters
        ----------
        vault
            Name of the 1Password vault.
        environment
            Name of the environment for which to load 1Password test data.
        """
        data_path = phalanx_test_path() / "onepassword" / f"{environment}.yaml"
        with data_path.open() as fh:
            secrets = StaticSecrets.model_validate(yaml.safe_load(fh))
        self._data[vault] = {}
        for title, values in secrets.applications.items():
            fields = [Field(label=k, value=v.value) for k, v in values.items()]
            self._data[vault][title] = Item(title=title, fields=fields)
        if secrets.pull_secret and secrets.pull_secret.registries:
            fields = []
            sections = []
            for registry, auth in secrets.pull_secret.registries.items():
                sections.append(Section(id=registry, label=registry))
                reference = FieldSection(id=registry)
                fields.extend(
                    Field(label=k, value=v, section=reference)
                    for k, v in auth.model_dump().items()
                )
            self._data[vault]["pull-secret"] = Item(
                title="pull-secret", fields=fields, sections=sections
            )

    def get_item(self, title: str, vault_id: str) -> Item:
        """Get an item from a 1Password vault.

        Parameters
        ----------
        title
            Title of the item.
        vault_id
            UUID of the vault.

        Returns
        -------
        Item
            Corresponding item.

        Raises
        ------
        FailedToRetrieveItemException
            Raised if the item was not found.
        """
        try:
            vault = self._uuids[vault_id]
            return self._data[vault][title]
        except KeyError:
            msg = f"Item {title} does not exist"
            raise FailedToRetrieveItemException(msg) from None

    def get_vault_by_title(self, title: str) -> Vault:
        """Get vault metadata by title.

        There are more fields normally, but we only care about the ``id``
        field. Populate this on the fly with a generated UUID the first time
        we're asked for a vault by name, provided that we have data for that
        vault name.

        Parameters
        ----------
        title
            Title of the vault.

        Returns
        -------
        Vault
            Partially-filled-out vault model.

        Raises
        ------
        FailedToRetrieveVaultException
            Raised if we have no data for this vault title.
        """
        if title not in self._data:
            msg = f"Vault {title} does not exist"
            raise FailedToRetrieveVaultException(msg) from None
        assert title in self._data
        for vault_id, name in self._uuids.items():
            if name == title:
                return Vault(id=vault_id, name=name)
        vault_id = str(uuid.uuid4())
        self._uuids[vault_id] = title
        return Vault(id=vault_id, name=title)


def patch_onepassword() -> Iterator[MockOnepasswordClient]:
    """Replace the onepasswordconnectsdk client with a mock class.

    Yields
    ------
    MockOnepasswordClient
        Mock onepasswordconnectsdk client.
    """
    mock = MockOnepasswordClient()
    with patch("phalanx.storage.onepassword.new_client", return_value=mock):
        old = os.getenv("OP_CONNECT_TOKEN")
        os.environ["OP_CONNECT_TOKEN"] = "some-token"
        yield mock
        if old:
            os.environ["OP_CONNECT_TOKEN"] = old
        else:
            del os.environ["OP_CONNECT_TOKEN"]
