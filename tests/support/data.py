"""Utilities for managing test data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

__all__ = [
    "phalanx_test_path",
    "read_input_static_secrets",
    "read_output_data",
    "read_output_json",
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


def read_input_static_secrets(environment: str) -> dict[str, dict[str, str]]:
    """Read test output data as YAML and return the parsed format.

    Parameters
    ----------
    environment
        Name of the environment for which to read static secrets.

    Returns
    -------
    dict of dict
        Parsed version of the YAML.
    """
    secrets_path = phalanx_test_path() / "secrets" / f"{environment}.yaml"
    with secrets_path.open() as fh:
        data = yaml.safe_load(fh)
    for secrets in data.values():
        for key in secrets:
            secrets[key] = secrets[key]["value"]
    return data


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


def read_output_json(environment: str, filename: str) -> Any:
    """Read test output data in JSON and return it.

    Parameters
    ----------
    environment
        Name of the environment under :filename:`data/output` that the test
        output is for.
    filename
        File containing the output data. ``.json`` will be appended.

    Returns
    -------
    Any
        Contents of the file.
    """
    base_path = Path(__file__).parent.parent / "data" / "output"
    data = (base_path / environment / (filename + ".json")).read_text()
    return json.loads(data)


def write_output_json(environment: str, filename: str, data: Any) -> None:
    """Store output data as JSON.

    This function is not called directly by the test suite. It is provided as
    a convenience to write the existing output as test data so that a human
    can review it without having to write it manually.

    Parameters
    ----------
    config
        Configuration to which to write data (the name of one of the
        directories under ``tests/configs``).
    filename
        File to write.
    data
        Data to write.
    """
    base_path = Path(__file__).parent.parent / "data" / "output"
    with (base_path / environment / (filename + ".json")).open("w") as f:
        json.dump(data, f, indent=2)
