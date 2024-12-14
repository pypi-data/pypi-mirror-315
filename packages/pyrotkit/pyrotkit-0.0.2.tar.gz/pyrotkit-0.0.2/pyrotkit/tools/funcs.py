from __future__ import annotations
import random
from typing import TYPE_CHECKING, Iterator

import numpy as np


from pyrotkit import los
from pyrotkit.types.coordinate import Coordinate
from pyrotkit.types.tile import Tile

if TYPE_CHECKING:
     import numpy.typing as npt

def tunnel_between(
        start: Tile, stop: Tile, rng: random.Random
    ) -> Iterator[Tile]:
        """Plots a tunnel between two rooms.
        
        Args:
            start: The starting tile
            stop: The finish tile
            rng: The random generator to use when deciding how to tunnel
        Yields:
            tile: tiles in the tunnel
        """
    
        if rng.random() < 0.5:
            corner = Tile(Coordinate(stop.x, start.y))
        else:
            corner = Tile(Coordinate(start.x, stop.y))

        for tile in los.bresenham(start, corner).tolist():
            yield tile
        for tile in los.bresenham(corner, stop).tolist():
            yield tile
            
def check_percent_walls(map_to_check: npt.NDArray, wall) -> float:
    """Calculates and returns the percent of the map which is walls.
    
    Args:
        map_to_check: Map to check for coverage
        wall: What should be considered a wall
    Returns:
        Percent of the map covered in walls
    """
    width, height = map_to_check.shape
    total_tiles = width * height
    walls = 0.0
    for x, y in np.ndindex(map_to_check.shape):
        if map_to_check[x, y] == wall:
            walls += 1
    return walls/float(total_tiles)