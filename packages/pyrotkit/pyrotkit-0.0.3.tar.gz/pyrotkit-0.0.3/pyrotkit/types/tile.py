from __future__ import annotations
from typing import Self, overload


from pyrotkit.types.coordinate import Coordinate


class Tile:
    """A generic tile.

    Has a location on a 2D grid, represented by a :py:class:`Coordinate`.

    Args:
        coord: The location of the tile, as a :py:class:`Coordinate`
    """
    def __init__(self, coord: Coordinate):
        """Initializes the instace based on coordinates."""
        self._coords = coord

    @classmethod
    def fromRawInt(cls, x: int, y: int) -> Tile:
        """Create a PathTile from raw integers.

        Args:
            x: `x` coordinate of the tile
            y: `y` coordinate of the tile
        Returns:
            A new tile"""
        return cls(Coordinate(x, y))

    @property
    def x(self) -> int:
        """The `x` coordinate of this :class:`Tile`."""
        return self._coords.x

    @property
    def y(self) -> int:
        """The `y` coordinate of this :class:`Tile`."""
        return self._coords.y

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    @property
    def coords(self) -> tuple[int, int]:
        """The `x, y` coordinates of this :class:`Tile`."""
        return self._coords.x, self._coords.y
    
    @overload
    def set_coords(self, x: int, y: int) -> None: ...
    @overload
    def set_coords(self, coords: tuple[int, int]) -> None: ...
    @overload
    def set_coords(self, coords: Coordinate) -> None: ...
    def set_coords(self, v1, v2=None):
        """Set the tile's coordinates."""
        if isinstance(v1, Coordinate):
            self._coords = v1
        elif isinstance(v1, tuple) and len(v1) == 2:
            self._coords.x, self._coords.y = v1
        elif isinstance(v1, int) and isinstance(v2, int):
            self._coords.x = v1
            self._coords.y = v2
        else:
            raise TypeError
    


