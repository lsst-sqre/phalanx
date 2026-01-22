"""Tools for working with the Backup for GKE API.

https://docs.cloud.google.com/python/docs/reference/gkebackup/latest
"""

from datetime import UTC, datetime
from uuid import uuid4

from google.cloud.gke_backup_v1 import (
    Backup,
    BackupForGKEClient,
    BackupPlan,
    CreateBackupPlanRequest,
    CreateBackupRequest,
)

from phalanx.exceptions import GoogleCloudAPIError

__all__ = ["GKEBackupStorage"]


class GKEBackupStorage:
    """Run GKE Backup commands against Google Cloud resources in a project.

    Anything that uses this storage should assume all authentication has
    already been done and that the Google Cloud Python SDK can find whatever it
    needs to send authenticated requests.

    If you're running locally, ``gcloud auth application-default login`` should
    work.

    Parameters
    ----------
    region
        The Google Cloud region to run comands against.
    project
        The Google Cloud project to run comands against.
    """

    def __init__(self, region: str, project: str) -> None:
        self._region = region
        self._project = project
        self._client = BackupForGKEClient()

    def create_backup_plan(self, source_cluster: str) -> str:
        """Create a backup plan to backup everything in source_cluster.

        Volume data for PVs attached to PVCs is backed up.
        """
        parent = f"projects/{self._project}/locations/{self._region}"
        now = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")
        plan_id = f"phalanx-{now}-{uuid4()}"

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.BackupPlan.BackupConfig
        config = BackupPlan.BackupConfig()
        config.all_namespaces = True
        config.include_volume_data = True

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.BackupPlan
        plan = BackupPlan()
        plan.cluster = f"{parent}/clusters/{source_cluster}"
        plan.backup_config = config
        plan.description = "Created by Phalanx"

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.CreateBackupPlanRequest
        request = CreateBackupPlanRequest()
        request.parent = parent
        request.backup_plan_id = plan_id
        request.backup_plan = plan

        operation = self._client.create_backup_plan(request=request)
        result = operation.result()
        if result is None:
            raise GoogleCloudAPIError(str(result))
        return result.name

    def create_backup(self, backup_plan: str):
        """Create a GKE backup from the given backup plan.

        Parameters
        ----------
        backup_plan
            The fully qualified backup plan name, like
            projects/roundtable-dev-abe2/locations/us-central1/backupPlans/phalanx-20260123-220839-fd0769e1-2b72-4464-8398-2cfcea696b13
        """
        now = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.Backup
        backup = Backup()
        backup.description = "Created by Phalanx"

        # https://docs.cloud.google.com/python/docs/reference/gkebackup/latest/google.cloud.gke_backup_v1.types.CreateBackupRequest.html
        request = CreateBackupRequest()
        request.parent = backup_plan
        request.backup_id = f"phalanx-{now}-{uuid4()}"
