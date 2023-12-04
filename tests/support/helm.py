"""Mock Helm command for testing."""

from __future__ import annotations

import subprocess
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

from typing_extensions import Protocol

from phalanx.exceptions import HelmFailedError
from phalanx.storage.helm import HelmStorage

__all__ = [
    "MockHelm",
    "MockHelmCallback",
    "patch_helm",
]


class MockHelmCallback(Protocol):
    """Protocol for Helm callbacks."""

    def __call__(*command: str) -> subprocess.CompletedProcess:
        ...


class MockHelm:
    """Mocked Helm commands captured during testing.

    This class holds a record of every Helm command that the Phalanx tooling
    under test attempted to run. It is patched into the standard Helm storage
    class, replacing the invocation of Helm via subprocess.

    Attributes
    ----------
    call_args_list
        Each call to Helm, as a list of arguments to the Helm command. The
        name is chosen to match the `unittest.mock.Mock` interface.
    """

    def __init__(self) -> None:
        self.call_args_list: list[list[str]] = []
        self._callback: MockHelmCallback | None = None

    def capture(
        self, command: str, *args: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess:
        """Mock capturing the output of a Helm command.

        Parameters
        ----------
        command
            Helm subcommand to run.
        *args
            Arguments for that subcommand.
        cwd
            If provided, change working directories to this path before
            running the Helm command.

        Returns
        -------
        subprocess.CompletedProcess
            Results of the process, containing the standard output and
            standard error streams.

        Raises
        ------
        HelmFailedError
            Raised if the ``returncode`` returned by a callback is non-zero.
        """
        self.call_args_list.append([command, *args])
        if self._callback:
            # https://github.com/python/mypy/issues/708 (which despite being
            # closed is not fixed for protocols as of mypy 1.7.0)
            result = self._callback(command, *args)  # type: ignore[misc]
            if result.returncode != 0:
                exc = subprocess.CalledProcessError(
                    returncode=result.returncode,
                    cmd=[command, *args],
                    output=result.stdout,
                    stderr=result.stderr,
                )
                raise HelmFailedError(command, args, exc)
            return result
        else:
            return subprocess.CompletedProcess(
                args=[command, *args], returncode=0, stdout=None, stderr=None
            )

    def reset_mock(self) -> None:
        """Clear the list of previous calls."""
        self.call_args_list = []

    def run(
        self,
        command: str,
        *args: str,
        cwd: Path | None = None,
        quiet: bool = False,
    ) -> None:
        """Mock running a Helm command.

        Parameters
        ----------
        command
            Helm subcommand being run run.
        *args
            Arguments for that subcommand.
        cwd
            If provided, the caller is requesting to change working
            directories to this path before running the Helm command.
            (Currently ignored.)
        quiet
            Whether to suppress Helm's standard output. (Currently ignored.)
        """
        self.call_args_list.append([command, *args])

    def set_capture_callback(self, callback: MockHelmCallback) -> None:
        """Set the callback called when capturing Helm command output.

        If no callback is set, empty standard output and standard error will
        be returned by the mock.

        Parameters
        ----------
        callback
            Callback run whenever the Phalanx code under test captures the
            output of a Helm command. The callback will be passed the Helm
            command as a list, and is expected to return a
            `subprocess.CompletedProcess` object. If ``returncode`` is
            non-zero, the mock will raise `subprocess.CalledProcessError`.
        """
        self._callback = callback


def patch_helm() -> Iterator[MockHelm]:
    """Intercept Helm invocations with a mock.

    Each attempt to run a Helm command will be captured in the mock and not
    actually run.

    Yields
    ------
    MockHelm
        Class that captures the attempted Helm commands.
    """
    mock = MockHelm()
    with patch.object(HelmStorage, "_capture_helm", side_effect=mock.capture):
        with patch.object(HelmStorage, "_run_helm", side_effect=mock.run):
            yield mock
