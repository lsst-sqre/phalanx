"""Tests for Kubernetes resource models."""

from ipaddress import AddressValueError, IPv4Address

import pytest
from syrupy.assertion import SnapshotAssertion

from phalanx.models.kubernetes import (
    CronJob,
    Deployment,
    NamespacedResourceList,
    Service,
    ServiceIPPatch,
    ServiceIPSpecPatch,
    StatefulSet,
)
from tests.support.constants import DATA_DIR


def kubectl_output(filename: str) -> str:
    return (DATA_DIR / "output" / "kubectl" / filename).read_text()


def test_cronjob_list(snapshot: SnapshotAssertion) -> None:
    out = kubectl_output("cronjob-list.json")
    expected = snapshot(name="cronjobs")
    actual = NamespacedResourceList[CronJob].model_validate_json(out)
    assert expected == actual


def test_deployment_list(snapshot: SnapshotAssertion) -> None:
    out = kubectl_output("deployment-list.json")
    expected = snapshot(name="deployments")
    actual = NamespacedResourceList[Deployment].model_validate_json(out)
    assert expected == actual


def test_statefulset_list(snapshot: SnapshotAssertion) -> None:
    out = kubectl_output("statefulset-list.json")
    expected = snapshot(name="statefulsets")
    actual = NamespacedResourceList[StatefulSet].model_validate_json(out)
    assert expected == actual


def test_loadbalancer_service_list(snapshot: SnapshotAssertion) -> None:
    out = kubectl_output("service-list.json")
    expected = snapshot(name="services")
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
