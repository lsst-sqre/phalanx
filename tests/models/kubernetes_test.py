"""Tests for Kubernetes resource models."""

from phalanx.models.kubernetes import CronJob, Resources
from tests.support.constants import DATA_DIR


def test_cronjob_list() -> None:
    out = (DATA_DIR / "output" / "kubectl" / "cronjob_list.json").read_text()
    expected = Resources(
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

    actual = Resources.model_validate_json(out)

    assert expected == actual
