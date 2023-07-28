"""Utilities for managing test data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

__all__ = [
    "phalanx_test_path",
    "read_output_data",
]


def phalanx_test_path() -> Path:
    """Return path to Phalanx test data.

    Returns
    -------
    Path
        Path to test input data.  The directory will contain test data in the
        layout of a Phalanx repository to test information gathering and
        analysis.
    """
    return Path(__file__).parent.parent / "data" / "input"


def read_output_data(environment: str, filename: str) -> str:
    """Read test output data and return it.

    Parameters
    ----------
    environment
        Name of the environment under :filename:`data/output` that the test
        output is for.
    filename
        File containing the output data.

    Returns
    -------
    str
        Contents of the file.
    """
    base_path = Path(__file__).parent.parent / "data" / "output"
    return (base_path / environment / filename).read_text()


def read_output_yaml(environment: str, filename: str) -> dict[str, Any]:
    """Read test output data as YAML and return the parsed format.

    Parameters
    ----------
    environment
        Name of the environment under :filename:`data/output` that the test
        output is for.
    filename
        File containing the output data.

    Returns
    -------
    dict
        Parsed version of the YAML.
    """
    base_path = Path(__file__).parent.parent / "data" / "output"
    with (base_path / environment / filename).open() as fh:
        return yaml.safe_load(fh)
