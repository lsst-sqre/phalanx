"""Tests for Kubernetes resource models."""

from ipaddress import AddressValueError, IPv4Address

import pytest

from phalanx.models.kubernetes import (
    CronJob,
    Deployment,
    NamespacedResourceList,
    Service,
    ServiceExternalTrafficPolicy,
    ServiceIPPatch,
    ServiceIPSpecPatch,
    StatefulSet,
)
from tests.support.constants import DATA_DIR


def kubectl_output(filename: str) -> str:
    return (DATA_DIR / "output" / "kubectl" / filename).read_text()


def test_cronjob_list() -> None:
    out = kubectl_output("cronjob-list.json")
    expected = NamespacedResourceList(
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

    actual = NamespacedResourceList[CronJob].model_validate_json(out)

    assert expected == actual


def test_deployment_list() -> None:
    out = kubectl_output("deployment-list.json")
    expected = NamespacedResourceList(
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

    actual = NamespacedResourceList[Deployment].model_validate_json(out)

    assert expected == actual


def test_statefulset_list() -> None:
    out = kubectl_output("statefulset-list.json")
    expected = NamespacedResourceList(
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

    actual = NamespacedResourceList[StatefulSet].model_validate_json(out)

    assert expected == actual


def test_loadbalancer_service_list() -> None:
    out = kubectl_output("service-list.json")
    expected = NamespacedResourceList[Service](
        items=[
            Service(
                kind="Service",
                namespace="ingress-nginx",
                name="ingress-nginx-controller",
                finalizers=[
                    "gke.networking.io/l4-netlb-v1",
                    "service.kubernetes.io/load-balancer-cleanup",
                ],
                previous_loadbalancer_ip=None,
                previous_external_traffic_policy=None,
                external_traffic_policy=ServiceExternalTrafficPolicy.LOCAL,
                load_balancer_ip=IPv4Address("35.225.112.77"),
                status_load_balancer_ip=IPv4Address("35.225.112.77"),
            )
        ],
        kind="List",
    )

    actual = NamespacedResourceList[Service].model_validate_json(out)

    assert expected == actual


def test_loadbalancer_service_patch() -> None:
    # This should work
    _ = ServiceIPPatch(
        spec=ServiceIPSpecPatch(load_balancer_ip=IPv4Address("1.2.3.4"))
    )

    with pytest.raises(AddressValueError):
        _ = ServiceIPPatch(
            spec=ServiceIPSpecPatch(
                load_balancer_ip=IPv4Address("something malicious injection")
            )
        )
