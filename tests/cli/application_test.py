"""Tests for the application command-line subcommand."""

import shutil
import subprocess
from pathlib import Path
from unittest.mock import ANY, call

import pytest
import yaml
from git.repo import Repo
from git.util import Actor

from phalanx.constants import KUBECONFORM_KUBERNETES_VERSION
from phalanx.exceptions import CommandFailedError
from phalanx.factory import Factory
from phalanx.models.applications import Project

from ..support.cli import run_cli
from ..support.command import MockCommand
from ..support.data import PhalanxData
from ..support.helm import MockHelmCommand

KUBE_LINTER_ARGS = ("lint", "--config", ANY, "-")
"""Expected arguments of each kube-linter invocation."""


KUBECONFORM_ARGS = (
    "-ignore-missing-schemas",
    "-kubernetes-version",
    ANY,
    "-cache",
    ANY,
    "-",
)
"""Expected arguments of a kubeconform invocation with no custom resources."""


def expect_kube_linter(mock_kube_linter: MockCommand, count: int) -> None:
    """Expect a given number of passing kube-linter runs."""
    for _ in range(count):
        mock_kube_linter.expect_capture(
            args=KUBE_LINTER_ARGS, response="No lint errors found!\n"
        )


def expect_kubeconform(mock_kubeconform: MockCommand, count: int) -> None:
    """Expect a given number of passing kubeconform runs."""
    for _ in range(count):
        mock_kubeconform.expect_capture(args=KUBECONFORM_ARGS, response="")


@pytest.fixture
def config_path(data: PhalanxData, tmp_path: Path) -> Path:
    """Create a copy of the input configuration for tests that modify it."""
    config_path = tmp_path / "phalanx"
    shutil.copytree(str(data.path("input")), str(config_path))
    return config_path


def test_add_helm_repos(data: PhalanxData, mock_helm: MockHelmCommand) -> None:
    result = run_cli("application", "add-helm-repos", "argocd")
    assert result.output == ""
    assert result.exit_code == 0
    data.assert_json_matches(
        mock_helm.call_args_list, "application/add-helm-repos-argocd"
    )

    mock_helm.reset_mock()
    result = run_cli("application", "add-helm-repos")
    assert result.output == ""
    assert result.exit_code == 0
    data.assert_json_matches(
        mock_helm.call_args_list, "application/add-helm-repos"
    )


def test_create(data: PhalanxData, config_path: Path) -> None:
    app_docs_path = config_path / "docs" / "applications"
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
    data.assert_text_matches(env_values, "create/values.yaml")

    # Check that the Argo CD application templates were created.
    argo_path = config_path / "environments" / "templates" / "applications"
    assert (argo_path / "infrastructure" / "aaa-new-app.yaml").exists()
    assert (argo_path / "rsp" / "hips.yaml").exists()
    assert (argo_path / "rsp" / "zzz-other-app.yaml").exists()

    # Check that the documentation files were created.
    assert (app_docs_path / "aaa-new-app" / "index.rst").exists()
    assert (app_docs_path / "aaa-new-app" / "values.md").exists()
    assert (app_docs_path / "hips" / "index.rst").exists()
    assert (app_docs_path / "hips" / "values.md").exists()
    assert (app_docs_path / "zzz-other-app" / "index.rst").exists()
    assert (app_docs_path / "zzz-other-app" / "values.md").exists()

    # Check that the applications were added to the indices.
    index = (app_docs_path / "infrastructure.rst").read_text()
    data.assert_text_matches(index, "create/infrastructure.rst")
    index = (app_docs_path / "rsp.rst").read_text()
    data.assert_text_matches(index, "create/rsp.rst")

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


def test_create_errors(data: PhalanxData, config_path: Path) -> None:
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


def test_create_prompt(data: PhalanxData, config_path: Path) -> None:
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


