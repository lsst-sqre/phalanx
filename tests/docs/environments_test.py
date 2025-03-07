"""Tests for the environment documentation pages."""

from __future__ import annotations

import re
from pathlib import Path


def test_environments() -> None:
    """Ensure all environments are documented."""
    doc_root = Path(__file__).parent.parent.parent / "docs" / "environments"
    seen_dir = set()
    for environment in doc_root.iterdir():
        if environment.is_dir():
            seen_dir.add(environment.name)
    seen_index = set()
    with (doc_root / "index.rst").open() as fh:
        for line in fh:
            if m := re.match("^   ([^/]+)/index$", line):
                seen_index.add(m.group(1))
    root_path = Path(__file__).parent.parent.parent / "environments"
    environments = [
        v.stem.removeprefix("values-")
        for v in sorted(root_path.glob("values-*.yaml"))
    ]
    for environment_name in environments:
        assert environment_name in seen_dir, (
            f"{environment_name} not documented in docs/environments"
        )
        assert environment_name in seen_index, (
            f"{environment_name} not linked in docs/environments/index.rst"
        )
