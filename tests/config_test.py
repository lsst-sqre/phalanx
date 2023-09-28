"""Tests for the Phalanx configuration itself."""

from __future__ import annotations

from pathlib import Path

import yaml

_ALLOW_NO_SECRETS = (
    "giftless",
    "linters",
    "monitoring",
    "obsloctap",
    "next-visit-fan-out",
    "plot-navigator",
    "production-tools",
)
"""Temporary whitelist of applications that haven't added secrets.yaml."""


def test_application_version() -> None:
    """All application charts should have version 1.0.0."""
    applications_path = Path(__file__).parent.parent / "applications"
    for application in applications_path.iterdir():
        if not application.is_dir():
            continue
        chart = yaml.safe_load((application / "Chart.yaml").read_text())
        assert (
            chart["version"] == "1.0.0"
        ), f"Chart for application {application.name} has incorrect version"

    # Check the same thing for shared charts.
    Path(__file__).parent.parent / "charts"
    for shared_chart in applications_path.iterdir():
        if not shared_chart.is_dir():
            continue
        chart = yaml.safe_load((shared_chart / "Chart.yaml").read_text())
        assert (
            chart["version"] == "1.0.0"
        ), f"Shared chart {shared_chart.name} has incorrect version"


def test_secrets_defined() -> None:
    """Any application with a VaultSecret should have secrets.yaml."""
    applications_path = Path(__file__).parent.parent / "applications"
    for application in applications_path.iterdir():
        if not application.is_dir() or application.name in _ALLOW_NO_SECRETS:
            continue
        if list(application.glob("secrets*.yaml")):
            continue
        template_path = application / "templates"
        if not template_path.is_dir():
            continue
        for template in (application / "templates").iterdir():
            if not template.is_file():
                continue
            resources = template.read_text().split("---\n")
            for resource in resources:
                if "kind: VaultSecret" not in resource:
                    continue
                if "name: pull-secret" in resource:
                    continue
                msg = (
                    f"Application {application.name} installs a VaultSecret"
                    " resource but has no secrets.yaml configuration"
                )
                raise AssertionError(msg)
