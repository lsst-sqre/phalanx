"""Test fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from .support.vault import MockVaultClient, patch_vault


@pytest.fixture
def mock_vault() -> Iterator[MockVaultClient]:
    """Mock out the HVAC Vault client API."""
    yield from patch_vault()
