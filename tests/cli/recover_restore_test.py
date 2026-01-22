"""Tests for recover restore."""

from pathlib import Path

from pytest_mock.plugin import MockerFixture

from ..support.cli import run_cli
from ..support.data import PhalanxData
from ..support.recover import MockRecover

ENVIRONMENT_NAME = "idfdev"
COMMAND = (
    "recover",
    "restore",
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
    "--run-id",
    "some-run-id",
)
"""The restore command"""


def test_succeeds(
    mock_recover: MockRecover,
    mock_which: MockerFixture,
    data: PhalanxData,
    real_git_repo: Path,
) -> None:
    # Mock the preflight check
    mock_recover.mock_connect_check()
    mock_recover.mock_static_ip_check()
    mock_recover.mock_firewall_check()
    mock_recover.mock_source_sync_check(ENVIRONMENT_NAME)

    # Mock everything in the universe
    mock_recover.mock_happy_restore()

    result = run_cli(
        *COMMAND, "--config", str(real_git_repo), needs_config=False
    )

    assert result.exit_code == 0
    mock_recover.assert_run_calls("restore-succeeds")