def test_lint(
    data: PhalanxData,
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = (
                "==> Linting .\n"
                "[INFO] Chart.yaml: icon is recommended\n"
                "\n"
                "1 chart(s) linted, 0 chart(s) failed\n"
            )
        elif command[0] == "template":
            output = "this is some template\n"
        return subprocess.CompletedProcess(
            returncode=0,
            args=command,
            stdout=output,
            stderr=None,
        )

    # Lint a single application that will succeed, and check that the icon
    # line is filtered out of the output. The chart is then expanded and the
    # result fed to kube-linter and kubeconform, which add no output when
    # they pass.
    mock_helm.set_capture_callback(callback)
    expect_kube_linter(mock_kube_linter, 1)
    expect_kubeconform(mock_kubeconform, 1)
    result = run_cli("application", "lint", "gafaelfawr", "-e", "idfdev")
    expected = "==> Linting gafaelfawr (environment idfdev)\n"
    assert result.output == expected
    assert result.exit_code == 0
    data.assert_json_matches(
        mock_helm.call_args_list, "application/lint-gafaelfawr"
    )
    assert mock_kube_linter.mock.capture.call_args_list == [
        call(*KUBE_LINTER_ARGS, stdin="this is some template\n")
    ]
    assert mock_kubeconform.mock.capture.call_args_list == [
        call(*KUBECONFORM_ARGS, stdin="this is some template\n")
    ]

    # Lint both gafaelfawr and portal for all configured environmments. We
    # won't bother to check the --set flag again. The important part is that
    # we call helm lint twice, but all of the setup is only called once.
    mock_helm.reset_mock()
    mock_kube_linter.mock.capture.reset_mock()
    mock_kubeconform.mock.capture.reset_mock()
    expect_kube_linter(mock_kube_linter, 3)
    expect_kubeconform(mock_kubeconform, 3)
    result = run_cli("application", "lint", "gafaelfawr", "portal")
    expected += (
        "==> Linting gafaelfawr (environment minikube)\n"
        "==> Linting portal (environment idfdev)\n"
    )
    assert result.output == expected
    assert result.exit_code == 0
    data.assert_json_matches(
        mock_helm.call_args_list, "application/lint-gafaelfawr-portal"
    )

    def callback_error(*command: str) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(
            returncode=1,
            args=command,
            stdout="",
            stderr="Some error\n",
        )

    # Neither kube-linter nor kubeconform is run when helm lint fails.
    mock_helm.reset_mock()
    mock_helm.set_capture_callback(callback_error)
    result = run_cli("application", "lint", "gafaelfawr", "--env", "idfdev")
    assert result.output == (
        "Some error\n"
        "Error: Application gafaelfawr in environment idfdev has errors\n"
    )
    assert result.exit_code == 1
    assert mock_kube_linter.mock.capture.call_count == 3
    assert mock_kubeconform.mock.capture.call_count == 3


def test_lint_kube_linter_error(
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = "==> Linting .\n\n1 chart(s) linted, 0 chart(s) failed\n"
        elif command[0] == "template":
            output = "this is some template\n"
        return subprocess.CompletedProcess(
            returncode=0, args=command, stdout=output, stderr=None
        )

    # A failing kube-linter check reports its output and fails the lint.
    # kubeconform is still run so that all problems are reported at once.
    mock_helm.set_capture_callback(callback)
    expect_kubeconform(mock_kubeconform, 1)
    failed_args = ("lint", "--config", ".kube-linter.yaml", "-")
    exc = subprocess.CalledProcessError(
        returncode=1,
        cmd=["kube-linter", *failed_args],
        output='Duplicate environment variable FOO in container "bar"\n',
        stderr="Error: found 1 lint errors\n",
    )
    mock_kube_linter.expect_capture(
        args=KUBE_LINTER_ARGS,
        response=CommandFailedError("kube-linter", failed_args, exc),
    )
    result = run_cli("application", "lint", "gafaelfawr", "-e", "idfdev")
    assert result.output == (
        "==> Linting gafaelfawr (environment idfdev)\n"
        'Duplicate environment variable FOO in container "bar"\n'
        "Error: found 1 lint errors\n"
        "Error: Application gafaelfawr in environment idfdev has"
        " kube-linter errors\n"
    )
    assert result.exit_code == 1
    assert mock_kubeconform.mock.capture.call_count == 1


def test_lint_kubeconform_error(
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = "==> Linting .\n\n1 chart(s) linted, 0 chart(s) failed\n"
        elif command[0] == "template":
            output = "this is some template\n"
        return subprocess.CompletedProcess(
            returncode=0, args=command, stdout=output, stderr=None
        )

    # A failing kubeconform check reports its output and fails the lint.
    mock_helm.set_capture_callback(callback)
    expect_kube_linter(mock_kube_linter, 1)
    failed_args = ("-ignore-missing-schemas", "-")
    message = (
        "stdin - Deployment gafaelfawr is invalid: problem validating schema."
        " - at '/spec/template/spec/containers/0/env/0/value': got boolean,"
        " want null or string\n"
    )
    exc = subprocess.CalledProcessError(
        returncode=1,
        cmd=["kubeconform", *failed_args],
        output=message,
        stderr="",
    )
    mock_kubeconform.expect_capture(
        args=KUBECONFORM_ARGS,
        response=CommandFailedError("kubeconform", failed_args, exc),
    )
    result = run_cli("application", "lint", "gafaelfawr", "-e", "idfdev")
    assert result.output == (
        "==> Linting gafaelfawr (environment idfdev)\n"
        f"{message}"
        "Error: Application gafaelfawr in environment idfdev has"
        " kubeconform errors\n"
    )
    assert result.exit_code == 1


def test_lint_kubeconform_custom_resources(
    tmp_path: Path,
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
    template = (
        "---\n"
        "# Source: gafaelfawr/templates/disabled.yaml\n"
        "# A comment outside a conditional that is false.\n"
        "---\n"
        "apiVersion: v1\n"
        "kind: ConfigMap\n"
        "metadata:\n"
        "  name: gafaelfawr\n"
        "---\n"
        "apiVersion: networking.k8s.io/v1\n"
        "kind: NetworkPolicy\n"
        "metadata:\n"
        "  name: gafaelfawr\n"
        "---\n"
        "apiVersion: ricoberger.de/v1alpha1\n"
        "kind: VaultSecret\n"
        "metadata:\n"
        "  name: gafaelfawr\n"
        "---\n"
        "apiVersion: gafaelfawr.lsst.io/v1alpha1\n"
        "kind: GafaelfawrIngress\n"
        "metadata:\n"
        "  name: gafaelfawr\n"
        "---\n"
        "apiVersion: ricoberger.de/v1alpha1\n"
        "kind: VaultSecret\n"
        "metadata:\n"
        "  name: gafaelfawr-other\n"
    )

    def callback(*command: str) -> subprocess.CompletedProcess:
        output = None
        if command[0] == "lint":
            output = "==> Linting .\n\n1 chart(s) linted, 0 chart(s) failed\n"
        elif command[0] == "template":
            output = template
        return subprocess.CompletedProcess(
            returncode=0, args=command, stdout=output, stderr=None
        )

    # Custom resources, and only custom resources, are skipped, each type
    # listed once. The schema cache is created under XDG_CACHE_HOME, which
    # the fixture points at the temporary directory.
    mock_helm.set_capture_callback(callback)
    expect_kube_linter(mock_kube_linter, 1)
    cache_path = tmp_path / "cache" / "phalanx" / "kubeconform"
    args = (
        "-ignore-missing-schemas",
        "-kubernetes-version",
        KUBECONFORM_KUBERNETES_VERSION,
        "-cache",
        str(cache_path),
        "-skip",
        (
            "gafaelfawr.lsst.io/v1alpha1/GafaelfawrIngress,"
            "ricoberger.de/v1alpha1/VaultSecret"
        ),
        "-",
    )
    mock_kubeconform.expect_capture(args=args, response="")
    result = run_cli("application", "lint", "gafaelfawr", "-e", "idfdev")
    assert result.output == "==> Linting gafaelfawr (environment idfdev)\n"
    assert result.exit_code == 0
    assert mock_kubeconform.mock.capture.call_args_list == [
        call(*args, stdin=template)
    ]
    assert cache_path.is_dir()


def test_lint_no_repos(
    data: PhalanxData,
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
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
    expect_kube_linter(mock_kube_linter, 1)
    expect_kubeconform(mock_kubeconform, 1)
    result = run_cli("application", "lint", "postgres", "-e", "idfdev")
    expected = "==> Linting postgres (environment idfdev)\n"
    assert result.output == expected
    assert result.exit_code == 0
    data.assert_json_matches(
        mock_helm.call_args_list, "application/lint-postgres"
    )


def test_lint_all(
    data: PhalanxData,
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
    expect_kube_linter(mock_kube_linter, 9)
    expect_kubeconform(mock_kubeconform, 9)
    result = run_cli("application", "lint-all")
    assert result.output == ""
    assert result.exit_code == 0
    data.assert_json_matches(mock_helm.call_args_list, "application/lint-all")


def test_lint_all_git(
    data: PhalanxData,
    tmp_path: Path,
    mock_helm: MockHelmCommand,
    mock_kube_linter: MockCommand,
    mock_kubeconform: MockCommand,
) -> None:
    upstream_path = tmp_path / "upstream"
    shutil.copytree(str(data.path("input")), str(upstream_path))
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
    expect_kube_linter(mock_kube_linter, 4)
    expect_kubeconform(mock_kubeconform, 4)
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
    data.assert_json_matches(
        mock_helm.call_args_list, "application/lint-all-git"
    )


def test_template(data: PhalanxData, mock_helm: MockHelmCommand) -> None:
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
    data.assert_json_matches(mock_helm.call_args_list, "application/template")
