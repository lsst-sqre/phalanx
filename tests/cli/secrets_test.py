"""Tests for the secrets command-line subcommand."""

from __future__ import annotations

import os
import re
from base64 import b64decode, b64encode
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
    phalanx_test_path,
    read_input_static_secrets,
    read_output_data,
    read_output_json,
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
        "secrets",
        "audit",
        "--secrets",
        str(secrets_path),
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "secrets-audit")


def test_audit_exclude(factory: Factory, mock_vault: MockVaultClient) -> None:
    input_path = phalanx_test_path()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    secrets_path = input_path / "secrets" / "idfdev.yaml"
    result = run_cli(
        "secrets",
        "audit",
        "--secrets",
        str(secrets_path),
        "--exclude",
        "argocd",
        "--exclude",
        "unknown",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 1
    all_output = read_output_data("idfdev", "secrets-audit").split("\n")
    expected = "\n".join(
        o for o in all_output if "argocd" not in o and "unknown" not in o
    )
    assert result.output == expected


def test_audit_onepassword_missing(
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
) -> None:
    """Check reporting of missing 1Password secrets."""
    phalanx_test_path()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.create_empty_test_vault(vault_title)
    mock_vault.load_test_data(environment.vault_path_prefix, "minikube")

    result = run_cli(
        "secrets",
        "audit",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken", "VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 1
    assert result.output == read_output_data(
        "minikube", "audit-missing-output"
    )


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
    output_path = tmp_path / "static-secrets.yaml"

    result = run_cli(
        "secrets",
        "onepassword-secrets",
        "minikube",
        "-o",
        str(output_path),
        env={"OP_CONNECT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == ""

    output = output_path.read_text()
    assert output == read_output_data("minikube", "onepassword-secrets.yaml")

    result = run_cli(
        "secrets",
        "onepassword-secrets",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == output

    result = run_cli("secrets", "onepassword-secrets", "minikube")
    assert result.exit_code == 2
    assert "OP_CONNECT_TOKEN must be set" in result.output


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

    # Syncing without a VAULT_TOKEN when the static secrets don't contain one
    # should fail with an error.
    result = run_cli(
        "secrets", "sync", "--secrets", str(secrets_path), "idfdev"
    )
    assert result.exit_code == 2
    assert "VAULT_TOKEN not set" in result.output

    # Providing a VAULT_TOKEN should make the sync work.
    result = run_cli(
        "secrets",
        "sync",
        "--secrets",
        str(secrets_path),
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "sync-output")

    # Check that all static secrets were copied over correctly.
    static_secrets = read_input_static_secrets("idfdev")
    for application, values in static_secrets.applications.items():
        vault = _get_app_secret(mock_vault, f"{base_vault_path}/{application}")
        for key, value in values.items():
            if key in vault:
                assert value.value
                assert value.value.get_secret_value() == vault[key]

    # Check generated or copied secrets.
    argocd = _get_app_secret(mock_vault, f"{base_vault_path}/argocd")
    assert re.match("^[0-9a-f]{64}$", argocd["server.secretkey"])
    gafaelfawr = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert Fernet(gafaelfawr["session-secret"].encode())
    assert "-----BEGIN PRIVATE KEY-----" in gafaelfawr["signing-key"]
    webhook = static_secrets.applications["mobu"]["app-alert-webhook"]
    assert webhook.value
    assert gafaelfawr["slack-webhook"] == webhook.value.get_secret_value()
    nublado = _get_app_secret(mock_vault, f"{base_vault_path}/nublado")
    assert re.match("^[0-9a-f]{64}$", nublado["proxy_token"])
    postgres = _get_app_secret(mock_vault, f"{base_vault_path}/postgres")
    assert postgres["nublado3_password"] == nublado["hub_db_password"]

    # Now sync again with --delete. The only change should be that the stray
    # Gafaelfawr Vault secret key is deleted. This also tests that if the
    # static secrets are already in Vault, there's no need to provide a source
    # for static secrets and the Phalanx CLI will silently cope.
    result = run_cli(
        "secrets",
        "sync",
        "--delete",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "sync-delete-output")
    after = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert "cilogon" in gafaelfawr
    assert "cilogon" not in after
    del gafaelfawr["cilogon"]
    assert after == gafaelfawr

    # Add a pull-secret to Vault, run secrets sync --delete again without
    # static secrets, and ensure that pull-secret wasn't deleted.
    pull_secret = read_output_json("minikube", "pull-secret")
    mock_vault.create_or_update_secret(
        f"{base_vault_path}/pull-secret", pull_secret
    )
    result = run_cli(
        "secrets",
        "sync",
        "--delete",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == ""

    # Test the same path for audit. This is a bit misplaced, but all the data
    # is set up properly here.
    result = run_cli(
        "secrets", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 0
    assert result.output == ""


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

    # It should be possible to omit VAULT_TOKEN and get the value from
    # 1Password.
    result = run_cli(
        "secrets",
        "sync",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("minikube", "sync-output")

    # Check that all static secrets were copied over correctly.
    with (input_path / "onepassword" / "minikube.yaml").open() as fh:
        onepassword_secrets = yaml.safe_load(fh)
    for app_name, values in onepassword_secrets["applications"].items():
        vault = _get_app_secret(mock_vault, f"{base_vault_path}/{app_name}")
        application = environment.applications[app_name]
        for key, secret in values.items():
            value = secret["value"]
            if application.secrets[key].onepassword.encoded:
                assert b64decode(value.encode()).decode() == vault[key]
            else:
                assert value == vault[key]

    # Check that the pull secret is correct.
    pull_secret = read_output_json("minikube", "pull-secret")
    vault = _get_app_secret(mock_vault, f"{base_vault_path}/pull-secret")
    assert vault == pull_secret


def test_sync_onepassword_errors(
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
) -> None:
    phalanx_test_path()
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(vault_title, "minikube")
    mock_vault.load_test_data(environment.vault_path_prefix, "minikube")

    # Find a secret that's supposed to be encoded and change it to have an
    # invalid base64 string.
    app_name = None
    key = None
    for application in environment.applications.values():
        for secret in application.secrets.values():
            if secret.onepassword.encoded:
                app_name = application.name
                key = secret.key
                break
    assert app_name
    assert key
    vault_id = mock_onepassword.get_vault_by_title(vault_title).id
    item = mock_onepassword.get_item(app_name, vault_id)
    for field in item.fields:
        if field.label == key:
            field.value = "invalid base64"

    # sync should throw an exception containing the application and key.
    result = run_cli(
        "secrets",
        "sync",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken", "VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 2
    assert app_name in result.output
    assert key in result.output

    # Instead set the secret to a value that is valid base64, but of binary
    # data that cannot be decoded to a string.
    for field in item.fields:
        if field.label == key:
            field.value = b64encode("ää".encode("iso-8859-1")).decode()

    # sync should throw an exception containing the application and key.
    run_cli(
        "secrets",
        "sync",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken", "VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 2
    assert app_name in result.output
    assert key in result.output


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
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    expected = read_output_data("idfdev", "sync-regenerate-output")
    assert result.output == expected

    # Check that all static secrets were copied over correctly.
    static_secrets = read_input_static_secrets("idfdev")
    for application, values in static_secrets.applications.items():
        vault = _get_app_secret(mock_vault, f"{base_vault_path}/{application}")
        for key, value in values.items():
            if key in vault:
                assert value.value
                assert value.value.get_secret_value() == vault[key]

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


def test_sync_exclude(factory: Factory, mock_vault: MockVaultClient) -> None:
    input_path = phalanx_test_path()
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    result = run_cli(
        "secrets",
        "sync",
        "--secrets",
        str(secrets_path),
        "--exclude",
        "argocd",
        "--exclude",
        "portal",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    all_output = read_output_data("idfdev", "sync-output").split("\n")
    expected = "\n".join(
        o for o in all_output if "argocd" not in o and "portal" not in o
    )
    assert result.output == expected
