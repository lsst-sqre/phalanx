"""Tests for the secrets command-line subcommand."""

from __future__ import annotations

import json
import os
from pathlib import Path

from click.testing import CliRunner
from phalanx.cli import main
from phalanx.factory import Factory

from ..support.data import phalanx_test_path, read_output_data
from ..support.vault import MockVaultClient


def test_audit(mock_vault: MockVaultClient) -> None:
    input_path = phalanx_test_path()
    os.chdir(str(input_path))
    input_path / "vault" / "idfdev"
    factory = Factory()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    runner = CliRunner()
    result = runner.invoke(
        main, ["secrets", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "secrets-audit")


def test_list() -> None:
    input_path = phalanx_test_path()
    os.chdir(str(input_path))
    runner = CliRunner()
    result = runner.invoke(
        main, ["secrets", "list", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "secrets-list")


def test_schema() -> None:
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


def test_static_template() -> None:
    input_path = phalanx_test_path()
    os.chdir(str(input_path))
    runner = CliRunner()
    result = runner.invoke(
        main, ["secrets", "static-template", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "static-secrets.yaml")


def test_vault_secrets(tmp_path: Path, mock_vault: MockVaultClient) -> None:
    input_path = phalanx_test_path()
    vault_input_path = input_path / "vault" / "idfdev"
    os.chdir(str(input_path))
    factory = Factory()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["secrets", "vault-secrets", "idfdev", str(tmp_path)],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert result.output == ""

    expected_files = {p.name for p in vault_input_path.iterdir()}
    output_files = {p.name for p in tmp_path.iterdir()}
    assert expected_files == output_files
    for expected_path in vault_input_path.iterdir():
        with expected_path.open() as fh:
            expected = json.load(fh)
        with (tmp_path / expected_path.name).open() as fh:
            assert expected == json.load(fh)
