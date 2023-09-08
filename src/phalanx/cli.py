"""Phalanx command-line interface."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
import yaml
from pydantic import BaseModel
from pydantic.tools import schema_of
from safir.click import display_help

from .constants import VAULT_WRITE_TOKEN_LIFETIME
from .factory import Factory
from .models.environments import EnvironmentConfig
from .models.helm import HelmStarter
from .models.secrets import ConditionalSecretConfig, StaticSecret

__all__ = [
    "help",
    "main",
    "application",
    "application_create",
    "environment",
    "environment_schema",
    "secrets",
    "secrets_audit",
    "secrets_list",
    "secrets_onepassword_secrets",
    "secrets_schema",
    "secrets_static_template",
    "secrets_vault_secrets",
    "vault",
    "vault_audit",
    "vault_create_read_approle",
    "vault_create_write_token",
]


def _find_config() -> Path:
    """Find the root of the Phalanx configuration tree.

    Returns
    -------
    Path
        Root of the tree.

    Raises
    ------
    click.UsageError
        Raised if we reach the root of the file system and did not locate the
        Phalanx configuration tree.
    """
    current = Path.cwd()

    def _is_config(path: Path) -> bool:
        if not (path / "environments").is_dir():
            return False
        if not (path / "applications").is_dir():
            return False
        return True

    while not _is_config(current):
        if current.parent == current:
            msg = "Cannot locate root of Phalanx configuration"
            raise click.UsageError(msg)
        current = current.parent
    return current


def _load_static_secrets(path: Path) -> dict[str, dict[str, StaticSecret]]:
    """Load static secrets from a file.

    Parameters
    ----------
    path
        Path to the file.

    Returns
    -------
    dict of dict
        Map from application to secret key to
        `~phalanx.models.secrets.StaticSecret`.
    """
    with path.open() as fh:
        static_secrets = yaml.safe_load(fh)

    # Pydantic can't parse a dictionary with arbitrary keys directly, so use a
    # workaround: define a model with one attribute that corresponds to the
    # nested dictionary we're expecting, and then parse the file contents with
    # a synthetic top-level key matching that attribute.
    class _StaticSecrets(BaseModel):
        secrets: dict[str, dict[str, StaticSecret]]

    model = _StaticSecrets.parse_obj({"secrets": static_secrets})
    return model.secrets


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(message="%(version)s")
def main() -> None:
    """Administrative command-line interface for Phalanx."""


@main.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.argument("subtopic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx: click.Context, topic: str | None, subtopic: str | None) -> None:
    """Show help for any command."""
    display_help(main, ctx, topic, subtopic)


@main.group()
def application() -> None:
    """Commands for Phalanx application configuration."""


@application.command("create")
@click.argument("name")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
@click.option(
    "-d",
    "--description",
    prompt="Short description",
    help="Short description of the new application.",
)
@click.option(
    "-s",
    "--starter",
    type=click.Choice([s.value for s in HelmStarter]),
    default=HelmStarter.WEB_SERVICE.value,
    help="Helm starter to use as the basis for the chart.",
)
def application_create(
    name: str, *, starter: str, config: Path | None, description: str
) -> None:
    """Create a new application from a starter template.

    This command creates the framework for a new Phalanx application from the
    named template (which must be one of the starter charts) and adds the
    appropriate documentation stubs, Argo CD Application resource, and
    environment configuration.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    application_service = factory.create_application_service()
    application_service.create_application(
        name, HelmStarter(starter), description
    )


@main.group()
def environment() -> None:
    """Commands for Phalanx environment configuration."""


@environment.command("schema")
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to which to write schema.",
)
def environment_schema(*, output: Path | None) -> None:
    """Generate schema for environment configuration.

    The output is a JSON schema for the values-<environment>.yaml file for a
    Phalanx environment. If the ``--output`` flag is not given, the schema is
    printed to standard output.

    Users normally don't need to run this command. It is used to update the
    schema file in the Phalanx repository, which is used by a pre-commit hook
    to validate environment configuration files before committing them.
    """
    json_schema = EnvironmentConfig.schema_json(indent=2) + "\n"
    if output:
        output.write_text(json_schema)
    else:
        sys.stdout.write(json_schema)


