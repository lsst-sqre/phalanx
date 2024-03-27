"""Tests for the environment command-line subcommand."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..support.cli import run_cli
from ..support.data import phalanx_test_path
from ..support.helm import MockHelmCommand


def test_lint(mock_helm: MockHelmCommand) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = (
                "==> Linting .\n"
                "[INFO] Chart.yaml: icon is recommended\n"
                "\n"
                "1 chart(s) linted, 0 chart(s) failed\n"
            )
        return subprocess.CompletedProcess(
            returncode=0,
            args=command,
            stdout=output,
            stderr=None,
        )

    # Lint a single environment and check that the output is filtered.
    mock_helm.set_capture_callback(callback)
    result = run_cli("environment", "lint", "idfdev")
    expected = "==> Linting top-level chart for idfdev\n"
    assert result.output == expected
    assert result.exit_code == 0
    assert mock_helm.call_args_list == [
        [
            "lint",
            "environments",
            "--strict",
            "--values",
            "environments/values.yaml",
            "--values",
            "environments/values-idfdev.yaml",
        ]
    ]

    # Lint all environments.
    mock_helm.reset_mock()
    result = run_cli("environment", "lint")
    expected += (
        "==> Linting top-level chart for minikube\n"
        "==> Linting top-level chart for usdfdev-prompt-processing\n"
    )
    assert result.output == expected
    assert result.exit_code == 0
    assert mock_helm.call_args_list == [
        [
            "lint",
            "environments",
            "--strict",
            "--values",
            "environments/values.yaml",
            "--values",
            "environments/values-idfdev.yaml",
        ],
        [
            "lint",
            "environments",
            "--strict",
            "--values",
            "environments/values.yaml",
            "--values",
            "environments/values-minikube.yaml",
        ],
        [
            "lint",
            "environments",
            "--strict",
            "--values",
            "environments/values.yaml",
            "--values",
            "environments/values-usdfdev-prompt-processing.yaml",
        ],
    ]

    def callback_error(*command: str) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(
            returncode=1,
            args=command,
            stdout="",
            stderr="Some error\n",
        )

    # Test with an error.
    mock_helm.reset_mock()
    mock_helm.set_capture_callback(callback_error)
    result = run_cli("environment", "lint", "idfdev")
    assert result.output == (
        "Some error\n"
        "Error: Top-level chart for environment idfdev has errors\n"
    )
    assert result.exit_code == 1


def test_schema() -> None:
    result = run_cli("environment", "schema", needs_config=False)
    assert result.exit_code == 0
    current = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "extras"
        / "schemas"
        / "environment.json"
    )
    assert result.output == current.read_text()


def test_template(mock_helm: MockHelmCommand) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "template":
            output = "this is some template\n"
        return subprocess.CompletedProcess(
            returncode=0, args=command, stdout=output, stderr=None
        )

    mock_helm.set_capture_callback(callback)
    result = run_cli("environment", "template", "idfdev")
    assert result.output == "this is some template\n"
    assert result.exit_code == 0
    assert mock_helm.call_args_list == [
        [
            "template",
            "science-platform",
            str(phalanx_test_path() / "environments"),
            "--include-crds",
            "--values",
            "environments/values.yaml",
            "--values",
            "environments/values-idfdev.yaml",
        ],
    ]
