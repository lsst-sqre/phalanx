"""Models for Gafaelfawr data structures.

Ideally, these should use the same models Gafaelfawr itself uses. Until that's
possible via a PyPI library, these models are largely copied from Gafaelfawr.
"""

from __future__ import annotations

import base64
import os

from pydantic import BaseModel, Field

__all__ = ["Token"]


def _random_128_bits() -> str:
    """Generate random 128 bits encoded in base64 without padding."""
    return base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")


class Token(BaseModel):
    """An opaque token.

    Notes
    -----
    A token consists of two parts, a semi-public key that is used as the Redis
    key, and a secret that is only present in the token returned to the user
    and the encrypted session in Redis.

    The serialized form of a token always starts with ``gt-``, short for
    Gafaelfawr token, to make it easier to identify these tokens in logs.

    The serialized form encodes the secret in URL-safe base64 with the padding
    stripped off (because equal signs can be parsed oddly in cookies).
    """

    key: str = Field(default_factory=_random_128_bits)
    secret: str = Field(default_factory=_random_128_bits)

    @classmethod
    def is_token(cls, token: str) -> bool:
        """Determine if a string is a Gafaelfawr token.

        Parameters
        ----------
        token
            The string to check.

        Returns
        -------
        bool
            Whether that string looks like a Gafaelfawr token.  The token
            isn't checked for validity, only format.
        """
        if not token.startswith("gt-"):
            return False
        trimmed_token = token[len("gt-") :]
        if "." not in trimmed_token:
            return False
        key, secret = trimmed_token.split(".", 1)
        return len(key) == 22 and len(secret) == 22

    def __str__(self) -> str:
        """Return the encoded token."""
        return f"gt-{self.key}.{self.secret}"
