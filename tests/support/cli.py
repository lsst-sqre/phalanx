"""Helper functions for running command-line tests."""

from __future__ import annotations

from click.testing import CliRunner, Result

from phalanx.cli import main

from .data import phalanx_test_path

__all__ = ["run_cli"]


def run_cli(
    *command: str, needs_config: bool = True, stdin: str | None = None
) -> Result:
    """Run the given command in the Click testing harness.

    The command will always be run with exception catching disabled.

    Parameters
    ----------
    *command
        Command to run.
    needs_config
        Whether to add the ``--config`` flag pointing to the test data to the
        end of the command.
    stdin
        Optional input for commands that prompt.
    """
    args = list(command)
    if needs_config:
        args.extend(["--config", str(phalanx_test_path())])
    runner = CliRunner()
    return runner.invoke(main, args, catch_exceptions=False, input=stdin)
