"""Test fixtures."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import jinja2
import pytest

from phalanx.factory import Factory

from .support.data import phalanx_test_path
from .support.vault import MockVaultClient, patch_vault


@pytest.fixture
def factory() -> Iterator[Factory]:
    """Change directories to the test data directory and return a factory."""
    input_path = phalanx_test_path()
    cwd = Path.cwd()
    os.chdir(str(input_path))
    yield Factory()
    os.chdir(str(cwd))


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
