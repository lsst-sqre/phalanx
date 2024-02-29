"""Tests for the application documentation pages."""

from __future__ import annotations

import re
from pathlib import Path


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
    """Ensure all applications are mentioned in the index."""
    doc_root = Path(__file__).parent.parent.parent / "docs" / "applications"
    seen = set()
    with (doc_root / "index.rst").open() as fh:
        for line in fh:
            if m := re.match("^   ([^/]+)/index$", line):
                seen.add(m.group(1))
    root_path = Path(__file__).parent.parent.parent / "applications"
    for project in root_path.iterdir():
        if not project.is_dir():
            continue
        for application in project.iterdir():
            if application.name in (
                "nublado-fileservers",
                "nublado-users",
                "ocps-uws-job",
            ):
                continue
            assert (
                application.name in seen
            ), f"{application.name} not lined in docs/applications/index.rst"
