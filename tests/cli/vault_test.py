"""Tests for the vault command-line subcommand."""

from __future__ import annotations

import re
from base64 import b64encode
from datetime import datetime, timedelta
from pathlib import Path

import jinja2
import yaml
from safir.datetime import current_datetime

from phalanx.constants import VAULT_SECRET_TEMPLATE, VAULT_WRITE_TOKEN_LIFETIME
from phalanx.factory import Factory
from phalanx.models.vault import VaultAppRole, VaultToken

from ..support.cli import run_cli
from ..support.data import (
    assert_json_dirs_match,
    phalanx_test_path,
    read_output_data,
)
from ..support.vault import MockVaultClient


def test_audit(factory: Factory, mock_vault: MockVaultClient) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)
    _, role_name = vault_path.rsplit("/", 1)

    # Nothing has been created, so audit will report both missing.
    result = run_cli(
        "vault", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-both-missing")

    # Create an AppRole with the wrong policy and the wrong list of policies.
    mock_vault.create_or_update_policy(f"{vault_path}/read", "blah blah blah")
    mock_vault.create_or_update_approle(
        role_name, token_policies=["something"], token_type="service"
    )
    result = run_cli(
        "vault", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-approle-policy")

    # Use the Phalanx Vault service to recreate the AppRole, which should fix
    # all of the problems, and then add an extra policy.
    vault_service = factory.create_vault_service()
    vault_service.create_read_approle("idfdev")
    mock_vault.create_or_update_approle(
        role_name,
        token_policies=[f"{vault_path}/read", "extra"],
        token_type="service",
    )
    result = run_cli(
        "vault", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-approle-extra")

    # Fix the AppRole again, and create a write token with the wrong policies
    # and a write policy with the wrong contents.
    vault_service.create_read_approle("idfdev")
    mock_vault.create(
        display_name=role_name,
        policies=["something"],
        ttl=VAULT_WRITE_TOKEN_LIFETIME,
    )
    mock_vault.create_or_update_policy(f"{vault_path}/write", "blah blah blah")
    result = run_cli(
        "vault", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-token-policy")

    # Create a new token that expires in six days and use that to fix the
    # policy. This should also revoke the old token. Also create a new token
    # that is already expired. We have to do some munging here of the output
    # since the date and time will vary.
    vault_service.create_write_token("idfdev", "6d")
    mock_vault.create(
        display_name=role_name,
        policies=[f"{vault_path}/write"],
        ttl=VAULT_WRITE_TOKEN_LIFETIME,
        create_expired_token=True,
    )
    result = run_cli(
        "vault", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 1
    output = re.sub(r"[\d-]{10} [\d:]{8}", "<timestamp>", result.output)
    assert output == read_output_data("idfdev", "audit-token-expired")


def test_audit_clean(factory: Factory, mock_vault: MockVaultClient) -> None:
    vault_service = factory.create_vault_service()
    vault_service.create_read_approle("idfdev")
    vault_service.create_write_token("idfdev", VAULT_WRITE_TOKEN_LIFETIME)

    result = run_cli(
        "vault", "audit", "idfdev", env={"VAULT_TOKEN": "sometoken"}
    )
    assert result.exit_code == 0
    assert result.output == ""


def test_copy_secrets(
    factory: Factory, tmp_path: Path, mock_vault: MockVaultClient
) -> None:
    input_path = phalanx_test_path()
    vault_input_path = input_path / "vault" / "idfdev"
    old_path = "secret/k8s_operator/data-dev.lsst.cloud"
    mock_vault.load_test_data(old_path, "idfdev")

    result = run_cli(
        "vault",
        "copy-secrets",
        "idfdev",
        old_path,
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == read_output_data("idfdev", "copy-output")
    result = run_cli(
        "vault",
        "export-secrets",
        "idfdev",
        str(tmp_path),
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == ""

    assert_json_dirs_match(tmp_path, vault_input_path)

    # Check that the Vault secrets cannot be copied over themselves.
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    result = run_cli(
        "vault",
        "copy-secrets",
        "idfdev",
        environment.vault_path_prefix,
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 2
    assert "cannot be copied onto itself" in result.output


def test_create_read_approle(
    factory: Factory,
    mock_vault: MockVaultClient,
    templates: jinja2.Environment,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)

    result = run_cli(
        "vault",
        "create-read-approle",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    approle = VaultAppRole.model_validate(yaml.safe_load(result.output))
    assert approle.token_ttl == 0
    assert approle.token_max_ttl == 0

    # Check that the AppRole was created with the right RoleID and policies.
    assert approle.policies == [f"{vault_path}/read"]
    _, role_name = vault_path.rsplit("/", 1)
    r = mock_vault.read_role_id(role_name)
    assert r["data"]["role_id"] == approle.role_id

    # Check the read policy against the proper expansion of the template.
    r = mock_vault.read_policy(approle.policies[0])
    seen_policy = r["rules"]
    template = templates.get_template("vault-read-policy.hcl.jinja")
    expected_policy = template.render({"path": vault_path})
    assert seen_policy == expected_policy

    # Check that it has only one SecretID.
    r = mock_vault.list_secret_id_accessors(role_name)
    assert r["data"]["keys"] == [approle.secret_id_accessor]

    # Recreating the AppRole should result in a new SecretID and delete the
    # old one. Pass in the --as-secret flag and check that the result is
    # formatted like a secret.
    result = run_cli(
        "vault",
        "create-read-approle",
        "idfdev",
        "--as-secret",
        "vault-credentials",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    secret = yaml.safe_load(result.output)
    r = mock_vault.read_role_id(role_name)
    role_id = r["data"]["role_id"]
    expected = VAULT_SECRET_TEMPLATE.format(
        name="vault-credentials",
        role_id=b64encode(role_id.encode()).decode(),
        secret_id=secret["data"]["VAULT_SECRET_ID"],
    )
    assert result.output == expected
    assert secret["data"]["VAULT_SECRET_ID"] != approle.secret_id

    # Recreate one more time with a maximum token lifetime.
    result = run_cli(
        "vault",
        "create-read-approle",
        "--token-lifetime",
        "3600",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    approle = VaultAppRole.model_validate(yaml.safe_load(result.output))
    assert approle.token_ttl == 3600
    assert approle.token_max_ttl == 3600


def test_create_write_token(
    factory: Factory,
    mock_vault: MockVaultClient,
    templates: jinja2.Environment,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)
    if "/" in vault_path:
        display_name = "token-" + vault_path.rsplit("/", 1)[1]
    else:
        display_name = "token-" + vault_path
    lifetime = timedelta(days=int(VAULT_WRITE_TOKEN_LIFETIME[:-1]))

    result = run_cli(
        "vault",
        "create-write-token",
        "idfdev",
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    token = VaultToken.model_validate(yaml.safe_load(result.output))
    assert token.display_name == display_name
    expires = current_datetime() + lifetime
    assert token.expires
    assert expires - timedelta(seconds=5) <= token.expires <= expires
    assert token.policies == [f"{vault_path}/write"]
    token_metadata = mock_vault.lookup_accessor(token.accessor)
    assert token_metadata["data"]["display_name"] == token.display_name
    expire_time = token_metadata["data"]["expire_time"]
    assert datetime.fromisoformat(expire_time) == token.expires

    # Check the write policy against the proper expansion of the template.
    r = mock_vault.read_policy(token.policies[0])
    seen_policy = r["rules"]
    template = templates.get_template("vault-write-policy.hcl.jinja")
    expected_policy = template.render({"path": vault_path})
    assert seen_policy == expected_policy


def test_export_secrets(
    factory: Factory, tmp_path: Path, mock_vault: MockVaultClient
) -> None:
    input_path = phalanx_test_path()
    vault_input_path = input_path / "vault" / "idfdev"
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
    mock_vault.load_test_data(environment.vault_path_prefix, "idfdev")

    result = run_cli(
        "vault",
        "export-secrets",
        "idfdev",
        str(tmp_path),
        env={"VAULT_TOKEN": "sometoken"},
    )
    assert result.exit_code == 0
    assert result.output == ""

    assert_json_dirs_match(tmp_path, vault_input_path)
