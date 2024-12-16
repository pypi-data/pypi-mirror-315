from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from pyrotkit.constants import DIRS
from pyrotkit.generators.mapgen import MapGenerator
from pyrotkit.tools import check_percent_walls


if TYPE_CHECKING:
    import numpy.typing as npt
    import random


class CellularGenerator(MapGenerator):
    """
    Uses an algorithm based on Conway's Game of Life to procedurally generate maps.
    
    Args:
        width: The width of the maps to generate
        height: The height of the maps to generate
        wall: The value inserted into the array when a tile is a wall
        floor: The value inserted into the array when a tile is a floor
        prob: The probability that any given tile will be a wall when randomizing the map
    """

    #: The number of iterations for the first algorithm, which seeds new walls
    rule1_iters: int
    #: The number of iterations fo the second algorithm, which does not seed walls
    rule2_iters: int

    def __init__(
        self,
        width: int,
        height: int,
        wall,
        floor,
        dirs: DIRS,
        rng: random.Random,
        dtype: npt.DTypeLike,
        prob: float,
    ) -> None:
        super().__init__(
            width=width, height=height, wall=wall, floor=floor, rng=rng, dtype=dtype
        )
        self.prob = prob
        self.rule1_iters = 4
        self.rule2_iters = 3

    def process_map(self, working_map: npt.NDArray) -> None:
        """Processes a randomized map.

        This does four iterations of an algorithm which includes seeding walls on
        tiles that have fewer than 3 walls in their neighborhood, followed by 3 iterations
        that process the map, but don't seed new tiles.

        Args:
            working_map: The map to process
        """
        for _ in range(self.rule1_iters):
            temp_map = np.full(self.dimensions, fill_value=self.floor)
            for ix, iy in np.ndindex(working_map):
                if self.get_neighbors(working_map, (ix, iy), self._dirs) >= 5:
                    temp_map[ix, iy] = self.wall
                elif self.get_neighborhood(working_map, (ix, iy)) <= 2:
                    temp_map[ix, iy] = self.wall
            working_map = temp_map
        for _ in range(self.rule2_iters):
            temp_map = np.full(self.dimensions, fill_value=self.floor)
            for ix, iy in np.ndindex(working_map):
                if self.get_neighbors(working_map, (ix, iy), self._dirs) >= 5:
                    temp_map[ix, iy] = self.wall
            working_map = temp_map

    def generate_map(self) -> npt.NDArray:
        """Generates a new map.

        Handles seeding and processing the map automatically.
        
        Returns:
            The new map"""
        while True:
            new_map = self.fill(self.floor)
            for ix, iy in np.ndindex(new_map.shape):
                new_map[ix, iy] = (
                    self.wall if self.rng.random() < self.prob else self.floor
                )
            self.process_map(new_map)
            if check_percent_walls(new_map, self.wall) <= 0.4:
                return new_map
