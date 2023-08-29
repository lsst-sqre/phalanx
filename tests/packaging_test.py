"""Test that the Python packaging metadata."""

from __future__ import annotations

from phalanx import __version__


def test_version() -> None:
    """Test that the package has a version (and is installed)."""
    assert len(__version__) > 0
    assert __version__ != "0.0.0"  # would be if not installed
