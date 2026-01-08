"""Service for manipulating Phalanx Kubernetes clusters directly."""

from ..storage.kubernetes import KubernetesStorage

__all__ = ["PhalanxClusterService"]


class PhalanxClusterService:
    """Kubernetes operations on a Phalanx cluster.

    These operations are not in the EnviromentService these reasons:

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
