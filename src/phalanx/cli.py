"""Phalanx command-line interface."""

from __future__ import annotations

import click

from phalanx.factory import Factory

__all__ = [
    "help",
    "secrets_list",
]


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(message="%(version)s")
def main() -> None:
    """Administrative command-line interface for gafaelfawr."""


@main.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx: click.Context, topic: str | None) -> None:
    """Show help for any command."""
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic:
        if topic in main.commands:
            click.echo(main.commands[topic].get_help(ctx))
        else:
            raise click.UsageError(f"Unknown help topic {topic}", ctx)
    else:
        if not ctx.parent:
            raise RuntimeError("help called without topic or parent")
        click.echo(ctx.parent.get_help())


@main.group()
def secrets() -> None:
    """Secret manipulation commands."""


@secrets.command("list")
@click.argument("environment")
def secrets_list(environment: str) -> None:
    """List all secrets required for a given environment."""
    factory = Factory()
    secrets_service = factory.create_secrets_service()
    secrets = secrets_service.list_secrets(environment)
    for secret in secrets:
        print(secret.application, secret.key)
