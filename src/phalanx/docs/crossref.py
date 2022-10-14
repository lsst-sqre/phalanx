"""Cross-referencing roles and directives for Phalanx topics."""

from __future__ import annotations

from sphinx.application import Sphinx

__all__ = ["setup"]


def setup(app: Sphinx) -> None:
    """Set up the Phalan cross-referencing extensions."""
    app.add_crossref_type(
        "px-env",
        "px-env",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    app.add_crossref_type(
        "px-app",
        "px-app",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
