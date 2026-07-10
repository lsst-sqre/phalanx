"""Sphinx configuration for Phalanx documentation."""

from typing import Dict
from pathlib import Path

from documenteer.conf.guide import *
from jinja2 import StrictUndefined
from sphinx.application import Sphinx

from phalanx.docs.jinja import build_jinja_contexts
from phalanx.docs.sphinx import build_discovery


# Exclude templates from rendering in the documentation output.
exclude_patterns.extend(
    [
        "_templates/**",
        "environments/_summary.rst.jinja",
        "applications/_summary.rst.jinja",
    ]
)

# Include JSON schemas in the documentation output tree.
html_extra_path = ["extras"]

# Construct the Jinja contexts for templating dynamically from the Phalanx
# application and environment configuration.
jinja_contexts = build_jinja_contexts()
jinja_env_kwargs = {
    "lstrip_blocks": True,
    "undefined": StrictUndefined,
}

# Suppress warnings about the inability to cache the Jinja configuration.
suppress_warnings = ["config.cache"]

# Do not linkcheck internal anchors, and do not linkcheck any links in the
# documentation generated from values files.
linkcheck_anchors = False
linkcheck_exclude_documents = [
    r"applications/.*/values",
]

# Add generation of service discovery files to the documentation build.
def setup(app: Sphinx) -> None:
    app.connect("builder-inited", lambda app: build_discovery(app.srcdir))
