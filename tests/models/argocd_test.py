"""Tests for ArgoCD resource models."""

from syrupy.assertion import SnapshotAssertion

from phalanx.models.argocd import ApplicationList
from tests.support.constants import DATA_DIR


def output(filename: str) -> str:
    return (DATA_DIR / "output" / "argocd" / filename).read_text()


def test_application(snapshot: SnapshotAssertion) -> None:
    out = output("application-list.json")
    application_list = ApplicationList.model_validate_json(out)
    assert application_list == snapshot(name="application_list")

    with_vault_secrets = application_list.with_resource("KafkaUser")
    assert with_vault_secrets == snapshot(name="with_vault_secrets")
