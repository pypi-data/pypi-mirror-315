from __future__ import annotations

from pyrotkit.types.coordinate import Coordinate
from pyrotkit.types.tile import Tile


class PathTile(Tile):
    """A tile with distance information for pathfinding.

    Has a location on a 2D grid, represented by a :py:class:`Coordinate`.

    Args:
        coord: The tile's location
        dist: Distance from the starting tile
    """

    def __init__(self, coord: Coordinate, dist: int = 0):
        super().__init__(coord)
        self.dist = dist

    @classmethod
    def fromRawInt(cls, x, y, dist: int = 0) -> PathTile:
        new: PathTile = super().fromRawInt(x, y)
        new.dist = dist
