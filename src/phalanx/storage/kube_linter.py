"""Storage layer for running kube-linter on rendered Kubernetes resources."""

import sys
from pathlib import Path

from ..exceptions import CommandFailedError
from .command import Command

__all__ = ["KubeLinterStorage"]


class KubeLinterStorage:
    """Storage layer for running :command:`kube-linter`.

    :command:`kube-linter` checks rendered Kubernetes resources for problems
    that :command:`helm lint` cannot see, such as two environment variables
    with the same name in one container. The checks to run are configured in
    the :file:`.kube-linter.yaml` file at the root of the Phalanx repository.

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
                "--config",
                str(self._config_path),
                "-",
                stdin=resources,
            )
        except CommandFailedError as e:
            if e.stdout:
                sys.stdout.write(e.stdout)
                sys.stdout.flush()
            if e.stderr:
                sys.stderr.write(e.stderr)
            msg = (
                f"Error: Application {application} in environment"
                f" {environment} has kube-linter errors\n"
            )
            sys.stderr.write(msg)
            return False
        return True
