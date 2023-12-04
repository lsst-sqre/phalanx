"""Mock Vault API for testing."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from collections.abc import Iterator
from datetime import timedelta
from typing import Any
from unittest.mock import patch
from uuid import uuid4

import hvac
from hvac.exceptions import InvalidPath
from safir.datetime import current_datetime, isodatetime

from phalanx.models.vault import VaultAppRoleMetadata, VaultToken

from .data import phalanx_test_path

__all__ = [
    "MockVaultClient",
    "patch_vault",
]


class MockVaultClient:
    """Mock Vault client for testing."""

    def __init__(self) -> None:
        # All APIs are currently collapsed into one object rather than using
        # sub-objects in the hope that all method calls will remain
        # unique. This may need to be revisited in the future if that hope
        # does not hold.
        self.approle = self
        self.auth = self
        self.kv = self
        self.secrets = self
        self.sys = self
        self.token = self

        self._approles: dict[str, VaultAppRoleMetadata] = {}
        self._data: defaultdict[str, dict[str, dict[str, str]]]
        self._data = defaultdict(dict)
        self._policies: dict[str, str] = {}
        self._tokens: list[VaultToken] = []
        self._secret_ids: defaultdict[str, list[tuple[str, str]]]
        self._secret_ids = defaultdict(list)

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
        data_path = phalanx_test_path() / "vault" / environment
        for app_data_path in data_path.iterdir():
            application = app_data_path.stem
            with app_data_path.open() as fh:
                self._data[app_path][application] = json.load(fh)

    def create(
        self,
        *,
        display_name: str,
        policies: list[str],
        ttl: str,
        create_expired_token: bool = False,
    ) -> dict[str, Any]:
        """Create a new authentication token.

        Parameters
        ----------
        display_name
            Display name of the token. Simulate the (weird) behavior of Vault
            and add ``token-`` to the start of this name.
        policies
            Policies to set for the token.
        ttl
            Lifetime (time-to-live) of the token. Must end in ``d`` for the
            test suite.
        create_expired_token
            Special test-only option that creates a token that expired one
            day ago.
        """
        assert ttl[-1] == "d"
        if create_expired_token:
            expires = current_datetime() - timedelta(days=1)
        else:
            expires = current_datetime() + timedelta(days=int(ttl[:-1]))
        token = VaultToken(
            display_name=f"token-{display_name}",
            token=f"s.{os.urandom(16).hex()}",
            accessor=os.urandom(16).hex(),
            policies=policies,
            expires=expires,
        )
        self._tokens.append(token)
        return {
            "auth": {
                "client_token": token.token,
                "accessor": token.accessor,
                "token_policies": token.policies,
            }
        }

    def create_or_update_approle(
        self, role_name: str, *, token_policies: list[str], token_type: str
    ) -> None:
        """Create or update an AppRole.

        Parameters
        ----------
        role_name
            Name of the AppRole.
        token_policies
            List of policies to apply to the AppRole.
        token_type
            Type of token (must be ``service``).
        """
        assert token_type == "service"
        self._approles[role_name] = VaultAppRoleMetadata(
            role_id=str(uuid4()), policies=token_policies
        )

    def create_or_update_policy(self, path: str, policy: str) -> None:
        """Create or update a policy.

        Parameters
        ----------
        path
            Vault path to the Policy.
        policy
            Policy document.
        """
        self._policies[path] = policy

    def create_or_update_secret(
        self, path: str, secret: dict[str, str]
    ) -> None:
        """Create or update a full secret.

        Parameters
        ----------
        path
            Vault path to the secret.
        secret
            New value for the secret.
        """
        base_path, application = path.rsplit("/", 1)
        self._data[base_path][application] = secret

    def delete_latest_version_of_secret(self, path: str) -> None:
        """Delete the latest version of a Vault secret.

        Parameters
        ----------
        path
            Vault path to the secret.

        Raises
        ------
        InvalidPath
            Raised if the provided Vault path does not exist.
        """
        base_path, application = path.rsplit("/", 1)
        if application not in self._data[base_path]:
            raise InvalidPath(f"Unknown Vault path {path}")
        del self._data[base_path][application]

    def destroy_secret_id_accessor(
        self, role_name: str, secret_id_accessor: str
    ) -> None:
        """Destroy a SecretID for an AppRole.

        Parameters
        ----------
        role_name
            Name of the role.
        secret_id_accessor
            Accessor of a SecretID.

        Raises
        ------
        InvalidPath
            Raised if the AppRole doesn't exist.
        """
        if role_name not in self._approles:
            raise InvalidPath(f"Unknown AppRole {role_name}")
        self._secret_ids[role_name] = [
            s
            for s in self._secret_ids[role_name]
            if s[1] != secret_id_accessor
        ]

    def generate_secret_id(self, role_name: str) -> dict[str, Any]:
        """Generate a SecretID for an AppRole.

        Parameters
        ----------
        role_name
            Name of the role.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.

        Raises
        ------
        InvalidPath
            Raised if the AppRole does not exist.
        """
        if role_name not in self._approles:
            raise InvalidPath(f"Unknown AppRole {role_name}")
        secret_id = str(uuid4())
        secret_id_accessor = str(uuid4())
        self._secret_ids[role_name].append((secret_id, secret_id_accessor))
        return {
            "data": {
                "secret_id": secret_id,
                "secret_id_accessor": secret_id_accessor,
            }
        }

    def list_accessors(self) -> dict[str, Any]:
        """List all token accessors.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.
        """
        return {"data": {"keys": [t.accessor for t in self._tokens]}}

    def list_secret_id_accessors(self, role_name: str) -> dict[str, Any]:
        """List all SecretID accessors for a given role.

        Parameters
        ----------
        role_name
            Name of the role.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.

        Raises
        ------
        InvalidPath
            Raised if the AppRole doesn't exist.
        """
        if role_name not in self._approles:
            raise InvalidPath(f"Unknown AppRole {role_name}")
        return {"data": {"keys": [s[1] for s in self._secret_ids[role_name]]}}

    def list_secrets(self, path: str) -> dict[str, Any]:
        """List all secrets available under a path.

        Parameters
        ----------
        path
            Vault path to the directory of secrets.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.
        """
        return {"data": {"keys": list(self._data[path].keys())}}

    def lookup_accessor(self, accessor: str) -> dict[str, Any]:
        """Look up a token by accessor.

        Parameter
        ---------
        accessor
            Token accessor.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.

        Raises
        ------
        InvalidPath
            Raised if the accessor does not exist.
        """
        token = None
        for candidate in self._tokens:
            if candidate.accessor == accessor:
                token = candidate
                break
        if not token:
            raise InvalidPath(f"Unknown accessor {accessor}")
        return {
            "data": {
                "display_name": token.display_name,
                "expire_time": isodatetime(token.expires),
                "policies": list(token.policies),
            }
        }

    def patch(self, path: str, secret: dict[str, str]) -> None:
        """Update specific keys and values in a secret.

        Parameters
        ----------
        path
            Vault path for the secret.
        secret
            Keys and values to update.

        Raises
        ------
        InvalidPath
            Raised if the provided Vault path does not exist.
        """
        base_path, application = path.rsplit("/", 1)
        if application not in self._data[base_path]:
            raise InvalidPath(f"Unknown Vault path {path}")
        self._data[base_path][application].update(secret)

    def read_policy(self, name: str) -> dict[str, Any]:
        """Read a Vault policy.

        Parameters
        ----------
        name
            Name of the policy.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.

        Raises
        ------
        InvalidPath
            Raised if the policy does not exist.
        """
        if name not in self._policies:
            raise InvalidPath(f"Unknown policy {name}")
        return {"name": name, "rules": self._policies[name]}

    def read_role(self, role_name: str) -> dict[str, Any]:
        """Read metadata about a Vault AppRole.

        Parameters
        ----------
        role_name
            Name of the role.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.

        Raises
        ------
        InvalidPath
            Raised if the AppRole does not exist.
        """
        if role_name not in self._approles:
            raise InvalidPath(f"Unknown AppRole {role_name}")
        return {
            "data": {
                "token_policies": list(self._approles[role_name].policies)
            }
        }

    def read_role_id(self, role_name: str) -> dict[str, Any]:
        """Read the RoleID of a Vault AppRole.

        Parameters
        ----------
        role_name
            Name of the role.

        Returns
        -------
        dict
            Reply matching the Vault client reply structure.

        Raises
        ------
        InvalidPath
            Raised if the AppRole does not exist.
        """
        if role_name not in self._approles:
            raise InvalidPath(f"Unknown AppRole {role_name}")
        return {"data": {"role_id": self._approles[role_name].role_id}}

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

        Raises
        ------
        InvalidPath
            Raised if the provided Vault path does not exist.
        """
        assert raise_on_deleted_version
        base_path, application = path.rsplit("/", 1)
        if application not in self._data[base_path]:
            raise InvalidPath(f"Unknown Vault path {path}")
        values = self._data[base_path][application]
        return {"data": {"data": values.copy()}}

    def revoke_accessor(self, accessor: str) -> None:
        """Revoke a token by accessor.

        Parameters
        ----------
        accessor
            Accessor of the token.

        Raises
        ------
        InvalidPath
            Raised if the provided Vault token accessor does not exist.
        """
        # Rely on the lookup to raise an exception if needed.
        self.lookup_accessor(accessor)

        # Do the delete.
        self._tokens = [t for t in self._tokens if t.accessor != accessor]


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
