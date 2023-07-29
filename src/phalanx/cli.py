"""Phalanx command-line interface."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from pydantic.tools import schema_of

from .factory import Factory
from .models.secrets import ConditionalSecretConfig

__all__ = [
    "help",
    "secrets_audit",
    "secrets_list",
    "secrets_schema",
    "secrets_static_template",
    "secrets_vault_secrets",
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


@secrets.command("audit")
@click.argument("environment")
def secrets_audit(environment: str) -> None:
    """Audit the secrets for the given environment for inconsistencies."""
    factory = Factory()
    secrets_service = factory.create_secrets_service()
    sys.stdout.write(secrets_service.audit(environment))


@secrets.command("list")
@click.argument("environment")
def secrets_list(environment: str) -> None:
    """List all secrets required for a given environment."""
    factory = Factory()
    secrets_service = factory.create_secrets_service()
    secrets = secrets_service.list_secrets(environment)
    for secret in secrets:
        print(secret.application, secret.key)


@secrets.command("schema")
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to which to write schema.",
)
def secrets_schema(*, output: Path | None) -> None:
    """Generate schema for application secret definition."""
    schema = schema_of(
        dict[str, ConditionalSecretConfig],
        title="Phalanx application secret definitions",
    )

    # Pydantic v1 doesn't have any way that I can find to add attributes to
    # the top level of a schema that isn't generated from a model, and the
    # top-level secrets schema is a dict, so manually add in the $id attribute
    # pointing to the canonical URL. Do this in a slightly odd way so that the
    # $id attribute will be at the top of the file, not at the bottom.
    schema = {"$id": "https://phalanx.lsst.io/schemas/secrets.json", **schema}

    json_schema = json.dumps(schema, indent=2)
    if output:
        output.write_text(json_schema)
    else:
        sys.stdout.write(json_schema)


@secrets.command("static-template")
@click.argument("environment")
def secrets_static_template(environment: str) -> None:
    """Generate a template for providing static secrets for an environment."""
    factory = Factory()
    secrets_service = factory.create_secrets_service()
    sys.stdout.write(secrets_service.generate_static_template(environment))


@secrets.command("vault-secrets")
@click.argument("environment")
@click.argument("output", type=click.Path(path_type=Path))
def secrets_vault_secrets(environment: str, output: Path) -> None:
    """Write the Vault secrets for the given environment.

    One JSON file per application with secrets will be created in the output
    directory, containing the secrets for that application. If the value of a
    secret is not known, it will be written as null.
    """
    factory = Factory()
    secrets_service = factory.create_secrets_service()
    secrets_service.generate_vault_secrets(environment, output)
