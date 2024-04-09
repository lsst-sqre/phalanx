"""Utility functions used when running under GitHub Actions.

The utility functions in this module can all be called unconditionally. They
will detect whether the Phalanx command-line tool is being run under GitHub
Actions and, if so, add additional GitHub-specific markers to the output to
improve display in GitHub Actions logs.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

__all__ = [
    "action_group",
]


@contextmanager
def action_group(title: str) -> Iterator[None]:
    """Wrap a sequence of commands in a GitHub Actions group.

    Must be used as a context manager. Any output produced by code that runs
    within that context manager will be wrapped into a GitHub Actions display
    group with the given title.

    Parameters
    ----------
    title
        Title of display group.
    """
    in_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
    if in_github_actions:
        print(f"::group::{title}", flush=True)
    yield
    if in_github_actions:
        print("::endgroup::", flush=True)
