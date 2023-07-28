"""Utility functions for manipulating YAML.

In several places in the Phalanx code, we want to be able to wrap long strings
to make them more readable or be able to dump `collections.defaultdict`
objects without adding special object tagging. This module collects utility
functions to make this easier.
"""

from __future__ import annotations

from collections import defaultdict

import yaml
from yaml.representer import Representer

__all__ = ["YAMLFoldedString"]


class YAMLFoldedString(str):
    """A string that will be folded when encoded in YAML."""

    __slots__ = ()


def _folded_string_representer(
    dumper: yaml.Dumper, data: YAMLFoldedString
) -> yaml.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=">")


yaml.add_representer(YAMLFoldedString, _folded_string_representer)
yaml.add_representer(defaultdict, Representer.represent_dict)
