"""Tests for the Helm models."""

from __future__ import annotations

from pathlib import Path

from phalanx.models.helm import HelmStarter


def test_starter_list() -> None:
    starters_path = Path(__file__).parent.parent.parent / "starters"
    available = (s.name for s in starters_path.iterdir() if s.is_dir())
    assert sorted(available) == sorted(s.value for s in HelmStarter)
