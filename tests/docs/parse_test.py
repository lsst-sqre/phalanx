"""Tests ensuring that the Phalanx configuration can be parsed."""

from __future__ import annotations

import os
from pathlib import Path

from phalanx.docs.jinja import build_jinja_contexts


def test_parse() -> None:
    """Ensure the Phalanx configuration can be parsed into doc models."""
    cwd = Path.cwd()
    os.chdir(str(Path(__file__).parent.parent.parent / "docs"))
    try:
        build_jinja_contexts()
    finally:
        os.chdir(str(cwd))
