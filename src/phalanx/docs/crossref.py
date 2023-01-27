"""Cross-referencing roles and directives for Phalanx topics."""

from __future__ import annotations

from sphinx.application import Sphinx

__all__ = ["setup"]


def setup(app: Sphinx) -> None:
    """Set up the Phalan cross-referencing extensions."""
    # Cross reference an environment's homepage
    app.add_crossref_type(
        "px-env",
        "px-env",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    # Cross reference an app's homepage
    app.add_crossref_type(
        "px-app",
        "px-app",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    # Cross reference an app's architectural notes page
    app.add_crossref_type(
        "px-app-notes",
        "px-app-notes",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    # Cross reference an app's bootstrapping page
    app.add_crossref_type(
        "px-app-bootstrap",
        "px-app-bootstrap",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    # Cross reference an app's upgrade page
    app.add_crossref_type(
        "px-app-upgrade",
        "px-app-upgrade",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    # Cross reference an app's troubleshooting page
    app.add_crossref_type(
        "px-app-troubleshooting",
        "px-app-troubleshooting",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
    # Cross reference an app's Helm values page
    app.add_crossref_type(
        "px-app-values",
        "px-app-values",
        indextemplate="single: %s",
        ref_nodeclass=None,
        objname="",
        override=False,
    )
