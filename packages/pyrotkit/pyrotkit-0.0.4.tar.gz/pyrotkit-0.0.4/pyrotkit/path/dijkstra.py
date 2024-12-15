"""An implementation of Dijkstra's Algorithm."""

from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING


from pyrotkit.path.pathfinder import PathFinder
from pyrotkit.types.pathtile import PathTile

if TYPE_CHECKING:
    from pyrotkit.types import Tile


class DijkstraPath(PathFinder):
    """
    Calculates a path using Dijkstra's algorithm.
    
    Args:
        target_tile: The tile this pathfinder will try to reach.
        passable_callback: Whether entities using this pathfinder can pass a tile."""

    def __init__(self, target_tile: Tile, passable_callback: Callable[[Tile], bool]):
        super().__init__(target_tile=target_tile, passable_callback=passable_callback)

        self._todo: list[PathTile] = []

    def compute(self, start: Tile) -> list[Tile] | None:
        """Computes the path from the given tile to the set destination.
        
        Args:
            start: The tile to start from
            
        Returns:
            Either a list of tiles to get to the target, or None"""
        self._todo.append(start)

        while len(self._todo):
            self._todo.sort(reverse=True, key=lambda item: item.dist)
            current_tile = self._todo.pop()
            if current_tile == self.target_tile:
                break

            for tile in self.get_neighbors(current_tile):
                try:
                    i = self._todo.index(tile)
                    if tile.dist < self._todo[i].dist:
                        self._todo[i] = tile
                except ValueError:
                    self._todo.append(tile)
