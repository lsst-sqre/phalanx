"""Sphinx configuration for Phalanx documentation."""

from typing import Dict
from pathlib import Path

from documenteer.conf.guide import *
from jinja2 import StrictUndefined

from phalanx.docs.jinja import build_jinja_contexts


exclude_patterns.extend(
    [
        "environments/_summary.rst.jinja",
        "applications/_summary.rst.jinja",
    ]
)

# Include JSON schemas in the documentation output tree.
html_extra_path = ["extras"]

jinja_contexts = build_jinja_contexts()
jinja_env_kwargs = {
    "lstrip_blocks": True,
    "undefined": StrictUndefined,
}

linkcheck_anchors = False
linkcheck_exclude_documents = [
    r"applications/.*/values",
]
