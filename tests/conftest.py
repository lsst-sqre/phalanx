"""Test fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import jinja2
import pytest

from phalanx.factory import Factory

from .support.data import phalanx_test_path
from .support.vault import MockVaultClient, patch_vault


@pytest.fixture
def factory() -> Factory:
    """Create a factory pointing at the test data."""
    return Factory(phalanx_test_path())


@pytest.fixture
def mock_vault() -> Iterator[MockVaultClient]:
    """Mock out the HVAC Vault client API."""
    yield from patch_vault()


@pytest.fixture
def templates() -> jinja2.Environment:
    """Return the Jinja templating environment."""
    return jinja2.Environment(
        loader=jinja2.PackageLoader("phalanx", "data"),
        undefined=jinja2.StrictUndefined,
        autoescape=jinja2.select_autoescape(disabled_extensions=["tmpl"]),
    )
