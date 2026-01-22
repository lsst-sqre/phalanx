"""Tests for ArgoCD resource models."""

from phalanx.models.argocd import ApplicationList

from ..support.data import PhalanxData


def test_application(data: PhalanxData) -> None:
    raw = data.read_text("argocd/application-list.json")
    application_list = ApplicationList.model_validate_json(raw)
    data.assert_pydantic_matches(application_list, "models/argocd-application")

    with_vault_secrets = application_list.with_resource("KafkaUser")
    serialized = [item.model_dump() for item in with_vault_secrets]
    data.assert_json_matches(
        serialized,
        "models/argocd-application-with-vault-secrets",
    )
