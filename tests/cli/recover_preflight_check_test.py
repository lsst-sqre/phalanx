"""Tests for recover preflight-check."""

import pytest

from ..support.cli import run_cli
from ..support.data import PhalanxData
from ..support.recover import MockRecover

ENVIRONMENT_NAME = "idfdev"
COMMAND = (
    "recover",
    "preflight-check",
    "--vault-role-id",
    "some-vault-role-id",
    "--vault-secret-id",
    "some-vault-secret-id",
    "--git-branch",
    "main",
    "--environment",
    ENVIRONMENT_NAME,
    "--new-context",
    "some-new-context",
    "--old-context",
    "some-old-context",
    "--gke-region",
    "some-gke-region",
    "--gke-project",
    "some-gke-project",
    "--source-cluster",
    "some-source-cluster",
    "--destination-cluster",
    "some-destination-cluster",
)
"""The preflight-check command"""


@pytest.mark.usefixtures("mock_kubectl")
@pytest.mark.usefixtures("mock_which")
def test_requires_both_contexts() -> None:
    result = run_cli("recover", "preflight-check")
    assert result.exit_code == 2

    args = ["recover", "preflight-check", "--old-context", "fake-old-context"]
    result = run_cli(*args)
    assert result.exit_code == 2

    args = ["recover", "preflight-check", "--new-context", "fake-new-context"]
    result = run_cli(*args)
    assert result.exit_code == 2


def test_fails_cluster_connect_source(
    mock_recover: MockRecover, mock_which: None, data: PhalanxData
) -> None:
    mock_recover.mock_connect_check(fail_source=True)
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(
        result.output, "recover/preflight-check/connect-source"
    )
    mock_recover.assert_run_calls("preflight-cluster-connect-source")


def test_fails_cluster_connect_destination(
    mock_recover: MockRecover, mock_which: None, data: PhalanxData
) -> None:
    mock_recover.mock_connect_check(fail_destination=True)
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(
        result.output, "recover/preflight-check/connect-destination"
    )
    mock_recover.assert_run_calls("preflight-cluster-connect-destination")


def test_fails_cluster_connect_both(
    mock_recover: MockRecover, mock_which: None, data: PhalanxData
) -> None:
    mock_recover.mock_connect_check(fail_source=True, fail_destination=True)
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(
        result.output, "recover/preflight-check/connect-both"
    )
    mock_recover.assert_run_calls("preflight-cluster-connect-both")


def test_fails_static_ip(
    mock_recover: MockRecover,
    mock_which: None,
    data: PhalanxData,
) -> None:
    mock_recover.mock_connect_check()
    mock_recover.mock_static_ip_check(fail=True)
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(
        result.output, "recover/preflight-check/static-ip"
    )
    mock_recover.assert_run_calls("preflight-static-ip")


def test_fails_firewall_rule_ip(
    mock_recover: MockRecover,
    mock_which: None,
    data: PhalanxData,
) -> None:
    mock_recover.mock_connect_check()
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check(fail_ips=True)
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(
        result.output, "recover/preflight-check/firewall-ip"
    )
    mock_recover.assert_run_calls("preflight-firewall-ip")


def test_fails_firewall_rule_tag(
    mock_recover: MockRecover, mock_which: None, data: PhalanxData
) -> None:
    mock_recover.mock_connect_check()
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check(fail_tags=True)
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(
        result.output, "recover/preflight-check/firewall-tag"
    )
    mock_recover.assert_run_calls("preflight-firewall-tag")


def test_fails_argocd(
    mock_recover: MockRecover, mock_which: None, data: PhalanxData
) -> None:
    mock_recover.mock_connect_check()
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME, fail=True)

    result = run_cli(*COMMAND)

    assert result.exit_code == 1
    data.assert_text_matches(result.output, "recover/preflight-check/argocd")
    mock_recover.assert_run_calls("preflight-argocd")


def test_succeeds(
    mock_recover: MockRecover, mock_which: None, data: PhalanxData
) -> None:
    mock_recover.mock_connect_check()
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    result = run_cli(*COMMAND)

    assert result.exit_code == 0
    data.assert_text_matches(result.output, "recover/preflight-check/succeeds")
    mock_recover.assert_run_calls("preflight-preflight-check-succeeds")
