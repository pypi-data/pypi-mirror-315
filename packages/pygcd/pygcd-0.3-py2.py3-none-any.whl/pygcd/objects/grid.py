from __future__ import annotations

from dataclasses import dataclass, field

from . import Object, read_grid


@dataclass
class Grid(Object):
    """Grid-geometry type object (Voxet, GSurf, SGrid)"""

    origin: tuple[float] = field(default_factory=tuple)
    dimension: tuple[float] = field(default_factory=tuple)
    spacing: tuple[float] = field(default_factory=tuple)
    data: list[float] = field(default_factory=list)

    @classmethod
    def from_chunk(cls, chunk: str, *args, **kwargs) -> Object:
        self = cls()
        params, self.data = read_grid(chunk, *args, **kwargs)
        self.origin, self.dimension, self.spacing = params
        return self

    def __repr__(self) -> str:
        s = super().__repr__() + "\n"
        s += f"\tN Points:\t{len(self.points)}\n"
        s += f"\tN Cells:\t{len(self.cells)}\n"
        s += f"\tN Arrays:\t{len(self.data)}\n"
        return s
