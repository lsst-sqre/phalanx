"""Tests for the application command-line subcommand."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from unittest.mock import ANY

import yaml
from git.repo import Repo
from git.util import Actor

from phalanx.factory import Factory
from phalanx.models.applications import Project

from ..support.cli import run_cli
from ..support.data import (
    phalanx_test_path,
    read_output_data,
    read_output_json,
)
from ..support.helm import MockHelmCommand


def test_add_helm_repos(mock_helm: MockHelmCommand) -> None:
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
        "--project",
        "infrastructure",
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
        "--starter",
        "web-service",
        "--project",
        "rsp",
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
        "--project",
        "rsp",
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
    for app, project in (
        ("aaa-new-app", Project.infrastructure),
        ("hips", Project.rsp),
        ("zzz-other-app", Project.rsp),
    ):
        assert environment.applications[app].project == project
    for app, expected in (
        ("aaa-new-app", "First new app"),
        ("hips", "Some HiPS service"),
        ("zzz-other-app", "Last new app"),
    ):
        assert environment.applications[app].chart["description"] == expected
        assert environment.applications[app].chart["version"] == "1.0.0"

    # Charts created from the empty starter should not have appVersion. Charts
    # using the web-service or fastapi-safir starters should, set to 0.1.0.
    assert "appVersion" not in environment.applications["aaa-new-app"].chart
    assert environment.applications["hips"].chart["appVersion"] == "0.1.0"
    zzz_other_app = environment.applications["zzz-other-app"]
    assert zzz_other_app.chart["appVersion"] == "0.1.0"

    # Charts using the web-service starter should have a default sources.
    expected = "https://github.com/lsst-sqre/hips"
    assert environment.applications["hips"].chart["sources"][0] == expected

    # Check that <CHARTENVPREFIX> was substituted correctly in the ConfigMap
    # template for the fastapi-safir chart.
    path = apps_path / "zzz-other-app" / "templates" / "configmap.yaml"
    config_map = path.read_text()
    assert "  ZZZ_OTHER_APP_LOG_LEVEL:" in config_map
    assert "  ZZZ_OTHER_APP_PATH_PREFIX:" in config_map


def test_create_errors(tmp_path: Path) -> None:
    config_path = tmp_path / "phalanx"
    shutil.copytree(str(phalanx_test_path()), str(config_path))
    result = run_cli(
        "application",
        "create",
        "some-really-long-app-name-please-do-not-do-this",
        "--project",
        "infrastructure",
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
        "--project",
        "infrastructure",
        "--description",
        "lowercase description",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert "Description must start with capital letter" in result.output
    assert result.exit_code == 2
    result = run_cli(
        "application",
        "create",
        "app",
        "--description",
        "Description",
        "--project",
        "foo",
        "--config",
        str(config_path),
        needs_config=False,
    )
    assert "'foo' is not one of" in result.output
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
        stdin="Some application\ninfrastructure\n",
    )
    assert result.output == (
        "Short description: Some application\n"
        "Possible Argo CD projects are\n  "
        + "\n  ".join(p.value for p in Project)
        + "\nArgo CD project: infrastructure\n"
    )
    assert result.exit_code == 0

    app_path = config_path / "applications" / "aaa-new-app"
    with (app_path / "Chart.yaml").open() as fh:
        chart = yaml.safe_load(fh)
    assert chart["description"] == "Some application"


def test_lint(mock_helm: MockHelmCommand) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = (
                "==> Linting .\n"
                "[INFO] Chart.yaml: icon is recommended\n"
                "\n"
                "1 chart(s) linted, 0 chart(s) failed\n"
            )
        return subprocess.CompletedProcess(
            returncode=0,
            args=command,
            stdout=output,
            stderr=None,
        )

    # Lint a single application that will succeed, and check that the icon
    # line is filtered out of the output.
    mock_helm.set_capture_callback(callback)
    result = run_cli("application", "lint", "gafaelfawr", "-e", "idfdev")
    expected = "==> Linting gafaelfawr (environment idfdev)\n"
    assert result.output == expected
    assert result.exit_code == 0
    set_args = read_output_json("idfdev", "lint-set-values")
    assert mock_helm.call_args_list == [
        ["repo", "add", "lsst-sqre", "https://lsst-sqre.github.io/charts/"],
        ["repo", "update"],
        ["dependency", "update", "--skip-refresh"],
        [
            "lint",
            "gafaelfawr",
            "--strict",
            "--values",
            "gafaelfawr/values.yaml",
            "--values",
            "gafaelfawr/values-idfdev.yaml",
            "--set",
            ",".join(set_args),
        ],
    ]

    # Lint both gafaelfawr and portal for all configured environmments. We
    # won't bother to check the --set flag again. The important part is that
    # we call helm lint twice, but all of the setup is only called once.
    mock_helm.reset_mock()
    result = run_cli("application", "lint", "gafaelfawr", "portal")
    expected += (
        "==> Linting gafaelfawr (environment minikube)\n"
        "==> Linting portal (environment idfdev)\n"
    )
    assert result.output == expected
    assert result.exit_code == 0
    assert mock_helm.call_args_list == [
        ["repo", "add", "lsst-sqre", "https://lsst-sqre.github.io/charts/"],
        ["repo", "update"],
        ["dependency", "update", "--skip-refresh"],
        [
            "lint",
            "gafaelfawr",
            "--strict",
            "--values",
            "gafaelfawr/values.yaml",
            "--values",
            "gafaelfawr/values-idfdev.yaml",
            "--set",
            ",".join(set_args),
        ],
        [
            "lint",
            "gafaelfawr",
            "--strict",
            "--values",
            "gafaelfawr/values.yaml",
            "--values",
            "gafaelfawr/values-minikube.yaml",
            "--set",
            ANY,
        ],
        ["dependency", "update", "--skip-refresh"],
        [
            "lint",
            "portal",
            "--strict",
            "--values",
            "portal/values.yaml",
            "--values",
            "portal/values-idfdev.yaml",
            "--set",
            ",".join(set_args),
        ],
    ]

    def callback_error(*command: str) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(
            returncode=1,
            args=command,
            stdout="",
            stderr="Some error\n",
        )

    mock_helm.reset_mock()
    mock_helm.set_capture_callback(callback_error)
    result = run_cli("application", "lint", "gafaelfawr", "--env", "idfdev")
    assert result.output == (
        "Some error\n"
        "Error: Application gafaelfawr in environment idfdev has errors\n"
    )
    assert result.exit_code == 1


def test_lint_no_repos(mock_helm: MockHelmCommand) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = "==> Linting .\n"
        return subprocess.CompletedProcess(
            returncode=0,
            args=command,
            stdout=output,
            stderr=None,
        )

    # Lint a single application that has no dependency charts, and make sure
    # we don't try to run repo update, which may fail.
    mock_helm.set_capture_callback(callback)
    result = run_cli("application", "lint", "postgres", "-e", "idfdev")
    expected = "==> Linting postgres (environment idfdev)\n"
    assert result.output == expected
    assert result.exit_code == 0
    set_args = read_output_json("idfdev", "lint-set-values")
    assert mock_helm.call_args_list == [
        ["dependency", "update", "--skip-refresh"],
        [
            "lint",
            "postgres",
            "--strict",
            "--values",
            "postgres/values.yaml",
            "--values",
            "postgres/values-idfdev.yaml",
            "--set",
            ",".join(set_args),
        ],
    ]


def test_lint_all(mock_helm: MockHelmCommand) -> None:
    result = run_cli("application", "lint-all")
    assert result.output == ""
    assert result.exit_code == 0
    expected_calls = read_output_json("idfdev", "lint-all-calls")
    assert mock_helm.call_args_list == expected_calls


def test_lint_all_git(tmp_path: Path, mock_helm: MockHelmCommand) -> None:
    upstream_path = tmp_path / "upstream"
    shutil.copytree(str(phalanx_test_path()), str(upstream_path))
    upstream_repo = Repo.init(str(upstream_path), initial_branch="main")
    upstream_repo.index.add(["applications", "environments"])
    actor = Actor("Someone", "someone@example.com")
    upstream_repo.index.commit("Initial commit", author=actor, committer=actor)
    change_path = tmp_path / "change"
    repo = Repo.clone_from(str(upstream_path), str(change_path))

    # Now, make a few changes that should trigger linting.
    #
    # - argocd (only idfdev)
    # - gafaelfawr (values change so all environments)
    # - portal (templates deletion so all environments)
    # - postgres (irrelevant change, no linting)
    path = change_path / "applications" / "argocd" / "values-idfdev.yaml"
    with path.open("a") as fh:
        fh.write("foo: bar\n")
    path = change_path / "applications" / "gafaelfawr" / "values.yaml"
    with path.open("a") as fh:
        fh.write("foo: bar\n")
    repo.index.remove(
        "applications/portal/templates/vault-secrets.yaml", working_tree=True
    )
    repo.index.remove(
        "applications/postgres/values-idfdev.yaml", working_tree=True
    )
    repo.index.add(["applications"])
    repo.index.commit("Some changes", author=actor, committer=actor)

    # Okay, now we can run the lint and check the helm commands that were run
    # against the expected output.
    result = run_cli(
        "application",
        "lint-all",
        "--git",
        "--config",
        str(change_path),
        needs_config=False,
    )
    assert result.output == ""
    assert result.exit_code == 0
    expected_calls = read_output_json("idfdev", "lint-git-calls")
    assert mock_helm.call_args_list == expected_calls


def test_template(mock_helm: MockHelmCommand) -> None:
    test_path = phalanx_test_path()

    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "template":
            output = "this is some template\n"
        return subprocess.CompletedProcess(
            returncode=0, args=command, stdout=output, stderr=None
        )

    mock_helm.set_capture_callback(callback)
    result = run_cli("application", "template", "gafaelfawr", "idfdev")
    assert result.output == "this is some template\n"
    assert result.exit_code == 0
    set_args = read_output_json("idfdev", "lint-set-values")
    assert mock_helm.call_args_list == [
        ["repo", "add", "lsst-sqre", "https://lsst-sqre.github.io/charts/"],
        ["repo", "update"],
        ["dependency", "update", "--skip-refresh"],
        [
            "template",
            "gafaelfawr",
            str(test_path / "applications" / "gafaelfawr"),
            "--include-crds",
            "--values",
            "gafaelfawr/values.yaml",
            "--values",
            "gafaelfawr/values-idfdev.yaml",
            "--set",
            ",".join(set_args),
        ],
    ]
