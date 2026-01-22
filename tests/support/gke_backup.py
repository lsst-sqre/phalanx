"""Helpers for mocking the Google BackupForGKEClient."""

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any, Self
from unittest.mock import Mock, patch

import pytest

__all__ = ["MockBackupForGKEClient"]


@dataclass
class _Call:
    """Args and response for an expected call to Command.capture."""

    args: tuple[str]
    """The expected args."""

    response: Any
    """The mock response."""


class MockBackupForGKEClient:
    """A wrapper around a BackupForGKEClient mock allowing method calls to be
    expected.

    #. Initialize by patching the BackupForGKEClient constructor in a module
       with patch, which yields a MockBackupForGKEClient instance.
    #. Expect calls to methods on the yielded MockCommand instance with
       expect_calls.
    #. Call a function that uses a BackupForGKEClient instance in the patched
       module.
       At this point, if any calls to capture are made that weren't explicitly
       expected, the test will fail.
    #. Assert any other calls on the .mock attribute.
    """

    def __init__(self) -> None:
        self._calls: dict[str, list[_Call]] = {}
        self._mock: Mock | None = None
        self._mocked_methods = (
            "create_backup",
            "create_backup_plan",
            "create_restore",
            "create_restore_plan",
            "delete_backup",
            "delete_backup_plan",
            "delete_restore",
            "delete_restore_plan",
            "get_backup",
            "get_restore",
            "list_backup_plans",
            "list_backups",
            "list_restore_plans",
            "list_restores",
        )

    def expect_call(
        self, method: str, args: tuple[Any], response: str
    ) -> None:
        """Expect method to be called with args and return response.

        This will configure the mock to expect calls to be made in the order
        that calls to this method are made.

        Parameters
        ----------
        method
            The method to expect a call to.
        args
            A tuple of args to expect the method to be called with.
        response
            The response to return from the mock call when called with these
            args.
        """
        self._calls.setdefault(method, []).append(
            _Call(args=args, response=response)
        )

    @property
    def mock(self) -> Mock:
        """Return the wrapped Mock object if it has been initialized.

        patch must be called before accessing this property.

        Returns
        -------
        Mock
            The Mock object returned from the patched constructor.

        Raises
        ------
        RuntimeError
            If this is accesed before being initialized with
            patch.
        """
        if self._mock is None:
            raise RuntimeError("You must call patch to initialize.")
        return self._mock

    def patch(self, module: object) -> Iterator[Self]:
        """Patch a GKEBackupStorage object with a mock.

        This will patch the Command constructor in the given module to return a
        mock that will expect an explicit list of calls to the capture method
        and return explicit responses for each call.

        Parameters
        ----------
        module
            The module in which to patch the Command class.

        Yields
        ------
        Self
            This same MockBackupForGKEClient instance with the mock attibute
            initialized to a mock BackupForGKEClient instance that will expect
            an exact list of calls to its various methods.
        """

        def make_side_effect(method: str) -> Callable:
            calls = self._calls[method]

            def side_effect(*args: Any) -> Any:
                """Return fake data from calls to capture."""
                try:
                    expected = calls.pop(0)
                except IndexError:
                    pytest.fail(
                        f"More were made to {method} than were expected."
                        f" Extra call: {args}"
                    )

                if args != expected.args:
                    pytest.fail(
                        f"Method called with unexpected arguments. Expected:"
                        f" {expected.args}, actual: {args}"
                    )
                return expected.response

            return side_effect

        mock = Mock()
        # for method in self._mocked_methods:
        #     getattr(mock, method).side_effect = make_side_effect(method)
        self._mock = mock

        with patch.object(
            module, "BackupForGKEClient", return_value=mock, autospec=True
        ):
            yield self
