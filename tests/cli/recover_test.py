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
        "suspend-crons",
        "resume-crons",
        "scale-down-workloads",
        "scale-up-workloads",
        "release-service-ips",
        "restore-service-ips",
        "pause-sasquatch-kafka-reconciliation",
        "resume-sasquatch-kafka-reconciliation",
        "scale-down",
        "scale-up",
    ):
        result = run_cli("recover", command)
        assert result.exit_code == 2


def test_suspend_crons(
    data: PhalanxData, mock_kubernetes_kubectl: MockCommand
) -> None:
    command = mock_kubernetes_kubectl
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
        stdout=data.read_text("kubectl/cronjob-list.json"),
    )

    result = run_cli("recover", "suspend-crons", "--context", "fake-context")
    assert result.exit_code == 0
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/suspend-crons"
    )


def test_resume_crons(
    data: PhalanxData, mock_kubernetes_kubectl: MockCommand
) -> None:
    command = mock_kubernetes_kubectl
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
        stdout=data.read_text("kubectl/cronjob-list.json"),
    )

    result = run_cli("recover", "resume-crons", "--context", "fake-context")
    assert result.exit_code == 0
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/resume-crons"
    )


def test_scale_down_workloads(
    data: PhalanxData, mock_kubernetes_kubectl: MockCommand
) -> None:
    command = mock_kubernetes_kubectl

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
        stdout=data.read_text("kubectl/deployment-list.json"),
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
        stdout=data.read_text("kubectl/statefulset-list.json"),
    )

    result = run_cli(
        "recover", "scale-down-workloads", "--context", "fake-context"
    )
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    data.assert_calls_match(
        command.mock.capture.call_args_list,
        "recover/scale-down-workloads-capture",
    )

    # Nothing from the argocd namespace should be in here.
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/scale-down-workloads-run"
    )


def test_scale_up_workloads(
    data: PhalanxData, mock_kubernetes_kubectl: MockCommand
) -> None:
    command = mock_kubernetes_kubectl

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
        stdout=data.read_text("kubectl/deployment-list-scaled-down.json"),
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
        stdout=data.read_text("kubectl/statefulset-list-scaled-down.json"),
    )
    result = run_cli(
        "recover", "scale-up-workloads", "--context", "fake-context"
    )
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    data.assert_calls_match(
        command.mock.capture.call_args_list,
        "recover/scale-up-workloads-capture",
    )

    # Nothing from the argocd namespace should be in here.
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/scale-up-workloads-run"
    )


def test_release_service_ips(
    data: PhalanxData,
    mock_kubernetes_kubectl: MockCommand,
    mocker: MockerFixture,
) -> None:
    mocker.patch("time.sleep")
    command = mock_kubernetes_kubectl

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
        stdout=data.read_text("kubectl/service-list.json"),
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
        stdout=data.read_text(
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
        stdout=data.read_text(
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
        stdout=data.read_text(
            "kubectl/service-ingress-nginx-controller-released.json"
        ),
    )

    result = run_cli(
        "recover", "release-service-ips", "--context", "fake-context"
    )

    assert result.exit_code == 0
    data.assert_calls_match(
        command.mock.capture.call_args_list,
        "recover/release-service-ips-capture",
    )
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/release-service-ips-run"
    )


def test_restore_service_ips(
    data: PhalanxData,
    mock_kubernetes_kubectl: MockCommand,
    mocker: MockerFixture,
) -> None:
    mocker.patch("time.sleep")
    command = mock_kubernetes_kubectl

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
        stdout=data.read_text("kubectl/service-list-released.json"),
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
        stdout=data.read_text(
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
        stdout=data.read_text(
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
        stdout=data.read_text("kubectl/service-ingress-nginx-controller.json"),
    )

    result = run_cli(
        "recover", "restore-service-ips", "--context", "fake-context"
    )

    assert result.exit_code == 0
    data.assert_calls_match(
        command.mock.capture.call_args_list,
        "recover/restore-service-ips-capture",
    )
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/restore-service-ips-run"
    )


def test_pause_kafka(
    data: PhalanxData, mock_kubernetes_kubectl: MockCommand
) -> None:
    command = mock_kubernetes_kubectl

    result = run_cli(
        "recover",
        "pause-sasquatch-kafka-reconciliation",
        "--context",
        "fake-context",
    )
    assert result.exit_code == 0
    data.assert_calls_match(
        command.mock.run.call_args_list,
        "recover/pause-sasquatch-kafka-reconciliation",
    )


def test_resume_kafka(
    data: PhalanxData, mock_kubernetes_kubectl: MockCommand
) -> None:
    command = mock_kubernetes_kubectl

    result = run_cli(
        "recover",
        "resume-sasquatch-kafka-reconciliation",
        "--context",
        "fake-context",
    )
    assert result.exit_code == 0
    data.assert_calls_match(
        command.mock.run.call_args_list,
        "recover/resume-sasquatch-kafka-reconciliation",
    )


def test_scale_down(
    data: PhalanxData,
    mock_kubernetes_kubectl: MockCommand,
    mocker: MockerFixture,
) -> None:
    mocker.patch("time.sleep")
    command = mock_kubernetes_kubectl

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
        stdout=data.read_text("kubectl/service-list.json"),
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
        stdout=data.read_text(
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
        stdout=data.read_text(
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
        stdout=data.read_text(
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
        stdout=data.read_text("kubectl/cronjob-list.json"),
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
        stdout=data.read_text("kubectl/deployment-list.json"),
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
        stdout=data.read_text("kubectl/statefulset-list.json"),
    )

    result = run_cli("recover", "scale-down", "--context", "fake-context")
    assert result.exit_code == 0

    data.assert_calls_match(
        command.mock.capture.call_args_list, "recover/scale-down-capture"
    )
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/scale-down-run"
    )


def test_scale_up(
    data: PhalanxData,
    mock_kubernetes_kubectl: MockCommand,
    mocker: MockerFixture,
) -> None:
    mocker.patch("time.sleep")
    command = mock_kubernetes_kubectl

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
        stdout=data.read_text("kubectl/service-list-released.json"),
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
        stdout=data.read_text(
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
        stdout=data.read_text(
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
        stdout=data.read_text("kubectl/service-ingress-nginx-controller.json"),
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
        stdout=data.read_text("kubectl/deployment-list-scaled-down.json"),
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
        stdout=data.read_text("kubectl/statefulset-list-scaled-down.json"),
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
        stdout=data.read_text("kubectl/cronjob-list.json"),
    )

    result = run_cli("recover", "scale-up", "--context", "fake-context")
    assert result.exit_code == 0

    data.assert_calls_match(
        command.mock.capture.call_args_list, "recover/scale-up-capture"
    )
    data.assert_calls_match(
        command.mock.run.call_args_list, "recover/scale-up-run"
    )