@main.group()
def secrets() -> None:
    """Secret manipulation commands."""


@secrets.command("audit")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
@click.option(
    "--secrets",
    type=click.Path(path_type=Path),
    default=None,
    help="YAML file containing static secrets for this environment.",
)
def secrets_audit(
    environment: str, *, config: Path | None, secrets: Path | None
) -> None:
    """Audit secrets for an environment.

    The secrets stored in Vault for the given environment will be compared to
    the secrets required for all applications enabled for that environment,
    and any discrepencies will be noted. The audit report will be printed to
    standard output and will be empty if no issues were found.

    The environment variable VAULT_TOKEN must be set to a token with read
    access to the Vault data for the given environment.
    """
    if not config:
        config = _find_config()
    static_secrets = None
    if secrets:
        static_secrets = _load_static_secrets(secrets)
    factory = Factory(config)
    secrets_service = factory.create_secrets_service()
    sys.stdout.write(secrets_service.audit(environment, static_secrets))


@secrets.command("list")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
def secrets_list(environment: str, *, config: Path | None) -> None:
    """List all secrets required for a given environment."""
    if not config:
        config = _find_config()
    factory = Factory(config)
    secrets_service = factory.create_secrets_service()
    secrets = secrets_service.list_secrets(environment)
    for secret in secrets:
        print(secret.application, secret.key)


@secrets.command("onepassword-secrets")
@click.argument("environment")
@click.argument("output", type=click.Path(path_type=Path))
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
def secrets_onepassword_secrets(
    environment: str, output: Path, *, config: Path | None
) -> None:
    """Write the 1Password secrets for the given environment.

    One JSON file per application with secrets will be created in the output
    directory, containing the secrets for that application. If the value of a
    secret is not known, it will be written as null.

    The environment variable OP_CONNECT_TOKEN must be set to the 1Password
    Connect token for the given environment.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    secrets_service = factory.create_secrets_service()
    secrets_service.save_onepassword_secrets(environment, output)


@secrets.command("schema")
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to which to write schema.",
)
def secrets_schema(*, output: Path | None) -> None:
    """Generate schema for application secret definition.

    The output is a JSON schema for the secrets.yaml file for an application,
    which specifies the secrets required for that application. If the
    ``--output`` flag is not given, the schema is printed to standard output.

    Users normally don't need to run this command. It is used to update the
    schema file in the Phalanx repository, which is used by a pre-commit hook
    to validate secrets.yaml files before committing them.
    """
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

    json_schema = json.dumps(schema, indent=2) + "\n"
    if output:
        output.write_text(json_schema)
    else:
        sys.stdout.write(json_schema)


@secrets.command("static-template")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
def secrets_static_template(environment: str, *, config: Path | None) -> None:
    """Generate a template for static secrets.

    Static secrets may be provided to other commands that need to know them
    (most notably ``phalanx secrets sync``) via the ``--secrets`` flag, which
    points to a YAML file containing the static secrets for an environment.
    This command generates a template for that YAML file. It will contain the
    descriptions for each secret and a place for the value of that secret to
    be filled in.

    The template is public information, but (somewhat obviously) once secret
    values have been added to it, this file must be kept secure and private to
    Phalanx administrators for that environment.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    secrets_service = factory.create_secrets_service()
    sys.stdout.write(secrets_service.generate_static_template(environment))


