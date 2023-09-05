"""Tests for the secrets command-line subcommand."""

from __future__ import annotations

import os
import re
from base64 import b64decode
from datetime import datetime, timedelta
from pathlib import Path

import bcrypt
import click
import yaml
from cryptography.fernet import Fernet
from safir.datetime import current_datetime

from phalanx.factory import Factory
from phalanx.models.gafaelfawr import Token

from ..support.cli import run_cli
from ..support.data import (
    assert_json_dirs_match,
    output_path,
    phalanx_test_path,
    read_input_static_secrets,
    read_output_data,
)
from ..support.onepassword import MockOnepasswordClient
from ..support.vault import MockVaultClient


def _get_app_secret(mock_vault: MockVaultClient, path: str) -> dict[str, str]:
    """Get an application secret from the mock Vault.

    Parameters
    ----------
    mock_vault
        Mock Vault client.
    path
        Path within Vault to the application.

    Returns
    -------
    dict of str
        Key and value pairs for that application.
    """
    result = mock_vault.read_secret(path, raise_on_deleted_version=True)
    return result["data"]["data"]


def test_audit(factory: Factory, mock_vault: MockVaultClient) -> None:
    input_path = phalanx_test_path()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    secrets_path = input_path / "secrets" / "idfdev.yaml"
    result = run_cli(
        "secrets", "audit", "--secrets", str(secrets_path), "idfdev"
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "secrets-audit")


def test_list() -> None:
    result = run_cli("secrets", "list", "idfdev")
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "secrets-list")


def test_list_path_search() -> None:
    """Test that we can find the root of the tree from a subdirectory."""
    cwd = Path.cwd()
    os.chdir(str(phalanx_test_path() / "applications" / "gafaelfawr"))
    try:
        result = run_cli("secrets", "list", "idfdev", needs_config=False)
        assert result.exit_code == 0
        assert result.output == read_output_data("idfdev", "secrets-list")
    finally:
        os.chdir(str(cwd))


def test_list_path_failure() -> None:
    """Test failure to find the root of the config tree."""
    cwd = Path.cwd()
    os.chdir("/usr")
    try:
        result = run_cli("secrets", "list", "idfdev", needs_config=False)
        assert result.exit_code == click.UsageError.exit_code
        assert "Cannot locate root of Phalanx configuration" in result.output
    finally:
        os.chdir(str(cwd))


def test_onepassword_secrets(
    factory: Factory,
    tmp_path: Path,
    mock_onepassword: MockOnepasswordClient,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(vault_title, "minikube")
    expected_path = output_path() / "minikube" / "onepassword"

    result = run_cli(
        "secrets", "onepassword-secrets", "minikube", str(tmp_path)
    )
    assert result.exit_code == 0
    assert result.output == ""

    assert_json_dirs_match(tmp_path, expected_path)


def test_schema() -> None:
    result = run_cli("secrets", "schema", needs_config=False)
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
    result = run_cli("secrets", "static-template", "idfdev")
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "static-secrets.yaml")


def test_sync(factory: Factory, mock_vault: MockVaultClient) -> None:
    input_path = phalanx_test_path()
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")
    _, base_vault_path = environment.vault_path_prefix.split("/", 1)

    result = run_cli(
        "secrets", "sync", "--secrets", str(secrets_path), "idfdev"
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "sync-output")

    # Check that all static secrets were copied over correctly.
    static_secrets = read_input_static_secrets("idfdev")
    for application, values in static_secrets.items():
        vault = _get_app_secret(mock_vault, f"{base_vault_path}/{application}")
        for key, value in values.items():
            if key in vault:
                assert value == vault[key]

    # Check generated or copied secrets.
    argocd = _get_app_secret(mock_vault, f"{base_vault_path}/argocd")
    assert re.match("^[0-9a-f]{64}$", argocd["server.secretkey"])
    gafaelfawr = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert Fernet(gafaelfawr["session-secret"].encode())
    assert "-----BEGIN PRIVATE KEY-----" in gafaelfawr["signing-key"]
    webhook = static_secrets["mobu"]["app-alert-webhook"]
    assert gafaelfawr["slack-webhook"] == webhook
    nublado = _get_app_secret(mock_vault, f"{base_vault_path}/nublado")
    assert re.match("^[0-9a-f]{64}$", nublado["proxy_token"])
    postgres = _get_app_secret(mock_vault, f"{base_vault_path}/postgres")
    assert postgres["nublado3_password"] == nublado["hub_db_password"]

    # Now sync again with --delete. The only change should be that the stray
    # Gafaelfawr Vault secret key is deleted. This also tests that if the
    # static secrets are already in Vault, there's no need to provide a source
    # for static secrets and the Phalanx CLI will silently cope.
    result = run_cli("secrets", "sync", "--delete", "idfdev")
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "sync-delete-output")
    after = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert "cilogon" in gafaelfawr
    assert "cilogon" not in after
    del gafaelfawr["cilogon"]
    assert after == gafaelfawr


