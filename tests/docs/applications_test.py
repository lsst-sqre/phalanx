"""Tests for the application documentation pages."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from phalanx.factory import Factory
from phalanx.models.applications import Project

_SPECIAL_APPLICATIONS = (
    "nublado-fileservers",
    "nublado-users",
    "ocps-uws-job",
)
"""Applications that are implementation details and have no documentation."""


def test_descriptions() -> None:
    """Ensure all application pages have proper short descriptions."""
    doc_root = Path(__file__).parent.parent.parent / "docs" / "applications"
    for application in doc_root.iterdir():
        if not application.is_dir():
            continue
        index_path = application / "index.rst"
        index_rst = index_path.read_text()
        m = re.search(r"\n(#+)\n([^\n]+)\n\1\n", index_rst)
        assert m, f"No title found in {index_path}"
        title = m.group(2)
        assert len(title) <= 80, f"Title too long in {index_path}"
        m = re.match(r"\S+ — (\S.*$)", title)
        assert m, f"Invalid title format in {index_path}"
        description = m.group(1)
        m = re.match("[A-Z0-9]", description)
        assert m, f"Description must start with capital letter in {index_path}"


def test_applications_index() -> None:
    """Ensure all applications are mentioned in the index.

    Also check that the application is listed under the project that it is
    configured to use during installation.
    """
    doc_root = Path(__file__).parent.parent.parent / "docs" / "applications"
    seen: defaultdict[str, set[str]] = defaultdict(set)
    for project in Project:
        with (doc_root / (project.value + ".rst")).open() as fh:
            for line in fh:
                if m := re.match("^   ([^/]+)/index$", line):
                    seen[project.value].add(m.group(1))

    # Load all of the configuration.
    factory = Factory(Path(__file__).parent.parent)
    config_storage = factory.create_config_storage()
    config = config_storage.load_phalanx_config()

    # Check that the project for each application matches where it's linked in
    # the docs.
    for application in config.applications:
        if application.name in _SPECIAL_APPLICATIONS:
            continue
        project_name = application.project.value
        assert application.name in seen[project_name], (
            f"{application} in {project_name} but not linked in"
            f" docs/applications/{project_name}.rst"
        )
