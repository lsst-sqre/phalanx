"""Operations for backing up and restoring GKE clusters."""

from ..storage.gke_backup import GKEBackupStorage

__all__ = ["GKEBackupService"]


class GKEBackupService:
    """Operations for backing up and restoring GKE clusters.

    All operations must happen in the same Google Cloud region and project.

    Anything that uses this service should assume all authentication has
    already been done and that the Google Cloud Python SDK can find whatever it
    needs to send authenticated requests.

    If you're running locally, ``gcloud auth application-default login`` should
    work.

    Parameters
    ----------
    storage
        Storage object for interacting with the Google Cloud Backup for GKE
        service.
    """

    def __init__(self, storage: GKEBackupStorage) -> None:
        self._gke_backup = storage

    def create_backup_plan(self, source_cluster: str) -> str:
        """Create a backup plan to backup everything in source_cluster.

        Volume data for PVs attached to PVCs is backed up.
        """
        return self._gke_backup.create_backup_plan(source_cluster)
