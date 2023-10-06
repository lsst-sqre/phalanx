"""Tests for the application command-line subcommand."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from phalanx.factory import Factory

from ..support.cli import run_cli
from ..support.data import phalanx_test_path, read_output_data
from ..support.helm import MockHelm


def test_add_helm_repos(mock_helm: MockHelm) -> None:
    result = run_cli("application", "add-helm-repos", "argocd")
    assert result.output == ""
    assert result.exit_code == 0
    assert mock_helm.call_args_list == [
        ["repo", "add", "argoproj", "https://argoproj.github.io/argo-helm"]
    ]

    mock_helm.reset_mock()
    result = run_cli("application", "add-helm-repos")
    assert result.output == ""
    assert result.exit_code == 0
    assert mock_helm.call_args_list == [
        ["repo", "add", "argoproj", "https://argoproj.github.io/argo-helm"],
        [
            "repo",
            "add",
            "jupyterhub",
            "https://jupyterhub.github.io/helm-chart/",
        ],
        ["repo", "add", "lsst-sqre", "https://lsst-sqre.github.io/charts/"],
    ]


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
        "--starter",
        "empty",
        "--description",
        "First new app",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert result.output == ""
    assert result.exit_code == 0
    result = run_cli(
        "application",
        "create",
        "hips",
        "--description",
        "Some HiPS service",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert result.output == ""
    assert result.exit_code == 0
    result = run_cli(
        "application",
        "create",
        "zzz-other-app",
        "--starter",
        "empty",
        "--description",
        "Last new app",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert result.output == ""
    assert result.exit_code == 0

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
    # the chart metadata is correct.
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
        assert environment.applications[app].chart["version"] == "1.0.0"

    # Charts created from the empty starter should not have appVersion. Charts
    # using the web-service starter should, set to 0.1.0.
    assert "appVersion" not in environment.applications["aaa-new-app"].chart
    assert "appVersion" not in environment.applications["zzz-other-app"].chart
    assert environment.applications["hips"].chart["appVersion"] == "0.1.0"

    # Charts using the web-service starter should have a default sources.
    expected = "https://github.com/lsst-sqre/hips"
    assert environment.applications["hips"].chart["sources"][0] == expected


def test_create_errors(tmp_path: Path) -> None:
    config_path = tmp_path / "phalanx"
    shutil.copytree(str(phalanx_test_path()), str(config_path))
    result = run_cli(
        "application",
        "create",
        "some-really-long-app-name-please-do-not-do-this",
        "--description",
        "Some really long description on top of the app name",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert "Name plus description is too long" in result.output
    assert result.exit_code == 2
    result = run_cli(
        "application",
        "create",
        "app",
        "--description",
        "lowercase description",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert "Description must start with capital letter" in result.output
    assert result.exit_code == 2


def test_create_prompt(tmp_path: Path) -> None:
    config_path = tmp_path / "phalanx"
    shutil.copytree(str(phalanx_test_path()), str(config_path))
    (config_path / "docs").mkdir()
    app_docs_path = config_path / "docs" / "applications"
    app_docs_path.mkdir()

    # Add an application, prompting for the description.
    result = run_cli(
        "application",
        "create",
        "aaa-new-app",
        "--config",
        str(config_path),
        needs_config=False,
        stdin="Some application\n",
    )
    assert result.output == "Short description: Some application\n"
    assert result.exit_code == 0

    app_path = config_path / "applications" / "aaa-new-app"
    with (app_path / "Chart.yaml").open() as fh:
        chart = yaml.safe_load(fh)
    assert chart["description"] == "Some application"
