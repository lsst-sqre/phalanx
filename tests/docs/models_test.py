"""Tests for the phalanx.docs.models module."""

from __future__ import annotations

from pathlib import Path

from phalanx.docs.models import Phalanx


def test_phalanx_load() -> None:
    """Smoke test for loading Phalanx repository metadata."""
    root_dir = Path(__file__).parent.parent.parent
    metadata = Phalanx.load_phalanx(root_dir)
    assert isinstance(metadata, Phalanx)

    assert len(metadata.environments) > 0
    assert len(metadata.apps) > 0
