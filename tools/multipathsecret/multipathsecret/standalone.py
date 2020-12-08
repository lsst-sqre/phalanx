import click
from .vaultconfig import VaultConfig


@click.group()
@click.option("--vault-address", "-a")
@click.option("--secret-name", "-n", required=True)
@click.option("--vault-file", "-v", required=True)
@click.option("--omit", "-o", multiple=True)
@click.option("--dry-run", "-x", is_flag=True)
@click.pass_context
def cli(ctx, vault_address, vault_file, omit, secret_name, dry_run):
    ctx.ensure_object(dict)
    ctx.obj['vault_config'] = VaultConfig(vault_address=vault_address,
                                          vault_file=vault_file,
                                          skip_list=omit)
    ctx.obj['options'] = {'secret_name': secret_name,
                          'dry_run': dry_run}


@cli.command()
@click.pass_context
@click.option("--secret-file", "-s", required=True)
def add(ctx, secret_file):
    vc = ctx.obj['vault_config']
    vc.load_secret(secret_file)
    opts = ctx.obj['options']
    vc.add_secrets(secret_name=opts['secret_name'],
                   dry_run=opts['dry_run'])


@cli.command()
@click.pass_context
def remove(ctx):
    vc = ctx.obj['vault_config']
    opts = ctx.obj['options']
    vc.remove_secrets(secret_name=opts['secret_name'],
                      dry_run=opts['dry_run'])
