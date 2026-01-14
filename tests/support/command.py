"""Helpers for mocking Commands."""

from collections.abc import Iterator
from dataclasses import dataclass
from subprocess import CompletedProcess
from typing import Any, Self
from unittest.mock import Mock, patch

import pytest

__all__ = ["MockCommand"]


@dataclass
class _CaptureCall:
    """Args and response for an expected call to Command.capture."""

    args: tuple[str]
    """The expected args."""

    response: str
    """The mock response."""


class MockCommand:
    """A wrapper around a Command mock allowing capture calls to be expected.

    #. Initialize by patching the Command constructor in a module with
       patch_command_class, which yields a MockCommand instance.
    #. Expect calls to capture on the yielded MockCommand instance.
    #. Call a function that uses a Command instance in the patched module.
       At this point, if any calls to capture are made that weren't explicitly
       expected, the test will fail.
    #. Assert any other calls (like to the run method) on the .mock attribute.

    Examples
    --------
    import phalanx.kubernetes

    mock_command = MockCommand()
    with mock_command.patch_module(kubernetes) as command:

        command.expect_capture(
            args=(
                "get",
                "Deployment",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            stdout=kubectl_output("deployment-list_scaled-down.json"),

        command.expect_capture(
            args=(
                "get",
                "StatefulSet",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            stdout=kubectl_output("statefulset-list-scaled-down.json"),
        )

        # Some method that uses a command instance in the kubernetes module
        use_command()

        assert command.mock.capture.call_args_list == [
            call(
                "get",
                "Deployment",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            call(
                "get",
                "StatefulSet",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
        ]


    """

    def __init__(self) -> None:
        self._capture_calls: list[_CaptureCall] = []
        self._run_calls: list[tuple] = []
        self._mock: Mock | None = None

    def expect_capture(self, args: tuple, stdout: str) -> None:
        """Expect capture to be called with args and return response.

        This will configure the mock to expect calls to be made in the order
        that calls to this method are made.

        Parameters
        ----------
        args
            A tuple of args to expect capture to be called with.
        response
            The response to return from the mock call when called with these
            args.
        """
        self._capture_calls.append(_CaptureCall(args=args, response=stdout))

    @property
    def mock(self) -> Mock:
        """Return the wrapped Mock object if it has been initialized.

        patch_command_class must be called before accessing this property.

        Returns
        -------
        Mock
            The Mock object returned from the patched Command constructor.

        Raises
        ------
        RuntimeError
            If this is accesed before being initialized with
            patch_command_class.
        """
        if self._mock is None:
            raise RuntimeError(
                "You must call patch_object to initialize this MockCommand."
            )
        return self._mock

    def patch_command_class(self, module: object) -> Iterator[Self]:
        """Patch a Command object with a mock.

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
            This same MockCommand instance with the mock
            attibute initialized to a mock Command instance
            that will expect an exact list of calls to its
            capture method.
        """

        def side_effect(*args: Any) -> CompletedProcess:
            """Return fake data from calls to capture."""
            try:
                expected = self._capture_calls.pop(0)
            except IndexError:
                pytest.fail(
                    f"More were made to capture than were expected."
                    f" Extra call: {args}"
                )

            process = CompletedProcess(
                args=expected.args, returncode=0, stdout=expected.response
            )

            if args != expected.args:
                pytest.fail(
                    f"Command called with unexpected arguments. Expected:"
                    f" {expected.args}, actual: {args}"
                )
            return process

        mock = Mock()
        mock.capture.side_effect = side_effect
        self._mock = mock

        with patch.object(module, "Command", return_value=mock, autospec=True):
            yield self
