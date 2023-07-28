"""Tests for the secrets command-line subcommand."""

from __future__ import annotations

import os
from pathlib import Path

from click.testing import CliRunner
from phalanx.cli import main

from ..support.data import phalanx_test_path, read_output_data


def test_generate_schema() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["secrets", "schema"], catch_exceptions=False)
    assert result.exit_code == 0
    current = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "extras"
        / "schemas"
        / "secrets.json"
    )
    assert result.output == current.read_text()


def test_list() -> None:
    input_path = phalanx_test_path()
    os.chdir(str(input_path))
    runner = CliRunner()
    result = runner.invoke(
        main, ["secrets", "list", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "secrets-list")
