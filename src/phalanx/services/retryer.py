"""Retry something a bunch and wait in between."""

import time
from collections.abc import Generator
from datetime import timedelta

from phalanx.exceptions import RetryerTimeoutError

__all__ = ["retryer"]


def retryer(
    condition: str,
    attempts: int,
    interval: timedelta,
    *,
    verbose: bool = False,
) -> Generator[int]:
    """Retry something a bunch and wait in between.

    Parameters
    ----------
    condition
        A description of the condition to wait for.
    attempts
        The number of times to try.
    interval
        The amount of time to wait in between attempts.

    Returns
    -------
    Generator[int]
        The current attempt.
    """
    seconds = int(interval.total_seconds())
    print(
        f'Waiting for condition: "{condition}", {attempts} times with'
        f" {seconds} seconds in between."
    )
    for attempt in range(attempts):
        yield attempt
        if verbose:
            print(
                f"{condition} not satisfied in attempt {attempt + 1} of"
                f" {attempts}. Trying again in {seconds} seconds."
            )
        time.sleep(interval.total_seconds())

    print(
        f'Condition: "{condition}" not satisfied in {attempts} with {seconds}'
        f" seconds in between."
    )
    raise RetryerTimeoutError(
        condition=condition, attempts=attempts, interval=interval
    )
