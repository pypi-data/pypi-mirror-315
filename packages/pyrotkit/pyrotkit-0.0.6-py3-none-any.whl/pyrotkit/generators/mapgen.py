from __future__ import annotations
import random
from typing import TYPE_CHECKING

import numpy as np

from pyrotkit.constants import DIR4, DIR8, DIRS, NEIGHBORHOOD
from pyrotkit.types.tile import Tile

if TYPE_CHECKING:
    import numpy.typing as npt


class MapGenerator:
    """Base class for all other map generators to inherit from.
    
    Args:
        width: Width of the map
        height: Height of the map
        wall: What to set for wall tiles
        floor: What to set for floor tiles
        dirs: How many directions of movement entity's have
        rng: Random generator to use when making decisions
        dtype: Arrays will be generated with this dtype set, if provided
    """
    
    def __init__(
        self,
        width: int,
        height: int,
        wall: npt.DTypeLike,
        floor: npt.DTypeLike,
        dirs: DIRS = DIRS.DIR8,
        rng: random.Random = None,
        dtype: npt.DTypeLike = None,
    ) -> None:
        self.width = width
        self.height = height
        self.wall = wall
        self.floor = floor
        self.rng = rng
        self._dirs_type = dirs
        self._dtype = dtype
        if dirs == DIRS.DIR4:
            self._dirs = DIR4
        elif dirs == DIRS.DIR8:
            self._dirs = DIR8

    @property
    def dimensions(self) -> tuple[int, int]:
        """The dimensions of the map"""
        return self.width, self.height

    @dimensions.setter
    def dimensions(self, value: tuple[int, int]) -> None:
        self.width, self.height = value

    def fill(self, value) -> npt.NDArray:
        """Makes and returns a new map full of the given value.
        
        Args:
            value: The value to fill the new map with.
        Returns:
            The new map"""
        return np.full(shape=(self.dimensions), fill_value=value, order="F", dtype=self._dtype)

    def generate_map(self) -> npt.NDArray:
        """Generate a map using the derived generator.
        
        Subclasses **must** override this function.
        
        Raises:
            NotImplementedError: Someone either misused this class or forgot to override this function."""
        raise NotImplementedError

    def get_neighbors(
        self,
        tile_map: npt.NDArray,
        tile: Tile,
        directions: list[tuple[int, int]],
    ) -> int:
        """Returns the number of walls which neighbor a given tile.

        By default, this counts neighbors in all 8 tiles which touch the specificed tile. Custom
        direcitons can be supplied to support maps of other shapes.

        Args:
            tile_map: The map in which the tile lives
            tile: The `Tile` whose neighbors to count
            directions: The relative coordinates of all the tiles to check
        Returns:
            The number of neighboring walls
        """
        neighbors = 0 if tile_map[tile.coords] == self.floor else 1
        max_x, max_y = tile_map.shape
        for dx, dy in directions:
            cx = tile.x + dx
            cy = tile.y + dy
            if cx in range(max_x) and cy in range(max_y):
                if tile_map[cx, cy] == self.wall:
                    neighbors += 1
            else:
                neighbors += 1
        return neighbors

    def get_neighborhood(
        self,
        tile_map: npt.NDArray,
        tile: Tile,
    ) -> int:
        """Returns the number of wall tiles in a given tile's neighborhood.
        
        A neighborhood is defined as the tiles within two movements of the specified tile. For
        a rectangular grid map with movement in 8 directions, this is the 5x5 grid centered on
        the specified tile.
        
        Args:
            tile_map: The map in which the tile lives
            coordinates: The coordinates of the tile
        Returns:
            The number of walls in the neighborhood
        """
        neighbors = 0 if tile_map[tile.coords] == self.floor else 1
        max_x, max_y = tile_map.shape
        for dx, dy in NEIGHBORHOOD:
            cx = tile.x + dx
            cy = tile.y + dy
            if cx in range(max_x) and cy in range(max_y):
                if tile_map[cx, cy] == self.wall:
                    neighbors += 1
            else:
                neighbors += 1
        return neighbors
