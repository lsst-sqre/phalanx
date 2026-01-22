"""Helpers for mocking the Google Cloud Python API."""

from collections.abc import Iterator
from dataclasses import dataclass
from unittest.mock import MagicMock, create_autospec, patch

from google.cloud.compute_v1beta import AddressesClient, FirewallsClient
from google.cloud.container_v1 import ClusterManagerClient
from google.cloud.gke_backup_v1 import Backup, BackupForGKEClient, Restore

from phalanx.storage import google_cloud_api

__all__ = ["MockGoogleCloudClients", "mock_google_cloud_storage"]


@dataclass
class MockGoogleCloudClients:
    addresses: MagicMock
    backup: MagicMock
    firewalls: MagicMock
    gke: MagicMock


def mock_google_cloud_storage() -> Iterator[MockGoogleCloudClients]:
    """Mock all of the Google Cloud API clients used by the storage.

    Returns
    -------
    MockGoogleCloudClients
        A collection of Mock objects that will be called by the storage in
        place of the actual Google Cloud API clients.

    """
    mocks = MockGoogleCloudClients(
        addresses=create_autospec(AddressesClient, instance=True),
        backup=create_autospec(BackupForGKEClient, instance=True),
        firewalls=create_autospec(FirewallsClient, instance=True),
        gke=create_autospec(ClusterManagerClient, instance=True),
    )

    patchers = []
    for location, mock_client in (
        ("AddressesClient", mocks.addresses),
        ("BackupForGKEClient", mocks.backup),
        ("FirewallsClient", mocks.firewalls),
        ("ClusterManagerClient", mocks.gke),
    ):
        patcher = patch.object(google_cloud_api, location, autospec=True)
        class_mock = patcher.start()
        class_mock.return_value = mock_client
        patchers.append(patcher)

    # Mock these so that we don't wait forever when we're waiting for status
    mock_backup = MagicMock()
    mock_backup.state = Backup.State.SUCCEEDED
    mocks.backup.get_backup.return_value = mock_backup

    mock_restore = MagicMock()
    mock_restore.state = Restore.State.SUCCEEDED
    mocks.backup.get_restore.return_value = mock_restore

    yield mocks

    for patcher in patchers:
        patcher.stop()
