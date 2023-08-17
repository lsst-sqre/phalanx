"""Helper functions for Sphinx Jinja templating."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..factory import Factory

__all__ = ["build_jinja_contexts"]


def build_jinja_contexts() -> dict[str, dict[str, Any]]:
    """Construct the Jinja contexts used for building Phalanx documentation.

    Must be run from the root of the Phalanx documentation tree (a
    subdirectory of the configuration tree). This is normally arranged by
    Sphinx.

    Returns
    -------
    dict of dict
        Dict of contexts. There will be top-level keys for each environment
        and for each application. The former will have an ``env`` key
        containing the environment details. The latter will have an ``app``
        key contianing the application and an ``envs`` key containing all
        the environment details.
    """
    factory = Factory(Path.cwd().parent)
    config_storage = factory.create_config_storage()
    phalanx_metadata = config_storage.load_phalanx_config()
    jinja_contexts: dict[str, dict[str, Any]] = {}
    for environment in phalanx_metadata.environments:
        jinja_contexts[environment.name] = {"env": environment}
    for application in phalanx_metadata.applications:
        jinja_contexts[application.name] = {
            "app": application,
            "envs": {e.name: e for e in phalanx_metadata.environments},
        }
    return jinja_contexts
