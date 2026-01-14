"""Tests for the recover CLI command and subcommands."""

from dataclasses import dataclass
from subprocess import CompletedProcess
from unittest.mock import call

import pytest

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


def test_suspend_crons(mock_kubernetes_kubectl: MockCommand) -> None:
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
        stdout=kubectl_output("cronjob_list.json"),
    )

    result = run_cli("recover", "suspend-crons", "--context", "fake-context")
    assert result.exit_code == 0

    assert command.mock.run.call_args_list == [
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


def test_resume_crons(mock_kubernetes_kubectl: MockCommand) -> None:
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
        stdout=kubectl_output("cronjob_list.json"),
    )

    result = run_cli("recover", "resume-crons", "--context", "fake-context")
    assert result.exit_code == 0

    assert command.mock.run.call_args_list == [
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


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_down_workloads_requires_context() -> None:
    result = run_cli("recover", "scale-down-workloads")
    assert result.exit_code == 2


def test_scale_down_workloads(mock_kubernetes_kubectl: MockCommand) -> None:
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
        stdout=kubectl_output("deployment_list.json"),
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
        stdout=kubectl_output("statefulset_list.json"),
    )

    result = run_cli(
        "recover", "scale-down-workloads", "--context", "fake-context"
    )
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    assert command.mock.capture.call_args_list == [
        call(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        call(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
    ]

    # Nothing from the argocd namespace should be in here.
    assert command.mock.run.call_args_list == [
        call(
            "annotate",
            "Deployment",
            "gafaelfawr",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "Deployment/gafaelfawr",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "Deployment",
            "gafaelfawr-operator",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "Deployment/gafaelfawr-operator",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis-ephemeral",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis-ephemeral",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
    ]


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_up_workloads_requires_context() -> None:
    result = run_cli("recover", "scale-up-workloads")
    assert result.exit_code == 2


def test_scale_up_workloads(mock_kubernetes_kubectl: MockCommand) -> None:
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
        stdout=kubectl_output("deployment_list_scaled_down.json"),
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
        stdout=kubectl_output("statefulset_list_scaled_down.json"),
    )
    result = run_cli(
        "recover", "scale-up-workloads", "--context", "fake-context"
    )
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    assert command.mock.capture.call_args_list == [
        call(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        call(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
    ]

    # Nothing from the argocd namespace should be in here.
    assert command.mock.run.call_args_list == [
        call(
            "scale",
            "Deployment/gafaelfawr",
            "--replicas",
            "1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "Deployment",
            "gafaelfawr",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "Deployment/gafaelfawr-operator",
            "--replicas",
            "2",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "Deployment",
            "gafaelfawr-operator",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis",
            "--replicas",
            "4",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis-ephemeral",
            "--replicas",
            "5",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis-ephemeral",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
    ]


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_down_requires_context() -> None:
    result = run_cli("recover", "scale-down")
    assert result.exit_code == 2


def test_scale_down(mock_kubernetes_kubectl: MockCommand) -> None:
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
        stdout=kubectl_output("cronjob_list.json"),
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
        stdout=kubectl_output("deployment_list.json"),
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
        stdout=kubectl_output("statefulset_list.json"),
    )

    result = run_cli("recover", "scale-down", "--context", "fake-context")
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    assert command.mock.capture.call_args_list == [
        call(
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        call(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        call(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
    ]

    # Nothing from the argocd namespace should be in here.
    assert command.mock.run.call_args_list == [
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
        call(
            "annotate",
            "Deployment",
            "gafaelfawr",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "Deployment/gafaelfawr",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "Deployment",
            "gafaelfawr-operator",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "Deployment/gafaelfawr-operator",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis-ephemeral",
            "phalanx.lsst.org/previous-replica-count=1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis-ephemeral",
            "--replicas",
            "0",
            "--namespace",
            "gafaelfawr",
        ),
    ]


@pytest.mark.usefixtures("mock_kubernetes_kubectl")
def test_scale_up_requires_context() -> None:
    result = run_cli("recover", "scale-up")
    assert result.exit_code == 2


def test_scale_up(mock_kubernetes_kubectl: MockCommand) -> None:
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
        stdout=kubectl_output("deployment_list_scaled_down.json"),
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
        stdout=kubectl_output("statefulset_list_scaled_down.json"),
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
        stdout=kubectl_output("cronjob_list.json"),
    )

    result = run_cli("recover", "scale-up", "--context", "fake-context")
    assert result.exit_code == 0

    # Assert exactly these calls to capture were made
    assert command.mock.capture.call_args_list == [
        call(
            "get",
            "Deployment",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        call(
            "get",
            "StatefulSet",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
        call(
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        ),
    ]

    # Nothing from the argocd namespace should be in here.
    assert command.mock.run.call_args_list == [
        call(
            "scale",
            "Deployment/gafaelfawr",
            "--replicas",
            "1",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "Deployment",
            "gafaelfawr",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "Deployment/gafaelfawr-operator",
            "--replicas",
            "2",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "Deployment",
            "gafaelfawr-operator",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis",
            "--replicas",
            "4",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "scale",
            "StatefulSet/gafaelfawr-redis-ephemeral",
            "--replicas",
            "5",
            "--namespace",
            "gafaelfawr",
        ),
        call(
            "annotate",
            "StatefulSet",
            "gafaelfawr-redis-ephemeral",
            "phalanx.lsst.org/previous-replica-count-",
            "--namespace",
            "gafaelfawr",
        ),
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
