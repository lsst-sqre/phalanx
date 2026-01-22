"""Operations for backing up and restoring GKE clusters."""

from google.cloud.gke_backup_v1 import Backup, Restore

from phalanx.constants import GOOGLE_CLOUD_RUN_ID_LABEL

from ..storage.gke_backup import GKEBackupStorage

__all__ = ["GKEBackupService"]


class GKEBackupService:
    """Operations for backing up and restoring GKE clusters.

    All operations must happen in the same Google Cloud region and project.

    Anything that uses this should assume all authentication has already been
    done and that the Google Cloud Python SDK can find whatever it needs to
    send authenticated requests.

    If you're running locally, ``gcloud auth application-default login`` should
    work.

    Parameters
    ----------
    storage
        Storage object for interacting with the Google Cloud Backup for GKE
        service.
    phalanx_run_id
        An identifier to put in the ``phalanx-run`` label on every Google Cloud
        resource that is created with this service. This is helpful in resuming
        backup and restore process after a Google Cloud operation fails (which
        does happen intermittently), and in cleaning up these resources later.
    """

    def __init__(self, storage: GKEBackupStorage, phalanx_run_id: str) -> None:
        self._gke_backup = storage
        self._run_id = phalanx_run_id

    def backup_and_restore_pvcs(
        self, source_cluster: str, destination_cluster: str
    ) -> None:
        """Backup a GKE cluster and restore the PVCs and PVs to another.

        Parameters
        ----------
        source_cluster
            The name of the GKE cluster to back up.
        destination cluster
            The name of the GKE cluster to restore the backup to.
        """
        backup_plan_name = self._gke_backup.create_backup_plan(source_cluster)
        print(f"Backup plan created: {backup_plan_name}")

        backup_name = self._gke_backup.create_backup(backup_plan_name)
        print(f"Waiting for backup to finish: {backup_name}")
        self._gke_backup.wait_for_backup(backup_name)
        print(f"Backup finished: {backup_name}")

        restore_plan_name = self._gke_backup.create_restore_plan(
            backup_plan=backup_plan_name,
            destination_cluster=destination_cluster,
        )
        print(f"Restore plan created: {restore_plan_name}")

        restore_name = self._gke_backup.create_pvc_restore(
            restore_plan_name, backup_name
        )
        print(f"Restore created: {restore_name}")
        print(f"Waiting for restore to finish: {restore_name}")
        self._gke_backup.wait_for_restore(restore_name)
        print(f"Restore finished: {restore_name}")
        print(f"Finished! {GOOGLE_CLOUD_RUN_ID_LABEL}: {self._run_id}")

    def cleanup_run(self) -> None:
        """Delete Google Cloud resources labeled with this phalanx run id."""
        filter_exp = f'labels.{GOOGLE_CLOUD_RUN_ID_LABEL}="{self._run_id}"'
        backup_plans = self._gke_backup.list_backup_plans(filter_exp)
        backups: list[Backup] = []
        for backup_plan in backup_plans:
            _backups = self._gke_backup.list_backups(
                backup_plan=backup_plan.name, filter_exp=filter_exp
            )
            backups.extend(_backups)

        for backup in backups:
            print(f"Deleting backup {backup.name}")
            self._gke_backup.delete_backup(backup.name)
            print(f"Deleted backup {backup.name}")
        for backup_plan in backup_plans:
            print(f"Deleting backup plan {backup_plan.name}")
            self._gke_backup.delete_backup_plan(backup_plan.name)
            print(f"Deleted backup plan {backup_plan.name}")

        restore_plans = self._gke_backup.list_restore_plans(filter_exp)
        restores: list[Restore] = []
        for restore_plan in restore_plans:
            _restores = self._gke_backup.list_restores(
                restore_plan=restore_plan.name, filter_exp=filter_exp
            )
            restores.extend(_restores)

        for restore in restores:
            print(f"Deleting restore {restore.name}")
            self._gke_backup.delete_restore(restore.name)
            print(f"Deleted restore {restore.name}")

        for restore_plan in restore_plans:
            print(f"Deleting restore plan {restore_plan.name}")
            self._gke_backup.delete_restore_plan(restore_plan.name)
            print(f"Deleted restore plan {restore_plan.name}")
