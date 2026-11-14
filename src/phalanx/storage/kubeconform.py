"""Storage layer for running kubeconform on rendered Kubernetes resources."""

import sys
from pathlib import Path

import yaml

from ..exceptions import CommandFailedError
from .command import Command

__all__ = ["KubeconformStorage"]


class KubeconformStorage:
    """Storage layer for running :command:`kubeconform`.

    :command:`kubeconform` validates rendered Kubernetes resources against the
    schemas of the Kubernetes API. This catches problems that neither
    :command:`helm lint` nor :command:`kube-linter` can see, such as a value
    of the wrong type (an unquoted ``true`` as the value of an environment
    variable, for example) or a missing required field. Kubernetes, and
    therefore Argo CD, rejects such resources when they are applied.

    kubeconform is not run in strict mode, which would also reject unknown
    fields and duplicate keys, because some existing charts still have them.

    The schemas are downloaded on first use and cached on disk, so that
    linting every application does not download them again for every chart.

    Custom resources are not validated, since kubeconform does not have their
    schemas. They are skipped explicitly rather than left for kubeconform to
    look up, because kubeconform does not cache a failed lookup and so would
    otherwise make a network request for each custom resource every time.

    Parameters
    ----------
    cache_path
        Directory in which to cache downloaded schemas. It is created if it
        does not exist.
    kubernetes_version
        Version of Kubernetes whose schemas to validate against.
    """

    def __init__(self, cache_path: Path, kubernetes_version: str) -> None:
        self._cache_path = cache_path
        self._kubernetes_version = kubernetes_version
        self._kubeconform = Command("kubeconform")

    def validate_application(
        self, application: str, environment: str, resources: str
    ) -> bool:
        """Run :command:`kubeconform` on the resources of an application.

        Any validation errors are sent to standard output, and a failure
        message is printed to standard error.

        Parameters
        ----------
        application
            Name of the application, used in the failure message.
        environment
            Name of the environment, used in the failure message.
        resources
            Rendered Kubernetes resources for the application in that
            environment, as produced by :command:`helm template`.

        Returns
        -------
        bool
            Whether the check passed.
        """
        self._cache_path.mkdir(parents=True, exist_ok=True)
        args = [
            "-ignore-missing-schemas",
            "-kubernetes-version",
            self._kubernetes_version,
            "-cache",
            str(self._cache_path),
        ]
        if custom_resources := _find_custom_resources(resources):
            args.extend(["-skip", ",".join(custom_resources)])
        args.append("-")
        try:
            self._kubeconform.capture(*args, stdin=resources)
        except CommandFailedError as e:
            if e.stdout:
                sys.stdout.write(e.stdout)
                sys.stdout.flush()
            if e.stderr:
                sys.stderr.write(e.stderr)
            msg = (
                f"Error: Application {application} in environment"
                f" {environment} has kubeconform errors\n"
            )
            sys.stderr.write(msg)
            return False
        return True


def _find_custom_resources(resources: str) -> list[str]:
    """Find the custom resource types among rendered resources.

    Parameters
    ----------
    resources
        Rendered Kubernetes resources as produced by :command:`helm template`.

    Returns
    -------
    list of str
        Sorted ``apiVersion/kind`` of each type of custom resource, in the
        form accepted by the ``-skip`` flag of :command:`kubeconform`. If the
        resources cannot be parsed, this is empty, and kubeconform will
        report the syntax error itself.
    """
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    try:
        documents = list(yaml.load_all(resources, Loader=loader))
    except yaml.YAMLError:
        return []
    custom_resources = set()
    for document in documents:
        if not isinstance(document, dict):
            continue
        api_version = document.get("apiVersion")
        kind = document.get("kind")
        if not isinstance(api_version, str) or not isinstance(kind, str):
            continue
        if _is_custom_api_version(api_version):
            custom_resources.add(f"{api_version}/{kind}")
    return sorted(custom_resources)


def _is_custom_api_version(api_version: str) -> bool:
    """Determine whether an API version belongs to a custom resource.

    Built-in Kubernetes API groups either have no dots in their names (such
    as ``apps``, ``batch``, and the core group, which has no name at all) or
    end in ``.k8s.io``. Anything else is a custom resource.

    A custom resource whose group ends in ``.k8s.io`` is not detected, but
    kubeconform still skips it because of ``-ignore-missing-schemas``, at the
    cost of a network request to look up its schema.

    Parameters
    ----------
    api_version
        The ``apiVersion`` of a resource, such as ``apps/v1``.

    Returns
    -------
    bool
        Whether that API version is a custom resource.
    """
    group, separator, _ = api_version.rpartition("/")
    return bool(separator) and "." in group and not group.endswith(".k8s.io")
