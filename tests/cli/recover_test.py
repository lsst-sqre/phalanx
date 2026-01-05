"""Tests for the recover CLI command and subcommands."""

from subprocess import CompletedProcess
from typing import Any
from unittest.mock import Mock, call

import pytest

from ..support.cli import run_cli
from ..support.constants import DATA_DIR


def kubectl_output(filename: str) -> str:
    return (DATA_DIR / "output" / "kubectl" / filename).read_text()


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_suspend_crons_requires_context() -> None:
    result = run_cli("recover", "suspend-crons")
    assert result.exit_code == 2


def test_suspend_crons(mock_kubernetes_kubectl: Mock) -> None:
    mock = mock_kubernetes_kubectl

    def mock_capture_behavior(*args: Any) -> CompletedProcess:
        """Return fake data from calls to capture."""
        expected_args = (
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )

        if args != expected_args:
            pytest.fail(
                f"kubectl called with unexpected arguments. Expected:"
                f" {expected_args}, actual: {args}"
            )

        stdout = kubectl_output("cronjob_list.json")
        return CompletedProcess(args=args, returncode=0, stdout=stdout)

    mock.capture.side_effect = mock_capture_behavior
    result = run_cli("recover", "suspend-crons", "--context", "fake-context")
    assert result.exit_code == 0

    assert mock.run.call_args_list == [
        call(
            "patch",
            "CronJob",
            "gafaelfawr-maintenance",
            "--namespace",
            "gafaelfawr",
            "--patch",
            '{"spec" : {"suspend" : true }}',
        ),
        call(
            "patch",
            "CronJob",
            "ook-ingest-lsst-texmf",
            "--namespace",
            "ook",
            "--patch",
            '{"spec" : {"suspend" : true }}',
        ),
    ]


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_resume_crons_requires_context() -> None:
    result = run_cli("recover", "resume-crons")
    assert result.exit_code == 2


def test_resume_crons(mock_kubernetes_kubectl: Mock) -> None:
    mock = mock_kubernetes_kubectl

    def mock_capture_behavior(*args: Any) -> CompletedProcess:
        """Return fake data from calls to capture."""
        expected_args = (
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )

        if args != expected_args:
            pytest.fail(
                f"kubectl called with unexpected arguments. Expected:"
                f" {expected_args}, actual: {args}"
            )

        stdout = kubectl_output("cronjob_list.json")
        return CompletedProcess(args=args, returncode=0, stdout=stdout)

    mock.capture.side_effect = mock_capture_behavior
    result = run_cli("recover", "resume-crons", "--context", "fake-context")
    assert result.exit_code == 0

    assert mock.run.call_args_list == [
        call(
            "patch",
            "CronJob",
            "gafaelfawr-maintenance",
            "--namespace",
            "gafaelfawr",
            "--patch",
            '{"spec" : {"suspend" : false }}',
        ),
        call(
            "patch",
            "CronJob",
            "ook-ingest-lsst-texmf",
            "--namespace",
            "ook",
            "--patch",
            '{"spec" : {"suspend" : false }}',
        ),
    ]
