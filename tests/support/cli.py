"""Helper functions for running command-line tests."""

from pathlib import Path

from click.testing import CliRunner, Result

from phalanx.cli import main

__all__ = ["run_cli"]


def run_cli(
    *command: str,
    env: dict[str, str] | None = None,
    needs_config: bool = True,
    stdin: str | None = None,
) -> Result:
    """Run the given command in the Click testing harness.

    The command will always be run with exception catching disabled.

    Parameters
    ----------
    *command
        Command to run.
    env
        Environment variable overrides.
    needs_config
        Whether to add the ``--config`` flag pointing to the test data to the
        end of the command.
    stdin
        Optional input for commands that prompt.
    """
    args = list(command)
    if needs_config:
        root_path = Path(__file__).parent.parent / "data" / "input"
        args.extend(["--config", str(root_path)])
    runner = CliRunner()
    return runner.invoke(
        main, args, catch_exceptions=False, env=env, input=stdin
    )
