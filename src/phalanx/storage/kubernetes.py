"""Storage layer for direct Kubernetes operations."""

from ..models.kubernetes import CronJob, Resources
from ..models.vault import VaultCredentials
from .command import Command

__all__ = ["KubernetesStorage"]


class KubernetesStorage:
    """Storage layer for direct Kubernetes operations.

    Used primarily by the installer. This uses :command:`kubectl` directly
    rather than one of the Python Kubernetes libraries since it seemed simpler
    at the time.

    Parameters
    ----------
    context
        The kubectl context to specify for all kubectl commands. If this is
        None, then the current context will be used.
    """

    def __init__(self, context: str | None = None) -> None:
        common_args = ["--context", context] if context else []
        self._kubectl = Command("kubectl", common_args=common_args)

    def create_namespace(
        self, namespace: str, *, ignore_fail: bool = False
    ) -> None:
        """Create a Kubernetes namespace.

        Parameters
        ----------
        namespace
            Namespace to create.
        ignore_fail
            If `True`, ignore failures, such as when the namespace already
            exists.

        Raises
        ------
        CommandFailedError
            Raised if the namespace creation fails, and ``ignore_fail`` was
            not set to `True`.
        """
        self._kubectl.run("create", "ns", namespace, ignore_fail=ignore_fail)

    def create_vault_secret(
        self, name: str, namespace: str, credentials: VaultCredentials
    ) -> None:
        """Create a Kubernetes ``Secret`` resource for Vault credentials.

        Parameters
        ----------
        name
            Name of the secret.
        namespace
            Namespace of the secret.
        credentials
            Vault credentials to store in the secret.
        """
        args = ["apply", "-f", "-"]
        self._kubectl.run(*args, stdin=credentials.to_kubernetes_secret(name))

    def get_current_context(self) -> str:
        """Get the current context (the default Kubernetes cluster).

        Returns
        -------
        str
            Name of the current Kubernetes context.
        """
        result = self._kubectl.capture("config", "current-context")
        return result.stdout.strip()

    def wait_for_rollout(self, name: str, namespace: str) -> None:
        """Wait for a Kubernetes rollout to complete.

        Parameters
        ----------
        name
            Name of the rollout. This should be the type of object (usually
            either ``deployment`` or ``statefulset``, followed by a slash and
            the name of the object.
        namespace
            Namespace in which the rollout is happening.
        """
        self._kubectl.run("-n", namespace, "rollout", "status", name)

    def restart(self, name: str, namespace: str) -> None:
        """Restart a kubernetes workload and wait for it to be ready again.

        Parameters
        ----------
        name
            Name of the workload. This should be the type of object (usually
            either ``deployment`` or ``statefulset``, followed by a slash and
            the name of the object.
        namespace
            Namespace in which the workload exists.
        """
        self._kubectl.run("-n", namespace, "rollout", "restart", name)
        self.wait_for_rollout(name=name, namespace=namespace)

    def get_phalanx_cronjobs(self) -> list[CronJob]:
        """Get the names of all CronJobs in all Phalanx apps.

        We say a CronJob is in a Phalanx app if it has an ArgoCD label.
        """
        raw = self._kubectl.capture(
            "get",
            "CronJob",
            "-l",
            "argocd.argoproj.io/instance",
            "-o",
            "json",
            "--all-namespaces",
        )
        cronjobs = Resources.model_validate_json(raw.stdout)
        return cronjobs.items

    def suspend_cronjobs(self, cronjobs: list[CronJob]) -> None:
        """Suspend all given cronjobs.

        Parameters
        ----------
        cronjobs
            A list of CronJobs to suspend.
        """
        patch = '{"spec" : {"suspend" : true }}'

        for job in cronjobs:
            self._kubectl.run(
                "patch",
                "CronJob",
                job.name,
                "--namespace",
                job.namespace,
                "--patch",
                patch,
            )

    def resume_cronjobs(self, cronjobs: list[CronJob]) -> None:
        """Resume all given cronjobs.

        Parameters
        ----------
        cronjobs
            A list of CronJobs to resume.
        """
        patch = '{"spec" : {"suspend" : false }}'

        for job in cronjobs:
            self._kubectl.run(
                "patch",
                "CronJob",
                job.name,
                "--namespace",
                job.namespace,
                "--patch",
                patch,
            )
