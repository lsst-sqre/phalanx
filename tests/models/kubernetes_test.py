"""Tests for Kubernetes resource models."""

from phalanx.models.kubernetes import (
    CronJob,
    Deployment,
    ResourceList,
    StatefulSet,
)
from tests.support.constants import DATA_DIR


def kubectl_output(filename: str) -> str:
    return (DATA_DIR / "output" / "kubectl" / filename).read_text()


def test_cronjob_list() -> None:
    out = kubectl_output("cronjob_list.json")
    expected = ResourceList(
        kind="List",
        items=[
            CronJob(
                kind="CronJob",
                namespace="gafaelfawr",
                name="gafaelfawr-maintenance",
            ),
            CronJob(
                kind="CronJob", namespace="ook", name="ook-ingest-lsst-texmf"
            ),
        ],
    )

    actual = ResourceList[CronJob].model_validate_json(out)

    assert expected == actual


def test_deployment_list() -> None:
    out = kubectl_output("deployment_list.json")
    expected = ResourceList(
        kind="List",
        items=[
            Deployment(
                kind="Deployment",
                namespace="gafaelfawr",
                name="gafaelfawr",
                replicas=1,
            ),
            Deployment(
                kind="Deployment",
                namespace="gafaelfawr",
                name="gafaelfawr-operator",
                replicas=1,
            ),
            Deployment(
                kind="Deployment",
                namespace="argocd",
                name="argocd",
                replicas=1,
            ),
        ],
    )

    actual = ResourceList[Deployment].model_validate_json(out)

    assert expected == actual


def test_statefulset_list() -> None:
    out = kubectl_output("statefulset_list.json")
    expected = ResourceList(
        kind="List",
        items=[
            StatefulSet(
                kind="StatefulSet",
                namespace="gafaelfawr",
                name="gafaelfawr-redis",
                replicas=1,
            ),
            StatefulSet(
                kind="StatefulSet",
                namespace="gafaelfawr",
                name="gafaelfawr-redis-ephemeral",
                replicas=1,
            ),
            StatefulSet(
                kind="StatefulSet",
                namespace="argocd",
                name="argocd",
                replicas=1,
            ),
        ],
    )

    actual = ResourceList[StatefulSet].model_validate_json(out)

    assert expected == actual
