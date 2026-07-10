"""Generate service discovery JSON dumps for every environment."""

import json
from pathlib import Path
from urllib.parse import urljoin

from pydantic.alias_generators import to_camel
from rubin.repertoire import RepertoireBuilder, RepertoireSettings

from ..factory import Factory

__all__ = ["build_discovery"]


def build_discovery(srcdir: str) -> None:
    """Construct service discovery dumps for every Phalanx environment.

    These will go in :file:`extras/environments/{environment}.json`, from
    which they will be copied into the output tree during the Sphinx build.
    These files can then be used by other documentation builds that want to
    use service discovery information, such as for lists of services available
    in environents or to embed links to specific services.

    Parameters
    ----------
    srcdir
        Root of the source directory.
    """
    source_path = Path(srcdir)
    factory = Factory(source_path.parent)
    config_storage = factory.create_config_storage()
    root_path = source_path / "extras" / "discovery" / "environments"
    root_path.mkdir(parents=True, exist_ok=True)

    # Process each environment.
    for env_name in config_storage.list_environments():
        environment = config_storage.load_environment(env_name)
        repertoire = environment.applications.get("repertoire")
        if not repertoire or not repertoire.values.get("config"):
            continue

        # Flesh out the Repertoire coniguration with settings that would be
        # injected by Argo CD, and calculate the base URLs for service
        # discovery.
        config = repertoire.values["config"]
        config["applications"] = list(environment.applications.keys())
        config["baseHostname"] = environment.fqdn
        if environment.butler_server_repositories:
            config["butlerConfigs"] = {
                k: str(v)
                for k, v in environment.butler_server_repositories.items()
            }
        config["environmentName"] = env_name
        base_url = f"https://{environment.fqdn}/"
        repertoire_base_url = urljoin(base_url, config["pathPrefix"])

        # RepertoireSettings uses extra="forbid", but the merged configuration
        # is for the Repertoire service and has extra fields. Delete the
        # fields that aren't part of the Repertoire settings.
        known_fields = {to_camel(k) for k in RepertoireSettings.model_fields}
        to_remove = set(config.keys()) - known_fields
        for field_name in to_remove:
            del config[field_name]

        # Now, load the Repertoire configuration and generate service
        # discovery information for that environment.
        settings = RepertoireSettings.model_validate(config)
        builder = RepertoireBuilder(settings)
        discovery = builder.build_discovery(repertoire_base_url, base_url)

        # Write out the discovery information.
        with (root_path / f"{env_name}.json").open("w") as fh:
            discovery_json = discovery.model_dump(
                mode="json", exclude_defaults=True
            )
            json.dump(discovery_json, fh, indent=2, sort_keys=True)
