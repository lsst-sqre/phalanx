"""Models for Helm commands."""

from __future__ import annotations

from enum import Enum

__all__ = ["HelmStarter"]


class HelmStarter(Enum):
    """A Helm chart starter.

    This must be kept in sync with the contents of the :file:`starters`
    directory.

    Notes
    -----
    This should be determined dynamically from the contents of the
    :file:`starters` directory, but the Phalanx configuration location can be
    specified with a flag at runtime and we want to tell Click about the list
    of available starters. This is therefore an imperfect compromise:
    hard-code the list of available starters in the source code but add a test
    so that if someone adds a new starter without updating this list, the test
    will fail.
    """

    EMPTY = "empty"
    WEB_SERVICE = "web-service"
    FASTAPI_SAFIR = "fastapi-safir"
