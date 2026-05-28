"""Tests for the recover CLI command and subcommands."""

from dataclasses import dataclass
from subprocess import CompletedProcess

import pytest
from pytest_mock import MockerFixture

from ..support.cli import run_cli
from ..support.command import MockCommand
from ..support.data import PhalanxData


@dataclass
class ExpectedCaptureCall:
    """Args and response for an expected call to Command.capture."""

    args: tuple
    """The expected args."""

    response: CompletedProcess
    """The mock response."""


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_requires_context() -> None:
    for command in (
        "scale-down",
        "scale-up",
    ):
        result = run_cli("recover", command)
        assert result.exit_code == 2


def test_scale_down(
    data: PhalanxData,
    mock_kubectl: MockCommand,
    mocker: MockerFixture,
) -> None:
    mocker.patch("time.sleep")
    command = mock_kubectl

    command.expect_capture(
        args=(
            "get",
            "Service",
            "--field-selector",
            "spec.type=LoadBalancer",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/service-list.json"),
    )
    command.expect_capture(
        args=(
            "get",
            "Service",
            "ingress-nginx-controller",
            "--namespace",
            "ingress-nginx",
            "-o",
            "json",
        ),
        response=data.read_text(
            "kubectl/"
            "service-ingress-nginx-controller-cluster-ip-with-finalizers.json"
        ),
    )
    command.expect_capture(
        args=(
            "get",
            "Service",
            "ingress-nginx-controller",
            "--namespace",
            "ingress-nginx",
            "-o",
            "json",
        ),
        response=data.read_text(
            "kubectl/"
            "service-ingress-nginx-controller-cluster-ip-without-finalizers.json"
        ),
    )
    command.expect_capture(
        args=(
            "get",
            "Service",
            "ingress-nginx-controller",
            "--namespace",
            "ingress-nginx",
            "-o",
            "json",
        ),
        response=data.read_text(
            "kubectl/service-ingress-nginx-controller-released.json"
        ),
    )
    command.expect_capture(
        args=(
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/cronjob-list.json"),
    )
    command.expect_capture(
        args=(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/deployment-list.json"),
    )
    command.expect_capture(
        args=(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/statefulset-list.json"),
    )

    result = run_cli("recover", "scale-down", "--context", "fake-context")
    assert result.exit_code == 0

    data.assert_calls_match(
        command.mock.capture.call_args_list, "recover/scale-down-capture"
    )
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/scale-down-run"
    )


@pytest.mark.usefixtures("mock_kubectl")
def test_scale_up_requires_context() -> None:
    result = run_cli("recover", "scale-up")
    assert result.exit_code == 2


def test_scale_up(
    data: PhalanxData,
    mock_kubectl: MockCommand,
    mocker: MockerFixture,
) -> None:
    mocker.patch("time.sleep")
    command = mock_kubectl

    command.expect_capture(
        args=(
            "get",
            "Service",
            "--field-selector",
            "spec.type=LoadBalancer",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/service-list-released.json"),
    )
    command.expect_capture(
        args=(
            "get",
            "Service",
            "ingress-nginx-controller",
            "--namespace",
            "ingress-nginx",
            "-o",
            "json",
        ),
        response=data.read_text(
            "kubectl/"
            "service-ingress-nginx-controller-released-cluster-ip-with-finalizers.json"
        ),
    )
    command.expect_capture(
        args=(
            "get",
            "Service",
            "ingress-nginx-controller",
            "--namespace",
            "ingress-nginx",
            "-o",
            "json",
        ),
        response=data.read_text(
            "kubectl/"
            "service-ingress-nginx-controller-released-cluster-ip-without-finalizers.json"
        ),
    )
    command.expect_capture(
        args=(
            "get",
            "Service",
            "ingress-nginx-controller",
            "--namespace",
            "ingress-nginx",
            "-o",
            "json",
        ),
        response=data.read_text(
            "kubectl/service-ingress-nginx-controller.json"
        ),
    )
    command.expect_capture(
        args=(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/deployment-list-scaled-down.json"),
    )
    command.expect_capture(
        args=(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/statefulset-list-scaled-down.json"),
    )
    command.expect_capture(
        args=(
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        response=data.read_text("kubectl/cronjob-list.json"),
    )

    result = run_cli("recover", "scale-up", "--context", "fake-context")
    assert result.exit_code == 0

    data.assert_calls_match(
        command.mock.capture.call_args_list, "recover/scale-up-capture"
    )
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/scale-up-run"
    )


@pytest.mark.usefixtures("mock_kubectl")
def test_restore_requires_both_contexts() -> None:
    result = run_cli("recover", "restore")
    assert result.exit_code == 2

    result = run_cli("recover", "restore", "--old-context", "fake-old-context")
    assert result.exit_code == 2

    result = run_cli("recover", "restore", "--new-context", "fake-new-context")
    assert result.exit_code == 2
