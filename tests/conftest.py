"""Test fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import jinja2
import pytest

from phalanx.factory import Factory

from .support.data import phalanx_test_path
from .support.helm import MockHelmCommand, patch_helm
from .support.onepassword import MockOnepasswordClient, patch_onepassword
from .support.vault import MockVaultClient, patch_vault


@pytest.fixture(autouse=True)
def _clear_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove dangerous environment variables.

    Ensure that none of the tests can accidentally authenticate to a live
    Vault or 1Password Connect server by clearing the relevant environment
    variables.
    """
    monkeypatch.delenv("OP_CONNECT_TOKEN", raising=False)
    monkeypatch.delenv("VAULT_TOKEN", raising=False)


@pytest.fixture
def factory() -> Factory:
    """Create a factory pointing at the test data."""
    return Factory(phalanx_test_path())


@pytest.fixture
def mock_helm() -> Iterator[MockHelmCommand]:
    """Mock out Helm commands."""
    yield from patch_helm()


@pytest.fixture
def mock_onepassword() -> Iterator[MockOnepasswordClient]:
    """Mock out the 1Password Connect client API."""
    yield from patch_onepassword()


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
