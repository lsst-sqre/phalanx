"""Tests for the vault command-line subcommand."""

from __future__ import annotations

import jinja2
import yaml
from click.testing import CliRunner

from phalanx.cli import main
from phalanx.factory import Factory
from phalanx.models.vault import VaultAppRole, VaultToken

from ..support.vault import MockVaultClient


def test_create_read_approle(
    factory: Factory,
    mock_vault: MockVaultClient,
    templates: jinja2.Environment,
) -> None:
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("idfdev")
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
    environment = config_storage.load_environment("idfdev")
    _, vault_path = environment.vault_path_prefix.split("/", 1)

    runner = CliRunner()
    result = runner.invoke(
        main, ["vault", "create-write-token", "idfdev"], catch_exceptions=False
    )
    assert result.exit_code == 0
    token = VaultToken.parse_obj(yaml.safe_load(result.output))
    assert token.policies == [f"{vault_path}/write"]
    assert token.token in {t.token for t in mock_vault.vault_tokens}

    # Check the write policy against the proper expansion of the template.
    r = mock_vault.read_policy(token.policies[0])
    seen_policy = r["rules"]
    template = templates.get_template("vault-write-policy.tmpl")
    expected_policy = template.render({"path": vault_path})
    assert seen_policy == expected_policy
