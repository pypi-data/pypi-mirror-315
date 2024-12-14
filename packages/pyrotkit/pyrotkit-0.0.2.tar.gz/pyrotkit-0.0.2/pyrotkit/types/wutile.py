from __future__ import annotations

from pyrotkit.types import Coordinate, Tile

class WuTile(Tile):
    def __init__(self, coord: Coordinate, brightness: float):
        super().__init__(coord)
        self.brightness = brightness