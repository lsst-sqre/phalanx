"""Tools for working with the Backup for GKE API.

https://docs.cloud.google.com/python/docs/reference/gkebackup/latest
"""

import time
from datetime import UTC, datetime, timedelta

from google.cloud.gke_backup_v1 import (
    Backup,
    BackupForGKEClient,
    BackupPlan,
    CreateBackupPlanRequest,
    CreateBackupRequest,
    CreateRestorePlanRequest,
    CreateRestoreRequest,
    DeleteBackupPlanRequest,
    DeleteBackupRequest,
    DeleteRestorePlanRequest,
    DeleteRestoreRequest,
    ListBackupPlansRequest,
    ListBackupsRequest,
    ListRestorePlansRequest,
    ListRestoresRequest,
    ResourceSelector,
    Restore,
    RestoreConfig,
    RestorePlan,
)

from ..exceptions import (
    GoogleCloudAPIError,
    GoogleCloudGKEBackupFailedError,
    GoogleCloudGKEBackupTimedoutError,
    GoogleCloudGKERestoreFailedError,
    GoogleCloudGKERestoreTimedoutError,
)

__all__ = ["GKEBackupStorage"]


class GKEBackupStorage:
    """Run GKE Backup commands against Google Cloud resources in a project.

    Anything that uses this should assume all authentication has already been
    done and that the Google Cloud Python SDK can find whatever it needs to
    send authenticated requests.

    If you're running locally, ``gcloud auth application-default login`` should
    work.

    Parameters
    ----------
    region
        The Google Cloud region to run comands against.
    project
        The Google Cloud project to run comands against.
    labels
        Labels to set on provisioned Google Cloud resources.
    """

    # Helpful docs for development:
    #
    # * API errors: https://docs.cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/errors

    def __init__(
        self, region: str, project: str, labels: dict[str, str] | None = None
    ) -> None:
        self._region = region
        self._project = project
        self._parent = f"projects/{self._project}/locations/{self._region}"
        self._client = BackupForGKEClient()
        self._labels = labels or {}

    def create_backup_plan(self, source_cluster: str) -> str:
        """Create a backup plan to backup everything in source_cluster.

        Volume data for PVs attached to PVCs is backed up.

        Parameters
        ----------
        source_cluster
            The GKE cluster to take a backup up of when creating backups from
            this plan.
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.BackupPlan.BackupConfig
        config = BackupPlan.BackupConfig(
            all_namespaces=True, include_volume_data=True
        )

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.BackupPlan
        plan = BackupPlan(
            cluster=f"{self._parent}/clusters/{source_cluster}",
            backup_config=config,
            description="Created by Phalanx",
            labels=self._labels,
        )

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.CreateBackupPlanRequest
        request = CreateBackupPlanRequest(
            parent=self._parent,
            backup_plan_id=self._make_id(),
            backup_plan=plan,
        )

        operation = self._client.create_backup_plan(request=request)
        result = operation.result()
        if result is None:
            raise GoogleCloudAPIError
        return result.name

    def create_backup(self, backup_plan: str) -> str:
        """Create a GKE backup from the given backup plan.

        Parameters
        ----------
        backup_plan
            The fully qualified backup plan name, like
            projects/roundtable-dev-abe2/locations/us-central1/backupPlans/phalanx-20260123-220839-fd0769e1-2b72-4464-8398-2cfcea696b13
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.Backup
        backup = Backup(
            description="Created by Phalanx",
            labels=self._labels,
        )

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.CreateBackupRequest.html
        request = CreateBackupRequest(
            parent=backup_plan,
            backup=backup,
            backup_id=self._make_id(),
        )

        operation = self._client.create_backup(request=request)
        result = operation.result()
        if result is None:
            raise GoogleCloudAPIError
        return result.name

    def create_restore_plan(
        self, backup_plan: str, destination_cluster: str
    ) -> str:
        """Create a restore plan.

        Volume data for PVs attached to PVCs is backed up.

        Parameters
        ----------
        backup_plan
            The name of the backup plan to restore a backup from.
        destination_cluster
            The GKE cluster to take restore the backup to.
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.RestoreConfig
        config = RestoreConfig(
            all_namespaces=True,
            # For each PVC to be restored, create a new underlying volume and
            # PV from the corresponding VolumeBackup contained within the
            # Backup.
            volume_data_restore_policy=RestoreConfig.VolumeDataRestorePolicy.RESTORE_VOLUME_DATA_FROM_BACKUP,
            # Do not attempt to restore the conflicting resource.
            cluster_resource_conflict_policy=RestoreConfig.ClusterResourceConflictPolicy.USE_EXISTING_VERSION,
            # This can't be FAIL_ON_CONFLICT, because we need to use
            # fine-grained restore, because we only want to restore certain
            # namespaced resources from the backup
            namespaced_resource_restore_mode=RestoreConfig.NamespacedResourceRestoreMode.MERGE_SKIP_ON_CONFLICT,
            cluster_resource_restore_scope=RestoreConfig.ClusterResourceRestoreScope(
                all_group_kinds=True
            ),
        )

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.RestorePlan
        plan = RestorePlan(
            description="Created by Phalanx",
            backup_plan=backup_plan,
            cluster=f"{self._parent}/clusters/{destination_cluster}",
            restore_config=config,
            labels=self._labels,
        )

        request = CreateRestorePlanRequest(
            parent=self._parent,
            restore_plan=plan,
            restore_plan_id=self._make_id(),
        )

        operation = self._client.create_restore_plan(request)
        result = operation.result()
        if result is None:
            raise GoogleCloudAPIError
        return result.name

    def wait_for_backup(
        self,
        backup_name: str,
        interval: timedelta = timedelta(seconds=5),
        attempts: int = 60,
    ) -> None:
        """Wait for a GKE backup to complete.

        Parameters
        ----------
        backup_name
            The fully-qualified name of the backup to wait for, like
            projects/roundtable-dev-abe2/locations/us-central1/backupPlans/phalanx-20260126-175433/backups/phalanx-20260126-175435

        Raises
        ------
        GoogleCloudGKEBackupFailedError
            If there was an error creating the backup.
        GoogleCloudGKEBackupTimedoutError
            If the backup has not completed after the specified number of
            attempts.
        """
        for _ in range(attempts):
            backup = self._client.get_backup(name=backup_name)
            if backup.state == Backup.State.SUCCEEDED:
                return
            elif backup.state == Backup.State.FAILED:
                raise GoogleCloudGKEBackupFailedError(backup_name)
            time.sleep(interval.total_seconds())

        raise GoogleCloudGKEBackupTimedoutError(
            backup_name, attempts, interval
        )

    def wait_for_restore(
        self,
        restore_name: str,
        interval: timedelta = timedelta(seconds=5),
        attempts: int = 60,
    ) -> None:
        """Wait for a GKE restore to complete.

        Parameters
        ----------
        restore_name
            The fully-qualified name of the restore to wait for, like
            projects/roundtable-dev-abe2/locations/us-central1/restorePlans/phalanx-20260126-175433/restores/phalanx-20260126-175435

        Raises
        ------
        GoogleCloudGKERestoreFailedError
            If there was an error creating the restore.
        GoogleCloudGKERestoreTimedoutError
            If the restore has not completed after the specified number of
            attempts.
        """
        for _ in range(attempts):
            restore = self._client.get_restore(name=restore_name)
            if restore.state == Restore.State.SUCCEEDED:
                return
            elif restore.state == Restore.State.FAILED:
                raise GoogleCloudGKERestoreFailedError(restore_name)
            time.sleep(interval.total_seconds())

        raise GoogleCloudGKERestoreTimedoutError(
            restore_name, attempts, interval
        )

    def list_backup_plans(self, filter_exp: str) -> list[BackupPlan]:
        """Get backup plans with a specific label value.

        Parameters
        ----------
        filter_exp
            A filter expression to list only specific resources.
            More information in the docs:

            https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.ListBackupPlansRequest
        request = ListBackupPlansRequest(
            filter=filter_exp, parent=self._parent
        )
        page_result = self._client.list_backup_plans(request=request)
        return list(page_result)

    def list_backups(self, backup_plan: str, filter_exp: str) -> list[Backup]:
        """Get backups with from a backup plan, filtered by filter_exp.

        Parameters
        ----------
        backup_plan
            The fully-qualified name of the backup plan that took the backups.
        filter_exp
            A filter expression to list only specific resources.
            More information in the docs:

            https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.ListBackupsRequest
        request = ListBackupsRequest(filter=filter_exp, parent=backup_plan)
        page_result = self._client.list_backups(request=request)
        return list(page_result)

    def list_restores(
        self, restore_plan: str, filter_exp: str
    ) -> list[Restore]:
        """Get restores from a specific restore plan, filtered with filter_exp.

        Parameters
        ----------
        restore_plan
            The fully-qualified name of the restore plan that made the restore.
        filter_exp
            A filter expression to list only specific resources.
            More information in the docs:

            https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.ListRestoresRequest
        request = ListRestoresRequest(filter=filter_exp, parent=restore_plan)
        page_result = self._client.list_restores(request=request)
        return list(page_result)

    def create_pvc_restore(self, restore_plan: str, backup: str) -> str:
        """Create a PVC-only restore for a GKE cluster.

        This will restore PVCs, the data from their backing PVs, and
        StorageClasses.

        Parameters
        ----------
        restore_plan
            The fully-qualified name of the restore plan to use when creating
            the restore.
        backup
            The fully-qualified name of the backup to restore from.
        """
        restore_filter = Restore.Filter(
            inclusion_filters=[
                ResourceSelector(
                    group_kind=RestoreConfig.GroupKind(
                        resource_group="storage.k8s.io",
                        resource_kind="StorageClass",
                    )
                ),
                ResourceSelector(
                    group_kind=RestoreConfig.GroupKind(
                        resource_kind="PersistentVolumeClaim"
                    )
                ),
            ]
        )

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.Restore
        restore = Restore(
            description="Created by Phalanx.",
            backup=backup,
            labels=self._labels,
            filter=restore_filter,
        )

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.CreateRestoreRequest
        request = CreateRestoreRequest(
            parent=restore_plan, restore=restore, restore_id=self._make_id()
        )

        operation = self._client.create_restore(request=request)
        result = operation.result()
        if result is None:
            raise GoogleCloudAPIError
        return result.name

    def list_restore_plans(self, filter_exp: str) -> list[RestorePlan]:
        """Get restore plans with a specific label value.

        Parameters
        ----------
        filter_exp
            A filter expression to list only specific resources.
            More information in the docs:

            https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.ListRestorePlansRequest
        request = ListRestorePlansRequest(
            filter=filter_exp, parent=self._parent
        )
        page_result = self._client.list_restore_plans(request=request)
        return list(page_result)

    def delete_backup_plan(self, backup_plan: str) -> None:
        """Delete a backup plan.

        If the backup plan still has associated backups, then it will only be
        deactivated.

        Parameters
        ----------
        backup_plan
            The fully-qualified name of the backup plan that took the backups.
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.DeleteBackupPlanRequest
        request = DeleteBackupPlanRequest(name=backup_plan)
        operation = self._client.delete_backup_plan(request)
        operation.result()

    def delete_restore_plan(self, restore_plan: str) -> None:
        """Delete a restore plan.

        If the restore plan still has associated restores, then it will only be
        deactivated.

        Parameters
        ----------
        restore_plan
            The fully-qualified name of the restore plan.
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.DeleteRestorePlanRequest
        request = DeleteRestorePlanRequest(name=restore_plan)
        operation = self._client.delete_restore_plan(request)
        operation.result()

    def delete_backup(self, backup: str) -> None:
        """Delete a backup, including all associated volume resources.

        Parameters
        ----------
        backup
            The fully-qualified name of the backup.
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.DeleteBackupRequest
        request = DeleteBackupRequest(
            name=backup,
            force=True,
        )

        operation = self._client.delete_backup(request)
        operation.result()

    def delete_restore(self, restore: str) -> None:
        """Delete a restore and all of its associated VolumeRestores.

        Parameters
        ----------
        restore
            The fully-qualified name of the restore.
        """
        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.DeleteRestoreRequest
        request = DeleteRestoreRequest(
            name=restore,
            force=True,
        )
        operation = self._client.delete_restore(request)
        operation.result()

    def _make_id(self) -> str:
        """Create a unique ID for a Google Cloud resource."""
        now = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")
        return f"phalanx-{now}"
