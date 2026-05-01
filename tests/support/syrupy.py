"""Helpers for syrupy snapshot assertions."""

from collections.abc import Iterable

from syrupy.extensions.amber.pydantic_plugin import PydanticPlugin
from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
)
from syrupy.extensions.single_file import SingleFileAmberSnapshotExtension

__all__ = ["SinglefilePydanticExtension"]


class _PydanticSerializer(AmberDataSerializer):
    """A syrupy serializer that can serialize Pydantic models."""

    serializer_plugins: Iterable[type["AmberDataSerializerPlugin"]] | None = [
        PydanticPlugin
    ]


class SinglefilePydanticExtension(SingleFileAmberSnapshotExtension):
    """An extension that serializes to single files and can handle Pydantic."""

    serializer_class = _PydanticSerializer
