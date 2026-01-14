"""Service for manipulating Phalanx Kubernetes clusters directly."""

from phalanx.constants import PREVIOUS_REPLICA_COUNT_ANNOTATION
from phalanx.models.kubernetes import Workload

from ..exceptions import InvalidScaleStateError
from ..storage.kubernetes import KubernetesStorage

__all__ = ["PhalanxClusterService"]


class PhalanxClusterService:
    """Kubernetes operations on a Phalanx cluster.

    These operations are not in the EnviromentService because:

    * They do not necessarily correspond 1-1 to a
      Phalanx enviroment.
    * They are often part of tasks that involve
      multiple clusters, so passing an explicit context is
      less error prone, and allows the operations to be
      automated without having to manually change the kubectl
      current context.

    For example, when recovering a GCP cluster from backups while the old
    cluster still exists, you will need to work with two clusters, both of
    which are associated with the same environment.

    Parameters
    ----------
    kubernetes_storage
        Interface to direct Kubernetes object manipulation.
    """

    def __init__(self, kubernetes_storage: KubernetesStorage) -> None:
        self._kubernetes = kubernetes_storage

    def suspend_cronjobs(self) -> None:
        """Suspend all CronJobs in all Phalanx apps."""
        cronjobs = self._kubernetes.get_phalanx_cronjobs()
        return self._kubernetes.suspend_cronjobs(cronjobs)

    def resume_cronjobs(self) -> None:
        """Resume all CronJobs in all Phalanx apps."""
        cronjobs = self._kubernetes.get_phalanx_cronjobs()
        return self._kubernetes.resume_cronjobs(cronjobs)

    def scale_down_workloads(self) -> None:
        """Scale down (almost) all Phalanx workloads.

        During cluster rebuilds when there is an old and a new cluster, certain
        workloads can't be running in both clusters at the same time, or else
        state external to the cluster could be corrupted.

        We'll leave ArgoCD running so the scaled-down cluster can still be
        inspected.

        Raises
        ------
        InvalidScaleStateError
            If the workload resource has a previous replica count annotation,
            but its current replica count is not zero.
        """
        workloads = self._get_workloads_except_argocd()
        for workload in workloads:
            self._check_state(workload)
            self._kubernetes.annotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
                value=str(workload.replicas),
            )
            self._kubernetes.scale(workload, 0)

    def scale_up_workloads(self) -> None:
        """Scale up (almost) all Phalanx workloads to their previous counts.

        This is only intended to be run after a scale down operation.

        Raises
        ------
        InvalidScaleStateError
            If the workload resource has a previous replica count annotation,
            but its current replica count is not zero.

        """
        workloads = self._get_workloads_except_argocd()
        for workload in workloads:
            self._check_state(workload)
            if workload.previous_replica_count is None:
                continue
            self._kubernetes.scale(workload, workload.previous_replica_count)
            self._kubernetes.deannotate(
                workload,
                key=PREVIOUS_REPLICA_COUNT_ANNOTATION,
            )

    def _get_workloads_except_argocd(self) -> list[Workload]:
        """Get all Phalanx workloads in the cluster except ArgoCD workloads.

        Returns
        -------
        list[Workload]
            A list of Phalanx workloads execpt for ArgoCD workloads.
        """
        deployments = self._kubernetes.get_phalanx_deployments()
        statefulsets = self._kubernetes.get_phalanx_stateful_sets()

        return [
            workload
            for workload in deployments + statefulsets
            if workload.namespace != "argocd"
        ]

    def _check_state(self, workload: Workload) -> None:
        """Make sure the workload is in an OK state to be scaled.

        Parameters
        ----------
        workload
          The workload to check the state of.

        """
        if workload.previous_replica_count:
            if workload.replicas != 0:
                raise InvalidScaleStateError(workload)
