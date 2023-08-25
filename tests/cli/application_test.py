"""Tests for the application command-line subcommand."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from phalanx.factory import Factory

from ..support.cli import run_cli
from ..support.data import phalanx_test_path, read_output_data


def test_create(tmp_path: Path) -> None:
    config_path = tmp_path / "phalanx"
    shutil.copytree(str(phalanx_test_path()), str(config_path))
    (config_path / "docs").mkdir()
    app_docs_path = config_path / "docs" / "applications"
    app_docs_path.mkdir()
    apps_path = config_path / "applications"

    # Add three new applications that sort at the start, in the middle, and at
    # the end of the list of applications in the environment values.yaml file
    # to test the complex code for adding the new flags in sorted order.
    result = run_cli(
        "application",
        "create",
        "aaa-new-app",
        "empty",
        "--description",
        "First new app",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert result.exit_code == 0
    assert result.output == ""
    result = run_cli(
        "application",
        "create",
        "hips",
        "web-service",
        "--description",
        "Some HiPS service",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert result.exit_code == 0
    assert result.output == ""
    result = run_cli(
        "application",
        "create",
        "zzz-other-app",
        "empty",
        "--description",
        "Last new app",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert result.exit_code == 0
    assert result.output == ""

    # Check that the environments/values.yaml file was updated correctly.
    env_values = (config_path / "environments" / "values.yaml").read_text()
    assert env_values == read_output_data("minikube", "values-after-add.yaml")

    # Check that the documentation files were created.
    assert (app_docs_path / "aaa-new-app" / "index.rst").exists()
    assert (app_docs_path / "aaa-new-app" / "values.md").exists()
    assert (app_docs_path / "hips" / "index.rst").exists()
    assert (app_docs_path / "hips" / "values.md").exists()
    assert (app_docs_path / "zzz-other-app" / "index.rst").exists()
    assert (app_docs_path / "zzz-other-app" / "values.md").exists()

    # Enable all of these applications for the minikube environment so that we
    # can load them with the normal tools.
    minikube_path = config_path / "environments" / "values-minikube.yaml"
    minikube = yaml.safe_load(minikube_path.read_text())
    minikube["applications"]["aaa-new-app"] = True
    minikube["applications"]["hips"] = True
    minikube["applications"]["zzz-other-app"] = True
    with minikube_path.open("w") as fh:
        yaml.dump(minikube, fh)
    (apps_path / "aaa-new-app" / "values-minikube.yaml").write_text("")
    (apps_path / "hips" / "values-minikube.yaml").write_text("")
    (apps_path / "zzz-other-app" / "values-minikube.yaml").write_text("")

    # Load the environment, make sure the new apps are enabled, and check that
    # the chart descriptions are correct.
    factory = Factory(config_path)
    config_storage = factory.create_config_storage()
    environment = config_storage.load_environment("minikube")
    assert "aaa-new-app" in environment.applications
    assert "hips" in environment.applications
    assert "zzz-other-app" in environment.applications
    for app, expected in (
        ("aaa-new-app", "First new app"),
        ("hips", "Some HiPS service"),
        ("zzz-other-app", "Last new app"),
    ):
        assert environment.applications[app].chart["description"] == expected
