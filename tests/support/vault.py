"""Mock Vault API for testing."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterator
from typing import Any
from unittest.mock import patch

import hvac

from .data import phalanx_test_path

__all__ = [
    "MockVaultClient",
    "patch_vault",
]


class MockVaultClient:
    """Mock Vault client for testing."""

    def __init__(self) -> None:
        self.secrets = self
        self.kv = self
        self._data: defaultdict[str, dict[str, dict[str, str]]]
        self._data = defaultdict(dict)
        self._paths: dict[str, str] = {}

    def load_test_data(self, path: str, environment: str) -> None:
        """Load Vault test data for the given environment.

        This method is not part of the Vault API. It is intended for use by
        the test suite to set up a test.

        Parameters
        ----------
        path
            Path to the environment data in Vault.
        environment
            Name of the environment for which to load Vault test data.
        """
        _, app_path = path.split("/", 1)
        self._paths[app_path] = environment
        data_path = phalanx_test_path() / "vault" / environment
        for app_data_path in data_path.iterdir():
            application = app_data_path.stem
            with app_data_path.open() as fh:
                self._data[environment][application] = json.load(fh)

    def read_secret(
        self, path: str, raise_on_deleted_version: bool | None = None
    ) -> dict[str, Any]:
        """Read a secret from Vault.

        Parameters
        ----------
        path
            Vault path to the secret.
        raise_on_deleted_version
            Whether to raise an exception if the most recent version is
            deleted (required to be `True`).

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.
        """
        assert raise_on_deleted_version
        base_path, application = path.rsplit("/", 1)
        environment = self._paths[base_path]
        values = self._data[environment][application]
        return {"data": {"data": values}}


def patch_vault() -> Iterator[MockVaultClient]:
    """Replace the HVAC Vault client with a mock class.

    Yields
    ------
    MockVaultClient
        Mock HVAC Vault client.
    """
    mock_vault = MockVaultClient()
    with patch.object(hvac, "Client", return_value=mock_vault):
        yield mock_vault
