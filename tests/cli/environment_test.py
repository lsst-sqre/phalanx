"""Tests for the environment command-line subcommand."""

from __future__ import annotations

from pathlib import Path

from ..support.cli import run_cli


def test_schema() -> None:
    result = run_cli("environment", "schema", needs_config=False)
    assert result.exit_code == 0
    current = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "extras"
        / "schemas"
        / "environment.json"
    )
    assert result.output == current.read_text()
