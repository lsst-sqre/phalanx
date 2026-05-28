"""Test fixtures."""

import shutil
from collections.abc import Iterator
from pathlib import Path

import jinja2
import pytest
from git import Repo
from pytest_mock.plugin import MockerFixture

from phalanx.factory import Factory
from phalanx.storage import argocd, kubernetes

from .support.command import MockCommand
from .support.data import PhalanxData
from .support.google_cloud import (
    MockGoogleCloudClients,
    mock_google_cloud_storage,
)
from .support.helm import MockHelmCommand, patch_helm
from .support.onepassword import MockOnepasswordClient, patch_onepassword
from .support.recover import MockRecover
from .support.vault import MockVaultClient, patch_vault


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-test-data",
        action="store_true",
        default=False,
        help="Overwrite expected test output with current results",
    )


@pytest.fixture(autouse=True)
def _clear_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove dangerous environment variables.

    Ensure that none of the tests can accidentally authenticate to a live
    Vault or 1Password Connect server by clearing the relevant environment
    variables.
    """
    monkeypatch.delenv("OP_CONNECT_TOKEN", raising=False)
    monkeypatch.delenv("VAULT_TOKEN", raising=False)


@pytest.fixture
def data(request: pytest.FixtureRequest) -> PhalanxData:
    update = request.config.getoption("--update-test-data")
    return PhalanxData(Path(__file__).parent / "data", update_test_data=update)


@pytest.fixture
def real_git_repo(tmp_path: Path, data: PhalanxData) -> Iterator[Path]:
    """Copy the test phalanx config dir and initialize a real git repo."""
    path = shutil.copytree(data.path("input"), tmp_path / "input")
    repo = Repo.init(path)
    repo.create_remote("origin", "https://nope.nope")

    yield path

    shutil.rmtree(path)


@pytest.fixture
def factory(data: PhalanxData) -> Factory:
    """Create a factory pointing at the test data."""
    return Factory(data.path("input"))


@pytest.fixture
def mock_helm() -> Iterator[MockHelmCommand]:
    """Mock out Helm commands."""
    yield from patch_helm()


@pytest.fixture
def mock_kubernetes_kubectl() -> Iterator[MockCommand]:
    """Mock the kubectl Command in the kubernetes storage."""
    mock_command = MockCommand()
    yield from mock_command.patch_command_class(kubernetes)


@pytest.fixture
def mock_onepassword() -> Iterator[MockOnepasswordClient]:
    """Mock out the 1Password Connect client API."""
    yield from patch_onepassword()


@pytest.fixture
def mock_vault() -> Iterator[MockVaultClient]:
    """Mock out the HVAC Vault client API."""
    yield from patch_vault()


@pytest.fixture
def templates() -> jinja2.Environment:
    """Return the Jinja templating environment."""
    return jinja2.Environment(
        loader=jinja2.PackageLoader("phalanx", "data"),
        undefined=jinja2.StrictUndefined,
        autoescape=jinja2.select_autoescape(disabled_extensions=["tmpl"]),
    )


@pytest.fixture
def mock_kubectl() -> Iterator[MockCommand]:
    """Mock the kubectl Command in the kubernetes storage."""
    mock_command = MockCommand()
    yield from mock_command.patch_command_class(kubernetes)


@pytest.fixture
def mock_argocd() -> Iterator[MockCommand]:
    """Mock the argocd Command in the argocd storage."""
    mock_command = MockCommand()
    yield from mock_command.patch_command_class(argocd)


@pytest.fixture
def mock_google_cloud() -> Iterator[MockGoogleCloudClients]:
    """Mock the Google Cloud API clients in the Google Cloud storage."""
    yield from mock_google_cloud_storage()


@pytest.fixture
def mock_recover(
    data: PhalanxData,
    factory: Factory,
    mock_helm: MockHelmCommand,
    mock_vault: MockVaultClient,
    mock_argocd: MockCommand,
    mock_kubectl: MockCommand,
    mock_google_cloud: MockGoogleCloudClients,
) -> MockRecover:
    """Return a function to mock things for preflight check testing."""
    return MockRecover(
        data=data,
        factory=factory,
        mock_helm=mock_helm,
        mock_vault=mock_vault,
        mock_argocd=mock_argocd,
        mock_kubectl=mock_kubectl,
        mock_google_cloud=mock_google_cloud,
    )


@pytest.fixture
def mock_which(mocker: MockerFixture) -> None:
    """Make shutil.which always find something."""
    mocker.patch("shutil.which")
