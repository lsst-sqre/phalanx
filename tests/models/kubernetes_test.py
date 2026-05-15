"""Tests for Kubernetes resource models."""

from ipaddress import AddressValueError, IPv4Address

import pytest

from phalanx.models.kubernetes import (
    CronJob,
    Deployment,
    ResourceList,
    Service,
    ServiceIPPatch,
    ServiceIPSpecPatch,
    StatefulSet,
)

from ..support.data import PhalanxData


def test_cronjob_list(data: PhalanxData) -> None:
    out = data.read_text("kubectl/cronjob-list.json")
    actual = ResourceList[CronJob].model_validate_json(out)
    data.assert_pydantic_matches(actual, "models/cron-job")


def test_deployment_list(data: PhalanxData) -> None:
    out = data.read_text("kubectl/deployment-list.json")
    actual = ResourceList[Deployment].model_validate_json(out)
    data.assert_pydantic_matches(actual, "models/deploymnet")


def test_statefulset_list(data: PhalanxData) -> None:
    out = data.read_text("kubectl/statefulset-list.json")
    actual = ResourceList[StatefulSet].model_validate_json(out)
    data.assert_pydantic_matches(actual, "models/stateful-set")


def test_loadbalancer_service_list(data: PhalanxData) -> None:
    out = data.read_text("kubectl/service-list.json")
    actual = ResourceList[Service].model_validate_json(out)
    data.assert_pydantic_matches(actual, "models/service")


def test_loadbalancer_service_patch() -> None:
    # This should work
    ServiceIPPatch(
        spec=ServiceIPSpecPatch(load_balancer_ip=IPv4Address("1.2.3.4"))
    )

    with pytest.raises(AddressValueError):
        ServiceIPPatch(
            spec=ServiceIPSpecPatch(
                load_balancer_ip=IPv4Address("something malicious injection")
            )
        )
