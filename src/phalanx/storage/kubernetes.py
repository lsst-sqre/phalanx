"""Storage layer for direct Kubernetes operations."""

from __future__ import annotations

from .command import Command

__all__ = ["KubernetesStorage"]


class KubernetesStorage:
    """Storage layer for direct Kubernetes operations.

    Used primarily by the installer. This uses :command:`kubectl` directly
    rather than one of the Python Kubernetes libraries since it seemed simpler
    at the time.
    """

    def __init__(self) -> None:
        self._kubectl = Command("kubectl")

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

    def create_generic_secret(
        self, name: str, namespace: str, keys: dict[str, str]
    ) -> None:
        """Create a generic Kubernetes ``Secret`` resource.

        Parameters
        ----------
        name
            Name of the secret.
        namespace
            Namespace of the secret.
        keys
            Key and value pairs to put into the secret.
        """
        args = [
            "create",
            "secret",
            "generic",
            name,
            "--namespace",
            namespace,
        ]
        for key, value in keys.items():
            args.append(f"--from-literal={key}={value}")
        self._kubectl.run(*args)

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
