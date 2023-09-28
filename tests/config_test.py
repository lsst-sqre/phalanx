"""Tests for the Phalanx configuration itself."""

from __future__ import annotations

from pathlib import Path

import yaml


def test_application_version() -> None:
    """Test that all application charts have version 1.0.0."""
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
