"""Tests for the secrets command-line subcommand."""

from __future__ import annotations

import os

from click.testing import CliRunner
from phalanx.cli import main

from ..support.data import phalanx_test_path, read_output_data


def test_list() -> None:
    input_path = phalanx_test_path()
    os.chdir(str(input_path))
    runner = CliRunner()
    result = runner.invoke(
        main, ["secrets", "list", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "secrets-list")
