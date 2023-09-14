"""Utilities for managing test data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from phalanx.models.secrets import StaticSecrets

__all__ = [
    "assert_json_dirs_match",
    "output_path",
    "phalanx_test_path",
    "read_input_static_secrets",
    "read_output_data",
    "read_output_json",
]


def assert_json_dirs_match(left: Path, right: Path) -> None:
    """Assert that two directories full of JSON files match.

    Parameters
    ----------
    left
        One tree of JSON files.
    right
        Another tree of JSON files.
    """
    left_files = {p.name for p in left.iterdir()}
    right_files = {p.name for p in right.iterdir()}
    assert left_files == right_files
    for left_path in left.iterdir():
        with left_path.open() as fh:
            left_json = json.load(fh)
        with (right / left_path.name).open() as fh:
            assert left_json == json.load(fh)


def output_path() -> Path:
    """Return path to Phalanx test output.

    Returns
    -------
    Path
        Path to test output data.
    """
    return Path(__file__).parent.parent / "data" / "output"


def phalanx_test_path() -> Path:
    """Return path to Phalanx test data.

    Returns
    -------
    Path
        Path to test input data. The directory will contain test data in the
        layout of a Phalanx repository to test information gathering and
        analysis.
    """
    return Path(__file__).parent.parent / "data" / "input"


def read_input_static_secrets(environment: str) -> StaticSecrets:
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
        return StaticSecrets.parse_obj(yaml.safe_load(fh))


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
    return (output_path() / environment / filename).read_text()


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
    data = (output_path() / environment / (filename + ".json")).read_text()
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
    with (output_path() / environment / (filename + ".json")).open("w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
