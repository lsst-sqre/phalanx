"""Tests for the secrets command-line subcommand."""

import json
import os
import re
from base64 import b64decode, b64encode
from datetime import UTC, datetime, timedelta
from pathlib import Path

import bcrypt
import click
import pytest
import yaml
from cryptography.fernet import Fernet

from phalanx.factory import Factory

from ..support.cli import run_cli
from ..support.data import PhalanxData
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


def test_audit(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    input_path = data.path("input")
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")

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
    data.assert_text_matches(result.output, "secrets/audit")


def test_audit_exclude(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    input_path = data.path("input")
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")

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
    data.assert_text_matches(result.output, "secrets/audit-exclude")


def test_audit_application(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    """Audit one application, including its copied secrets."""
    environment = factory.create_config_storage().load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")
    result = run_cli(
        "secrets",
        "audit",
        "idfdev",
        "--application",
        "gafaelfawr",
        "--secrets",
        str(data.path("input/secrets/idfdev.yaml")),
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 1
    assert result.output == (
        "Missing secrets:\n"
        "• gafaelfawr session-secret\n"
        "• gafaelfawr signing-key\n"
        "• gafaelfawr slack-webhook\n"
        "\nSecrets that do not have their expected value:\n"
        "• gafaelfawr database-password\n"
        "\nUnknown secrets in Vault:\n"
        "• gafaelfawr cilogon\n"
    )


@pytest.mark.parametrize("command", ["audit", "list", "sync"])
@pytest.mark.parametrize("application", ["unknown", "tap"])
def test_application_unknown(command: str, application: str) -> None:
    """Reject applications that are unknown or disabled before using Vault."""
    result = run_cli(
        "secrets", command, "idfdev", "--application", application
    )
    assert result.exit_code == 2
    assert (
        f"Application {application} is not enabled for environment idfdev"
        in result.output
    )


def test_audit_onepassword_missing(
    *,
    data: PhalanxData,
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
) -> None:
    """Check reporting of missing 1Password secrets."""
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.create_empty_test_vault(vault_title)
    mock_vault.load_test_data(data, environment.vault_path_prefix, "minikube")

    result = run_cli(
        "secrets",
        "audit",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken", "VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 1
    data.assert_text_matches(result.output, "secrets/audit-missing")


def test_list(data: PhalanxData) -> None:
    result = run_cli("secrets", "list", "idfdev")
    assert result.exit_code == 0
    data.assert_text_matches(result.output, "secrets/list")


def test_list_application() -> None:
    result = run_cli("secrets", "list", "idfdev", "--application", "postgres")
    assert result.exit_code == 0
    assert result.output == (
        "postgres nublado3_password\npostgres root_password\n"
    )


def test_list_path_search(data: PhalanxData) -> None:
    """Test that we can find the root of the tree from a subdirectory."""
    cwd = Path.cwd()
    os.chdir(str(data.path("input") / "applications" / "gafaelfawr"))
    try:
        result = run_cli("secrets", "list", "idfdev", needs_config=False)
        assert result.exit_code == 0
        data.assert_text_matches(result.output, "secrets/list")
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
    data: PhalanxData,
    factory: Factory,
    tmp_path: Path,
    mock_onepassword: MockOnepasswordClient,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(data, vault_title, "minikube")
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
    data.assert_text_matches(output, "secrets/onepassword-secrets")

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


def test_static_template(data: PhalanxData) -> None:
    result = run_cli("secrets", "static-template", "idfdev")
    assert result.exit_code == 0
    data.assert_text_matches(result.output, "secrets/static-template")


def test_sync(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    input_path = data.path("input")
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")
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
    data.assert_text_matches(result.output, "secrets/sync")

    # Check that all static secrets were copied over correctly.
    static_secrets = data.read_static_secrets("input/secrets/idfdev")
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
    data.assert_text_matches(result.output, "secrets/sync-delete")
    after = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert "cilogon" in gafaelfawr
    assert "cilogon" not in after
    del gafaelfawr["cilogon"]
    assert after == gafaelfawr

    # Add a pull-secret to Vault, run secrets sync --delete again without
    # static secrets, and ensure that pull-secret wasn't deleted.
    pull_secret = data.read_json("output/minikube/pull-secret")
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
    *,
    data: PhalanxData,
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
) -> None:
    input_path = data.path("input")
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(data, vault_title, "minikube")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "minikube")
    _, base_vault_path = environment.vault_path_prefix.split("/", 1)

    # It should be possible to omit VAULT_TOKEN and get the value from
    # 1Password.
    result = run_cli(
        "secrets",
        "sync",
        "minikube",
        env={"OP_CONNECT_TOKEN": "sometoken"},
    )
    data.assert_text_matches(result.output, "sync-onepassword")
    assert result.exit_code == 0

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

    # Check that the Gafaelfawr OpenID Connect clients secret is correct.
    vault = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    seen_oidc_secrets = json.loads(vault["oidc-server-secrets"])
    data.assert_json_matches(seen_oidc_secrets, "output/minikube/oidc-clients")

    # Check that the pull secret is correct.
    vault = _get_app_secret(mock_vault, f"{base_vault_path}/pull-secret")
    data.assert_json_matches(vault, "output/minikube/pull-secret")


@pytest.mark.parametrize("regenerate", [False, True])
def test_sync_application(
    *,
    data: PhalanxData,
    factory: Factory,
    mock_vault: MockVaultClient,
    regenerate: bool,
) -> None:
    """Deletion and regeneration must only affect the selected application."""
    environment = factory.create_config_storage().load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")
    _, base_path = environment.vault_path_prefix.split("/", 1)
    pull_secret = data.read_json("output/minikube/pull-secret")
    mock_vault.create_or_update_secret(f"{base_path}/pull-secret", pull_secret)
    before = {
        app: _get_app_secret(mock_vault, f"{base_path}/{app}").copy()
        for app in mock_vault.list_secrets(base_path)["data"]["keys"]
    }
    options = ["--regenerate"] if regenerate else []
    result = run_cli(
        "secrets",
        "sync",
        "idfdev",
        "--application",
        "gafaelfawr",
        "--delete",
        "--secrets",
        str(data.path("input/secrets/idfdev.yaml")),
        *options,
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert all("gafaelfawr" in line for line in result.output.splitlines())
    after = _get_app_secret(mock_vault, f"{base_path}/gafaelfawr")
    assert "cilogon" not in after
    assert after["database-password"] == "some-other-database-password"
    assert after["slack-webhook"] == "https://hooks.slack.com/app-slack-hook"
    assert (
        before["gafaelfawr"]["bootstrap-token"] != after["bootstrap-token"]
    ) == regenerate
    for app, values in before.items():
        if app != "gafaelfawr":
            assert _get_app_secret(mock_vault, f"{base_path}/{app}") == values


@pytest.mark.parametrize("command", ["audit", "sync"])
@pytest.mark.parametrize("exclude_option", ["--exclude", "-e"])
@pytest.mark.parametrize("excluded_application", ["gafaelfawr", "argocd"])
def test_application_exclude_mutually_exclusive(
    command: str, exclude_option: str, excluded_application: str
) -> None:
    """Reject conflicting filters before loading configuration or secrets."""
    result = run_cli(
        "secrets",
        command,
        "idfdev",
        "--application",
        "gafaelfawr",
        exclude_option,
        excluded_application,
        "--config",
        "/nonexistent/phalanx-config",
        needs_config=False,
    )
    assert result.exit_code == 2
    assert (
        "--application and --exclude are mutually exclusive" in result.output
    )


@pytest.mark.parametrize("command", ["audit", "sync"])
def test_application_copied_secrets(
    data: PhalanxData,
    factory: Factory,
    mock_vault: MockVaultClient,
    command: str,
) -> None:
    """Scoped commands resolve copies without changing their sources."""
    environment = factory.create_config_storage().load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")
    _, base_path = environment.vault_path_prefix.split("/", 1)
    before = _get_app_secret(mock_vault, f"{base_path}/nublado").copy()
    before_postgres = _get_app_secret(
        mock_vault, f"{base_path}/postgres"
    ).copy()
    assert before_postgres["nublado3_password"] != before["hub_db_password"]
    options = ["--regenerate", "--delete"] if command == "sync" else []
    result = run_cli(
        "secrets",
        command,
        "idfdev",
        "--application",
        "postgres",
        *options,
        env={"VAULT_TOKEN": "sometoken"},
    )
    postgres = _get_app_secret(mock_vault, f"{base_path}/postgres")
    if command == "audit":
        assert result.exit_code == 1
        assert result.output == (
            "Secrets that do not have their expected value:\n"
            "• postgres nublado3_password\n"
        )
        assert postgres == before_postgres
    else:
        assert result.exit_code == 0
        assert all("postgres" in line for line in result.output.splitlines())
        assert postgres["nublado3_password"] == before["hub_db_password"]
    assert _get_app_secret(mock_vault, f"{base_path}/nublado") == before


@pytest.mark.parametrize("command", ["audit", "sync"])
def test_application_onepassword(
    data: PhalanxData,
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
    command: str,
) -> None:
    """Unrelated missing static secrets and pull secrets are ignored."""
    environment = factory.create_config_storage().load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(data, vault_title, "minikube")
    vault_id = mock_onepassword.get_vault_by_title(vault_title).id
    # Break an unrelated required static secret in 1Password.
    mock_onepassword.get_item("argocd", vault_id).fields = []
    result = run_cli(
        "secrets",
        command,
        "minikube",
        "--application",
        "mobu",
        env={"OP_CONNECT_TOKEN": "sometoken"},
    )
    if command == "audit":
        assert result.exit_code == 1
        assert result.output == (
            "Missing secrets:\n• mobu ALERT_HOOK\n• mobu app-alert-webhook\n"
        )
    else:
        assert result.exit_code == 0
        assert result.output == "Created Vault secret for mobu\n"
        _, base_path = environment.vault_path_prefix.split("/", 1)
        assert mock_vault.list_secrets(base_path)["data"]["keys"] == ["mobu"]


def test_sync_onepassword_errors(
    *,
    data: PhalanxData,
    factory: Factory,
    mock_onepassword: MockOnepasswordClient,
    mock_vault: MockVaultClient,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert environment.onepassword
    vault_title = environment.onepassword.vault_title
    mock_onepassword.load_test_data(data, vault_title, "minikube")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "minikube")

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
    assert app_name in result.output
    assert key in result.output
    assert result.exit_code == 2

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
    assert app_name in result.output
    assert key in result.output
    assert result.exit_code == 2


def test_sync_regenerate(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    input_path = data.path("input")
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")
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
    data.assert_text_matches(result.output, "secrets/sync-regenerate")

    # Check that all static secrets were copied over correctly.
    static_secrets = data.read_static_secrets("input/secrets/idfdev")
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
    assert before["bootstrap-token"] != after["bootstrap-token"]
    assert re.match("^[0-9a-f]{64}$", after["redis-password"])
    assert before["redis-password"] != after["redis-password"]

    # Check whether bcrypt passwords are generated properly.
    argocd = _get_app_secret(mock_vault, f"{base_vault_path}/argocd")
    password = argocd["admin.plaintext_password"].encode()
    assert bcrypt.checkpw(password, argocd["admin.password"].encode())

    # Check whether mtime secrets are generated properly.
    mtime = datetime.fromisoformat(argocd["admin.passwordMtime"])
    now = datetime.now(tz=UTC)
    assert now - timedelta(seconds=5) <= mtime <= now


def test_sync_exclude(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    input_path = data.path("input")
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")

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
    data.assert_text_matches(result.output, "secrets/sync-exclude")


def test_sync_modify_delete(
    data: PhalanxData, factory: Factory, mock_vault: MockVaultClient
) -> None:
    """Test a sync that modifies and deletes a secret key at the same time."""
    input_path = data.path("input")
    secrets_path = input_path / "secrets" / "idfdev.yaml"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(data, environment.vault_path_prefix, "idfdev")
    _, base_vault_path = environment.vault_path_prefix.split("/", 1)
    before = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")

    result = run_cli(
        "secrets",
        "sync",
        "--secrets",
        str(secrets_path),
        "--exclude",
        "argocd",
        "--exclude",
        "nublado",
        "--exclude",
        "portal",
        "--exclude",
        "postgres",
        "--exclude",
        "unknown",
        "--delete",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    data.assert_text_matches(result.output, "secrets/sync-modify-delete")
    after = _get_app_secret(mock_vault, f"{base_vault_path}/gafaelfawr")
    assert before["database-password"] != after["database-password"]
    assert after.get("session-secret")
    assert after.get("signing-key")
    assert after.get("slack-webhook")
    assert "cilogon" not in after