@secrets.command("sync")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
@click.option(
    "--delete",
    default=False,
    is_flag=True,
    help="Delete any unexpected secrets in Vault.",
)
@click.option(
    "--regenerate",
    default=False,
    is_flag=True,
    help="Regenerate (change) all generated secrets.",
)
@click.option(
    "--secrets",
    type=click.Path(path_type=Path),
    default=None,
    help="YAML file containing static secrets for this environment.",
)
def secrets_sync(
    environment: str,
    *,
    config: Path | None,
    delete: bool,
    regenerate: bool,
    secrets: Path | None,
) -> None:
    """Synchronize environment secrets with Vault.

    The secrets required for all enabled applications for the given
    environment are compared with the secrets stored for that environment in
    Vault, any missing or incorrect secrets are updated, and optionally any
    extraneous secrets may be deleted.

    The environment variable VAULT_TOKEN must be set to a token with read and
    write access to the secrets for this environment (and optionally delete
    access). If Vault credentials are managed through this tool, such a token
    can be created with the ``phalanx vault create-write-token`` command.
    """
    if not config:
        config = _find_config()
    static_secrets = None
    if secrets:
        static_secrets = _load_static_secrets(secrets)
    factory = Factory(config)
    secrets_service = factory.create_secrets_service()
    secrets_service.sync(
        environment, static_secrets, regenerate=regenerate, delete=delete
    )


@secrets.command("vault-secrets")
@click.argument("environment")
@click.argument("output", type=click.Path(path_type=Path))
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
def secrets_vault_secrets(
    environment: str, output: Path, *, config: Path | None
) -> None:
    """Write the Vault secrets for the given environment.

    One JSON file per application with secrets will be created in the output
    directory, containing the secrets for that application. If the value of a
    secret is not known, it will be written as null.

    The environment variable VAULT_TOKEN must be set to a token with read
    access to the Vault data for the given environment.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    secrets_service = factory.create_secrets_service()
    secrets_service.save_vault_secrets(environment, output)


@main.group()
def vault() -> None:
    """Vault management commands."""


@vault.command("audit")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
def vault_audit(environment: str, *, config: Path | None) -> None:
    """Audit Vault credentials for an environment.

    The audit report will be printed to standard output and will be empty if
    no issues were found.

    The environment variable VAULT_TOKEN must be set to a token with access to
    read policies, AppRoles, tokens, and token accessors.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    vault_service = factory.create_vault_service()
    report = vault_service.audit(environment)
    if report:
        sys.stdout.write(report)
        sys.exit(1)


@vault.command("create-read-approle")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
def vault_create_read_approle(
    environment: str, *, config: Path | None
) -> None:
    """Create a new Vault read AppRole.

    The created AppRole will have read access to all of the Vault secrets for
    the given environment. It is intended for use by vault-secrets-operator to
    maintain Kubernetes secrets from the Phalanx Vault secrets.

    The environment variable VAULT_TOKEN must be set to a token with access to
    create policies and AppRoles, list AppRole SecretID accessors, and revoke
    AppRole SecretIDs.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    vault_service = factory.create_vault_service()
    vault_approle = vault_service.create_read_approle(environment)
    sys.stdout.write(vault_approle.to_yaml())


@vault.command("create-write-token")
@click.argument("environment")
@click.option(
    "-c",
    "--config",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to root of Phalanx configuration.",
)
@click.option(
    "--lifetime",
    type=str,
    default=VAULT_WRITE_TOKEN_LIFETIME,
    help="Token lifetime in Vault duration format.",
)
def vault_create_write_token(
    environment: str, *, config: Path | None, lifetime: str
) -> None:
    """Create a new Vault write token.

    The created token will have read, write, delete, and destroy access to all
    of the Vault secrets for the given environment. It is intended for
    interactive use with this tool synchronize environment secrets to Vault.

    The environment variable VAULT_TOKEN must be set to a token with access to
    list token accessors, create policies, and create and revoke tokens.
    """
    if not config:
        config = _find_config()
    factory = Factory(config)
    vault_service = factory.create_vault_service()
    vault_token = vault_service.create_write_token(environment, lifetime)
    sys.stdout.write(vault_token.to_yaml())
