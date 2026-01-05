"""Helpers for testing code that shells out to kubectl."""

from collections.abc import Iterator
from unittest.mock import Mock, patch

from phalanx.storage import kubernetes

__all__ = ["patch_kubectl"]


def patch_kubectl() -> Iterator[Mock]:
    """Patch the kubectl Command in the kubernetes storage with a mock."""
    mock = Mock()
    with patch.object(kubernetes, "Command", return_value=mock):
        yield mock