def test_sync_onepassword(
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
) -> None:
    input_path = phalanx_test_path()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(vault_title, "minikube")
    mock_vault.load_test_data(environment.vault_path_prefix, "minikube")
    _, base_vault_path = environment.vault_path_prefix.split("/", 1)

    result = run_cli("secrets", "sync", "minikube")
    assert result.exit_code == 0
    assert result.output == read_output_data("minikube", "sync-output")

    # Check that all static secrets were copied over correctly.
    with (input_path / "onepassword" / "minikube.yaml").open() as fh:
        onepassword_secrets = yaml.safe_load(fh)
    for app_name, values in onepassword_secrets.items():
        vault = _get_app_secret(mock_vault, f"{base_vault_path}/{app_name}")
        application = environment.applications[app_name]
        for key, value in values.items():
            if application.secrets[key].onepassword.encoded:
                assert b64decode(value.encode()).decode() == vault[key]
            else:
                assert value == vault[key]


def test_sync_regenerate(
    factory: Factory, mock_vault: MockVaultClient
) -> None:
    input_path = phalanx_test_path()
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")
    _, base_vault_path = environment.vault_path_prefix.split("/", 1)
    before = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")

    result = run_cli(
        "secrets",
        "sync",
        "--secrets",
        str(secrets_path),
        "--regenerate",
        "idfdev",
    )
    assert result.exit_code == 0
    expected = read_output_data("idfdev", "sync-regenerate-output")
    assert result.output == expected

    # Check that all static secrets were copied over correctly.
    static_secrets = read_input_static_secrets("idfdev")
    for application, values in static_secrets.items():
        vault = _get_app_secret(mock_vault, f"{base_vault_path}/{application}")
        for key, value in values.items():
            if key in vault:
                assert value == vault[key]

    # Don't recheck all the details that match the regular sync test. Just
    # check that some secrets that would have been left alone without
    # --regenerate were regenerated and are syntactically valid.
    after = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert Token.from_str(after["bootstrap-token"])
    assert before["bootstrap-token"] != after["bootstrap-token"]
    assert re.match("^[0-9a-f]{64}$", after["redis-password"])
    assert before["redis-password"] != after["redis-password"]

    # Check whether bcrypt passwords are generated properly.
    argocd = _get_app_secret(mock_vault, f"{base_vault_path}/argocd")
    password = argocd["admin.plaintext_password"].encode()
    assert bcrypt.checkpw(password, argocd["admin.password"].encode())

    # Check whether mtime secrets are generated properly.
    mtime = datetime.fromisoformat(argocd["admin.passwordMtime"])
    now = current_datetime()
    assert now - timedelta(seconds=5) <= mtime <= now


def test_vault_secrets(
    factory: Factory, tmp_path: Path, mock_vault: MockVaultClient
) -> None:
    input_path = phalanx_test_path()
    vault_input_path = input_path / "vault" / "idfdev"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    result = run_cli("secrets", "vault-secrets", "idfdev", str(tmp_path))
    assert result.exit_code == 0
    assert result.output == ""

    assert_json_dirs_match(tmp_path, vault_input_path)
