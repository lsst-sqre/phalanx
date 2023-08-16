"""Tests for the vault command-line subcommand."""

from __future__ import annotations

import re
from datetime import datetime, timedelta

import jinja2
import yaml
from click.testing import CliRunner
from safir.datetime import current_datetime

from phalanx.cli import main
from phalanx.constants import VAULT_WRITE_TOKEN_LIFETIME
from phalanx.factory import Factory
from phalanx.models.vault import VaultAppRole, VaultToken

from ..support.data import read_output_data
from ..support.vault import MockVaultClient


def test_audit(factory: Factory, mock_vault: MockVaultClient) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)
    _, role_name = vault_path.rsplit("/", 1)

    runner = CliRunner()

    # Nothing has been created, so audit will report both missing.
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-both-missing")

    # Create an AppRole with the wrong policy and the wrong list of policies.
    mock_vault.create_or_update_policy(f"{vault_path}/read", "blah blah blah")
    mock_vault.create_or_update_approle(
        role_name, token_policies=["something"], token_type="service"
    )
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
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
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-approle-extra")

    # Fix the AppRole again, and create a write token with the wrong policies
    # and a write policy with the wrong contents.
    vault_service.create_read_approle("idfdev")
    r = mock_vault.create(
        display_name=role_name,
        policies=["something"],
        ttl=VAULT_WRITE_TOKEN_LIFETIME,
    )
    accessor = r["auth"]["accessor"]
    mock_vault.create_or_update_policy(f"{vault_path}/write", "blah blah blah")
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 1
    assert result.output == read_output_data("idfdev", "audit-token-policy")

    # Create a new token that expires in six days and use that to fix the
    # policy. The old token should still exist and produce the same warnings,
    # except for the incorrect write policy, and there should be a new warning
    # about the token expiring within seven days. We have to do some munging
    # here of the output since the date and time will vary.
    vault_service.create_write_token("idfdev", "6d")
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 1
    output = re.sub(r"[\d-]{10} [\d:]{8}", "<timestamp>", result.output)
    assert output == read_output_data("idfdev", "audit-token-multiple")

    # Delete the manually-created token and make a new one that is already
    # expired.
    mock_vault.revoke_accessor(accessor)
    r = mock_vault.create(
        display_name=role_name,
        policies=[f"{vault_path}/write"],
        ttl=VAULT_WRITE_TOKEN_LIFETIME,
        create_expired_token=True,
    )
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 1
    output = re.sub(r"[\d-]{10} [\d:]{8}", "<timestamp>", result.output)
    assert output == read_output_data("idfdev", "audit-token-expired")


def test_audit_clean(factory: Factory, mock_vault: MockVaultClient) -> None:
    vault_service = factory.create_vault_service()
    vault_service.create_read_approle("idfdev")
    vault_service.create_write_token("idfdev", VAULT_WRITE_TOKEN_LIFETIME)

    runner = CliRunner()
    result = runner.invoke(
        main, ["vault", "audit", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == ""


def test_create_read_approle(
    factory: Factory,
    mock_vault: MockVaultClient,
    templates: jinja2.Environment,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["vault", "create-read-approle", "idfdev"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    approle = VaultAppRole.parse_obj(yaml.safe_load(result.output))

    # Check that the AppRole was created with the right RoleID and policies.
    assert approle.policies == [f"{vault_path}/read"]
    _, role_name = vault_path.rsplit("/", 1)
    r = mock_vault.read_role_id(role_name)
    assert r["data"]["role_id"] == approle.role_id

    # Check the read policy against the proper expansion of the template.
    r = mock_vault.read_policy(approle.policies[0])
    seen_policy = r["rules"]
    template = templates.get_template("vault-read-policy.tmpl")
    expected_policy = template.render({"path": vault_path})
    assert seen_policy == expected_policy


def test_create_write_token(
    factory: Factory,
    mock_vault: MockVaultClient,
    templates: jinja2.Environment,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment_config("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)
    if "/" in vault_path:
        _, display_name = vault_path.rsplit("/", 1)
    else:
        display_name = vault_path
    lifetime = timedelta(days=int(VAULT_WRITE_TOKEN_LIFETIME[:-1]))
    expires = current_datetime() + lifetime

    runner = CliRunner()
    result = runner.invoke(
        main, ["vault", "create-write-token", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    token = VaultToken.parse_obj(yaml.safe_load(result.output))
    assert token.display_name == display_name
    assert expires - timedelta(seconds=5) <= token.expires <= expires
    assert token.policies == [f"{vault_path}/write"]
    token_metadata = mock_vault.lookup_accessor(token.accessor)
    assert token_metadata["data"]["display_name"] == token.display_name
    expire_time = token_metadata["data"]["expire_time"]
    assert datetime.fromisoformat(expire_time) == token.expires

    # Check the write policy against the proper expansion of the template.
    r = mock_vault.read_policy(token.policies[0])
    seen_policy = r["rules"]
    template = templates.get_template("vault-write-policy.tmpl")
    expected_policy = template.render({"path": vault_path})
    assert seen_policy == expected_policy
