"""Generate service discovery JSON dumps for every environment."""

import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

from rubin.repertoire import RepertoireBuilder

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
    mapping: defaultdict[str, dict[str, str]] = defaultdict(dict)
    for env_name in config_storage.list_environments():
        environment = config_storage.load_environment(env_name)
        settings = environment.build_repertoire_settings()
        if not settings:
            continue
        config = environment.applications["repertoire"].values["config"]

        # Generate service discovery information for that environment.
        base_url = f"https://{environment.fqdn}/"
        repertoire_base_url = urljoin(base_url, config["pathPrefix"])
        builder = RepertoireBuilder(settings)
        discovery = builder.build_discovery(repertoire_base_url, base_url)

        # Write out the discovery information.
        with (root_path / f"{env_name}.json").open("w") as fh:
            discovery_json = discovery.model_dump(
                mode="json", exclude_defaults=True
            )
            json.dump(discovery_json, fh, indent=2, sort_keys=True)

        # Add this environment to the index.
        mapping[env_name]["url"] = (
            f"https://phalanx.lsst.io/discovery/environments/{env_name}.json"
        )

    # Write out the index file.
    with (root_path / "index.json").open("w") as fh:
        json.dump(mapping, fh, indent=2, sort_keys=True)
