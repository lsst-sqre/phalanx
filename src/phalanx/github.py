"""Utility functions used when running under GitHub Actions.

The utility functions in this module can all be called unconditionally. They
will detect whether the Phalanx command-line tool is being run under GitHub
Actions and, if so, add additional GitHub-specific markers to the output to
improve display in GitHub Actions logs.

See `GitHub's documentation
<https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions>`__
for other possibly useful commands that could be added.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import SecretStr

__all__ = [
    "action_group",
    "add_mask",
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


def add_mask(secret: str | SecretStr) -> None:
    """Mask a secret in future GitHub Actions output.

    Tell GitHub Actions to hide any occurrences of the provided secret in
    subsequent GitHub Actions output. The primary use is to register secrets
    that may otherwise appear in backtraces or other output so that they're
    not leaked into the GitHub Actions logs.

    Parameters
    ----------
    secret
        Secret to mask.
    """
    if os.getenv("GITHUB_ACTIONS") == "true":
        if isinstance(secret, SecretStr):
            value = secret.get_secret_value()
        else:
            value = secret
        print(f"::add-mask::{value}", flush=True)
