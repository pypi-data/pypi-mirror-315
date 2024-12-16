"""A base class for pathfinders to inherit from."""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from pyrotkit.constants import DIR8
from pyrotkit.types import Coordinate, Tile
from pyrotkit.types.pathtile import PathTile


if TYPE_CHECKING:
    import numpy.typing as npt


class PathFinder:
    """
    Args:
        target_tile: The tile this pathfinder will try to reach.
        passable_callback: Whether entities using this pathfinder can pass a tile."""
    start_tile: Coordinate

    def __init__(
        self, target_tile: Tile, passable_callback: Callable[[Tile], bool]
    ) -> None:
        self.target_tile = target_tile
        self.passable_callback = passable_callback

        self._dirs = [
            DIR8[0],
            DIR8[2],
            DIR8[4],
            DIR8[6],
            DIR8[1],
            DIR8[3],
            DIR8[5],
            DIR8[7],
        ]

    def compute(self, start_tile: Tile) -> npt.NDArray:
        raise NotImplementedError

    def get_neighbors(self, test_tile: PathTile) -> list[PathTile]:
        result: list[PathTile] = []
        for i in range(self._dirs):
            dx, dy = self._dirs[i]
            temp_tile = PathTile(Coordinate(test_tile.x + dx, test_tile.y + dy), test_tile.dist+1)
            if self.passable_callback(temp_tile):
                result.append(temp_tile)
        return result
