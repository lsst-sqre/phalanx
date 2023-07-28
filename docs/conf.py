from typing import Dict
from pathlib import Path

from documenteer.conf.guide import *  # noqa: F401 F403

from phalanx.docs.models import Phalanx as PhalanxModel

phalanx_metadata = PhalanxModel.load_phalanx(Path(__file__).parent.parent)
jinja_contexts: Dict[str, Dict] = {}
for env in phalanx_metadata.environments:
    jinja_contexts[env.name] = {"env": env}
for app in phalanx_metadata.apps:
    jinja_contexts[app.name] = {
        "app": app,
        "envs": {env.name: env for env in phalanx_metadata.environments},
    }


jinja_env_kwargs = {
    "lstrip_blocks": True,
}

exclude_patterns.extend(  # noqa: F405
    [
        "requirements.txt",
        "environments/_summary.rst.jinja",
        "applications/_summary.rst.jinja",
    ]
)

linkcheck_anchors = False
linkcheck_exclude_documents = [
    r"applications/.*/values",
]

# Include JSON schemas in the documentation output tree.
html_extra_path = ["extras"]
