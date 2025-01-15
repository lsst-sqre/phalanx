"""Tests for the Phalanx configuration itself."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import yaml

from phalanx.factory import Factory
from phalanx.models.applications import Project

_ALLOW_NO_SECRETS = ("next-visit-fan-out",)
"""Temporary whitelist of applications that haven't added secrets.yaml."""


def all_charts(
    parent: Literal["applications", "charts"],
) -> Iterator[Path]:
    """Iterate through all chart paths."""
    root_path = Path(__file__).parent.parent / parent
    for candidate in root_path.iterdir():
        if not candidate.is_dir():
            continue
        yield candidate


def test_application_names() -> None:
    """All applications must have valid names."""
    for application in all_charts("applications"):
        assert re.match("[a-z][a-z0-9-]+$", application.name), (
            f"Application {application.name} has invalid name"
        )


def test_application_projects() -> None:
    """All applications are in projects in the correct directories."""
    factory = Factory(Path(__file__).parent.parent)
    config_storage = factory.create_config_storage()
    config = config_storage.load_phalanx_config()
    for application in config.applications:
        template_path = (
            config_storage.get_environment_chart_path()
            / "templates"
            / "applications"
            / application.project.name
            / f"{application.name}.yaml"
        )
        assert template_path.exists(), (
            f"Application resource template for {application.name} not at"
            f" {template_path!s}"
        )
        template = template_path.read_text()

        # Helm templates are unfortunately not valid YAML, so do this the hard
        # way with a regular expression.
        pattern = r"project:\s*\"?(?P<project>[a-z]+)\"?\s"
        match = re.search(pattern, template)
        assert match, f"Project not found in {template_path!s}"
        assert match.group("project") == application.project.value, (
            f"Project in {template_path!s} does not match"
            f" {application.project.value}"
        )


def test_application_version() -> None:
    """All application charts should have version 1.0.0."""
    for application in all_charts("applications"):
        chart = yaml.safe_load((application / "Chart.yaml").read_text())
        assert chart["version"] == "1.0.0", (
            f"Chart for application {application.name} has incorrect version"
        )

    # Check the same thing for shared charts.
    for shared_chart in all_charts("charts"):
        chart = yaml.safe_load((shared_chart / "Chart.yaml").read_text())
        assert chart["version"] == "1.0.0", (
            f"Shared chart {shared_chart.name} has incorrect version"
        )


def test_enviroments() -> None:
    """Ensure applications don't have configs for unknown environments."""
    factory = Factory(Path(__file__).parent.parent)
    config_storage = factory.create_config_storage()
    environments = set(config_storage.list_environments())
    for app_name in config_storage.list_applications():
        app_envs = set(config_storage.get_application_environments(app_name))
        if not app_envs <= environments:
            unknown = ", ".join(sorted(app_envs - environments))
            msg = f"{app_name} configured for unknown environments: {unknown}"
            raise AssertionError(msg)


def test_projects() -> None:
    """Ensure all projects are defined."""
    template_path = (
        Path(__file__).parent.parent
        / "environments"
        / "templates"
        / "projects"
    )
    for project in Project:
        assert (template_path / f"{project.value}.yaml").exists(), (
            f"Project {project.value} is not defined"
        )


def test_secrets_defined() -> None:
    """Any application with a VaultSecret should have secrets.yaml."""
    for application in all_charts("applications"):
        if application.name in _ALLOW_NO_SECRETS:
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


def test_shared_subcharts() -> None:
    """Check references to shared subcharts."""
    available = [c.name for c in all_charts("charts")]
    for application in all_charts("applications"):
        chart = yaml.safe_load((application / "Chart.yaml").read_text())
        chart.get("dependencies")
        for dependency in chart.get("dependencies", []):
            if not re.match("file:", dependency.get("repository", "")):
                continue
            name = application.name
            version = dependency.get("version")
            repository = dependency["repository"]
            m = re.match(r"file://[.][.]/[.][.]/charts/([^/]+)$", repository)
            assert m, f"Incorrect shared chart URL in {name}: {repository}"
            assert m.group(1) in available, (
                f"Missing shared chart dependency {m.group(1)} in {name}"
            )
            assert dependency["version"] == "1.0.0", (
                f"Incorrect shared chart version in {name}: {version} != 1.0.0"
            )


def test_applications_enabled() -> None:
    """Check that every application is enabled in some environment.

    Also check that the application is configured for every environment in
    which it is enabled.
    """
    factory = Factory(Path(__file__).parent.parent)
    config_storage = factory.create_config_storage()
    config = config_storage.load_phalanx_config()
    for application in config.applications:
        name = application.name
        active = set(application.active_environments)
        assert active, f"Application {name} is not enabled in any environment"
        configured = set(config_storage.get_application_environments(name))
        for env in active:
            msg = f"Application {name} enabled for {env} but not configured"
            assert env in configured, msg
