"""Mock Helm command for testing."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

from phalanx.storage.helm import HelmStorage

__all__ = [
    "MockHelm",
    "patch_helm",
]


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

    def reset_mock(self) -> None:
        """Clear the list of previous calls."""
        self.call_args_list = []

    def run(self, command: str, *args: str, cwd: Path | None = None) -> None:
        """Capture a Helm command.

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
        """
        self.call_args_list.append([command, *args])


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
    with patch.object(HelmStorage, "_run_helm", side_effect=mock.run):
        yield mock
