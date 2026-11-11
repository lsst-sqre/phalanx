"""Storage layer for running kube-linter on rendered Kubernetes resources."""

import sys
from pathlib import Path

from ..exceptions import CommandFailedError
from .command import Command

__all__ = ["KubeLinterStorage"]

_DEPRECATION_WARNING = "Flag --fail-on-invalid-resource has been deprecated"
"""Start of the warning kube-linter prints for ``--fail-on-invalid-resource``.

The flag is deprecated in favor of the ``schema-validation`` check, but that
check only sees resources that kube-linter has already loaded successfully, so
it cannot catch the problems the flag exists to catch. The warning is
therefore dropped from the output shown to the user, where it would otherwise
appear alongside every real failure and could be mistaken for its cause.
"""


class KubeLinterStorage:
    """Storage layer for running :command:`kube-linter`.

    :command:`kube-linter` checks rendered Kubernetes resources for problems
    that :command:`helm lint` cannot see, such as two environment variables
    with the same name in one container. The checks to run are configured in
    the :file:`.kube-linter.yaml` file at the root of the Phalanx repository.

    Any resource that kube-linter cannot load is also reported as an error.
    Without that, kube-linter silently skips the resource, so a value of the
    wrong type, such as an unquoted ``true`` as the value of an environment
    variable, passes linting but is rejected when Argo CD syncs it.

    Parameters
    ----------
    config_path
        Path to the kube-linter configuration file.
    """

    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path
        self._kube_linter = Command("kube-linter")

    def lint_application(
        self, application: str, environment: str, resources: str
    ) -> bool:
        """Run :command:`kube-linter` on the resources of an application.

        Any lint errors are sent to standard output, and a failure message is
        printed to standard error.

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
        try:
            self._kube_linter.capture(
                "lint",
                "--fail-on-invalid-resource",
                "--config",
                str(self._config_path),
                "-",
                stdin=_drop_empty_documents(resources),
            )
        except CommandFailedError as e:
            if e.stdout:
                sys.stdout.write(e.stdout)
                sys.stdout.flush()
            if e.stderr:
                sys.stderr.write(_drop_deprecation_warning(e.stderr))
            msg = (
                f"Error: Application {application} in environment"
                f" {environment} has kube-linter errors\n"
            )
            sys.stderr.write(msg)
            return False
        return True


def _drop_deprecation_warning(output: str) -> str:
    """Remove the ``--fail-on-invalid-resource`` deprecation warning.

    Parameters
    ----------
    output
        Standard error from :command:`kube-linter`.

    Returns
    -------
    str
        The same output without the deprecation warning line.
    """
    lines = output.splitlines(keepends=True)
    return "".join(
        line for line in lines if not line.startswith(_DEPRECATION_WARNING)
    )


def _drop_empty_documents(resources: str) -> str:
    """Remove YAML documents that contain only comments or whitespace.

    :command:`helm template` emits a document for every template file, even
    one whose resources are all inside a conditional that is false. If the
    template has comments outside that conditional, the document contains
    only those comments. Argo CD ignores such documents, but kube-linter
    cannot load them and so reports them as errors.

    Parameters
    ----------
    resources
        Rendered Kubernetes resources as produced by :command:`helm template`.

    Returns
    -------
    str
        The same resources, byte for byte, without the empty documents.
    """
    documents: list[list[str]] = [[]]
    for line in resources.splitlines(keepends=True):
        if line.rstrip() == "---" and documents[-1]:
            documents.append([])
        documents[-1].append(line)
    return "".join(
        "".join(lines) for lines in documents if _has_content(lines)
    )


def _has_content(lines: list[str]) -> bool:
    """Check whether a YAML document has anything other than comments.

    Parameters
    ----------
    lines
        Lines of the document, possibly starting with a ``---`` separator.

    Returns
    -------
    bool
        Whether any line is something other than a separator, a comment, or
        whitespace.
    """
    for line in lines:
        stripped = line.strip()
        if stripped and stripped != "---" and not stripped.startswith("#"):
            return True
    return False
