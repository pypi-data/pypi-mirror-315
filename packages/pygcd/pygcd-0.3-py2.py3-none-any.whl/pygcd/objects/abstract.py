from __future__ import annotations

from abc import abstractclassmethod
from dataclasses import dataclass, field
from enum import Enum
from logging import warning
from typing import Any

from . import read_header


class Geometry(Enum):
    """GOCAD object geometry type."""

    Invalid = -1
    # 0 <= mesh data < 10
    VSet = 0
    PLine = 1
    TSurf = 2
    TSolid = 3
    # well data == 10
    Well = 10
    # grid data > 10
    Voxet = 11
    GSurf = 12
    SGrid = 13

    @classmethod
    def names(cls):
        return [el.name for el in cls]

    @property
    def instance(self):
        from . import Grid, Mesh, Well

        if self.value > 10:
            return Grid
        elif self.value == 10:
            return Well
        elif self.value >= 0:
            return Mesh
        else:
            raise ValueError(f"{self.name} geometry !")

    def read(self, text, *args, **kwargs):
        return self.instance.from_chunk(text, *args, **kwargs)


@dataclass
class Layer:
    """Generic GOCAD object (abstract class)"""

    name: str = "Unknown object"
    geometry: Geometry = Geometry(-1)
    version: str = "?"
    fields: dict = field(default_factory=dict)

    def __post_init__(self):
        """Make it abstract, any Layer() will fail"""
        if self.__class__ == Layer:
            raise TypeError("Cannot instantiate abstract class.")

    def __getattr__(self, name: str) -> Any:
        """Make self.fields accessible as class attributes.

        Any failed `self.name` attempt will trigger a lookup in
        self.fields.keys() and return self.fields[name] if match.

        Args:
            name (str): Field name.

        Raises:
            AttributeError: Non existing keys will raise AttributeError.

        Returns:
            Any: Identical to `self.fields[name]`.
        """
        if name in self.__getattribute__("fields"):
            return self.fields[name]
        else:
            raise AttributeError(f"'{self.__class__}' object has no attribute '{name}'")

    def __repr__(self) -> str:
        """Textual representation of an object.

        self.geometry.name ("self.name")
            N Fields:   len(self.fields)
            -> child classes will add informations

        Returns:
            str: Object string representation.
        """
        s = f'{self.geometry.name} ("{self.name}")\n'
        s += f"\tN Fields:\t{len(self.fields)}"
        return s


class Object(Layer):
    """Geometric object (abstract class)"""

    def __post_init__(self):
        """make it abstract"""
        if self.__class__ == Object:
            raise TypeError("Cannot instantiate abstract class.")

    @abstractclassmethod
    def from_chunk(cls, chunk: str, *args, **kwargs) -> Object:
        return cls()

    def to(self, wrapper: str):
        from ..drivers import Drivers

        if wrapper.lower() not in Drivers:
            raise ValueError(f"Unsupported format: {wrapper}")
        else:
            driver = Drivers[wrapper.lower()]
        return driver(self)


class Chunk(Layer):
    """Identified object (i.e. decoded header)"""

    def __init__(self, raw: str):
        self.load(raw)

    def load(self, chunk: str):
        header = read_header(chunk)
        self.name = header.pop("name", self.name)
        self.geometry = Geometry[header.pop("geometry", self.geometry.name)]
        self.version = header.pop("version", self.version)
        self.fields = header
        self.chunk = chunk

    def read(self, *args, **kwargs) -> Object:
        new = self.geometry.read(self.chunk, *args, **kwargs)
        for attr in self.__dataclass_fields__.keys():
            if hasattr(new, attr):
                new.__setattr__(attr, self.__getattribute__(attr))
        return new

    @staticmethod
    def decode(chunk: str, *args, **kwargs) -> Chunk:
        return Chunk(chunk).read(*args, **kwargs)


def decode(chunk, *args, **kwargs):
    if isinstance(chunk, str):
        return Chunk.decode(str, *args, **kwargs)
    if isinstance(chunk, Chunk):
        return chunk.read(*args, **kwargs)
    if isinstance(chunk, Object):
        return chunk
    warning(f"Ignoring unsupported GOCAD object: {chunk})")
    return None
