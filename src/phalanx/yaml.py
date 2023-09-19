"""Utility functions for manipulating YAML.

In several places in the Phalanx code, we want to be able to wrap long strings
to make them more readable or be able to dump `collections.defaultdict`
objects without adding special object tagging. This module collects utility
functions to make this easier.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import yaml
from pydantic import GetCoreSchemaHandler, SecretStr
from pydantic_core import CoreSchema, core_schema
from yaml.representer import Representer

__all__ = ["YAMLFoldedString"]


class YAMLFoldedString(str):
    """A string that will be folded when encoded in YAML."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


def _folded_string_representer(
    dumper: yaml.Dumper, data: YAMLFoldedString
) -> yaml.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=">")


def _secret_str_representer(dumper: yaml.Dumper, data: SecretStr) -> yaml.Node:
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str", data.get_secret_value()
    )


yaml.add_representer(SecretStr, _secret_str_representer)
yaml.add_representer(YAMLFoldedString, _folded_string_representer)
yaml.add_representer(defaultdict, Representer.represent_dict)
