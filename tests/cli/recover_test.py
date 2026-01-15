"""Tests for the recover CLI command and subcommands."""

from dataclasses import dataclass
from subprocess import CompletedProcess

import pytest
from pytest_mock import MockerFixture
from syrupy.assertion import SnapshotAssertion

from ..support.cli import run_cli
from ..support.command import MockCommand
from ..support.constants import DATA_DIR


def kubectl_output(filename: str) -> str:
    return (DATA_DIR / "output" / "kubectl" / filename).read_text()


@dataclass
class ExpectedCaptureCall:
    """Args and response for an expected call to Command.capture."""

    args: tuple
    """The expected args."""

    response: CompletedProcess
    """The mock response."""


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_suspend_crons_requires_context() -> None:
    result = run_cli("recover", "suspend-crons")
    assert result.exit_code == 2


def test_suspend_crons(
    mock_kubernetes_kubectl: MockCommand, snapshot: SnapshotAssertion
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
        stdout=kubectl_output("cronjob-list.json"),
    )

    result = run_cli("recover", "suspend-crons", "--context", "fake-context")
    assert result.exit_code == 0

    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_resume_crons_requires_context() -> None:
    result = run_cli("recover", "resume-crons")
    assert result.exit_code == 2


def test_resume_crons(
    mock_kubernetes_kubectl: MockCommand, snapshot: SnapshotAssertion
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
        stdout=kubectl_output("cronjob-list.json"),
    )

    result = run_cli("recover", "resume-crons", "--context", "fake-context")
    assert result.exit_code == 0

    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_down_workloads_requires_context() -> None:
    result = run_cli("recover", "scale-down-workloads")
    assert result.exit_code == 2


def test_scale_down_workloads(
    mock_kubernetes_kubectl: MockCommand, snapshot: SnapshotAssertion
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
        stdout=kubectl_output("deployment-list.json"),
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
        stdout=kubectl_output("statefulset-list.json"),
    )

    result = run_cli(
        "recover", "scale-down-workloads", "--context", "fake-context"
    )
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    assert command.mock.capture.call_args_list == snapshot

    # Nothing from the argocd namespace should be in here.
    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_up_workloads_requires_context() -> None:
    result = run_cli("recover", "scale-up-workloads")
    assert result.exit_code == 2


def test_scale_up_workloads(
    mock_kubernetes_kubectl: MockCommand, snapshot: SnapshotAssertion
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
        stdout=kubectl_output("deployment-list-scaled-down.json"),
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
        stdout=kubectl_output("statefulset-list-scaled-down.json"),
    )
    result = run_cli(
        "recover", "scale-up-workloads", "--context", "fake-context"
    )
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    assert command.mock.capture.call_args_list == snapshot

    # Nothing from the argocd namespace should be in here.
    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_release_service_ips_requires_context() -> None:
    result = run_cli("recover", "release-service-ips")
    assert result.exit_code == 2


def test_release_service_ips(
    mock_kubernetes_kubectl: MockCommand,
    snapshot: SnapshotAssertion,
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
        stdout=kubectl_output("service-list.json"),
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
        stdout=kubectl_output(
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
        stdout=kubectl_output(
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
        stdout=kubectl_output(
            "service-ingress-nginx-controller-released.json"
        ),
    )

    result = run_cli(
        "recover", "release-service-ips", "--context", "fake-context"
    )

    assert result.exit_code == 0
    assert command.mock.capture.call_args_list == snapshot
    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_restore_service_ips_requires_context() -> None:
    result = run_cli("recover", "restore-service-ips")
    assert result.exit_code == 2


def test_restore_service_ips(
    mock_kubernetes_kubectl: MockCommand,
    snapshot: SnapshotAssertion,
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
        stdout=kubectl_output("service-list-released.json"),
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
        stdout=kubectl_output(
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
        stdout=kubectl_output(
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
        stdout=kubectl_output("service-ingress-nginx-controller.json"),
    )

    result = run_cli(
        "recover", "restore-service-ips", "--context", "fake-context"
    )

    assert result.exit_code == 0
    assert command.mock.capture.call_args_list == snapshot
    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_pause_kafka_requires_context() -> None:
    result = run_cli("recover", "pause-sasquatch-kafka-reconciliation")
    assert result.exit_code == 2


def test_pause_kafka(
    mock_kubernetes_kubectl: MockCommand, snapshot: SnapshotAssertion
) -> None:
    command = mock_kubernetes_kubectl

    result = run_cli(
        "recover",
        "pause-sasquatch-kafka-reconciliation",
        "--context",
        "fake-context",
    )
    assert result.exit_code == 0

    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_resume_kafka_requires_context() -> None:
    result = run_cli("recover", "resume-sasquatch-kafka-reconciliation")
    assert result.exit_code == 2


def test_resume_kafka(
    mock_kubernetes_kubectl: MockCommand, snapshot: SnapshotAssertion
) -> None:
    command = mock_kubernetes_kubectl

    result = run_cli(
        "recover",
        "resume-sasquatch-kafka-reconciliation",
        "--context",
        "fake-context",
    )
    assert result.exit_code == 0

    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_down_requires_context() -> None:
    result = run_cli("recover", "scale-down")
    assert result.exit_code == 2


def test_scale_down(
    mock_kubernetes_kubectl: MockCommand,
    snapshot: SnapshotAssertion,
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
        stdout=kubectl_output("service-list.json"),
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
        stdout=kubectl_output(
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
        stdout=kubectl_output(
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
        stdout=kubectl_output(
            "service-ingress-nginx-controller-released.json"
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
        stdout=kubectl_output("cronjob-list.json"),
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
        stdout=kubectl_output("deployment-list.json"),
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
        stdout=kubectl_output("statefulset-list.json"),
    )

    result = run_cli("recover", "scale-down", "--context", "fake-context")
    assert result.exit_code == 0

    assert command.mock.capture.call_args_list == snapshot
    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_up_requires_context() -> None:
    result = run_cli("recover", "scale-up")
    assert result.exit_code == 2


def test_scale_up(
    mock_kubernetes_kubectl: MockCommand,
    snapshot: SnapshotAssertion,
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
        stdout=kubectl_output("service-list-released.json"),
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
        stdout=kubectl_output(
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
        stdout=kubectl_output(
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
        stdout=kubectl_output("service-ingress-nginx-controller.json"),
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
        stdout=kubectl_output("deployment-list-scaled-down.json"),
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
        stdout=kubectl_output("statefulset-list-scaled-down.json"),
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
        stdout=kubectl_output("cronjob-list.json"),
    )

    result = run_cli("recover", "scale-up", "--context", "fake-context")
    assert result.exit_code == 0

    assert command.mock.capture.call_args_list == snapshot
    assert command.mock.run.call_args_list == snapshot


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def restore_requires_both_contexts() -> None:
    result = run_cli("recover", "restore")
    assert result.exit_code == 2

    result = run_cli("recover", "restore", "--old-context", "fake-old-context")
    assert result.exit_code == 2

    result = run_cli("recover", "restore", "--new-context", "fake-new-context")
    assert result.exit_code == 2
