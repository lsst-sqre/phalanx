"""Support tooling for Phalanx, SQuaRE's application development platform."""

__all__ = ["__version__"]

from importlib.metadata import PackageNotFoundError, version

__version__: str
"""The version string, although ``phalanx`` isn't technically released
like a typical Python package.
"""

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
