from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from ..constants import DIRS
from .mapgen import MapGenerator
from ..types import Coordinate, RectangularRoom, Tile
from pyrotkit.tools import tunnel_between

if TYPE_CHECKING:
    import numpy.typing as npt

class RoomGenerator(MapGenerator):
    """
    Generates maps made of rectangular rooms connected by corridors.
    
    Args:
        max_rooms: The maximum number of rooms in the map
        room_min_size: The minimum size when determining a room's dimensions
        room_max_size: The maximum size when determining a room's dimensions
    """
    def __init__(
        self,
        width,
        height,
        wall,
        floor,
        dirs=DIRS.DIR8,
        rng=None,
        dtype: npt.DTypeLike = None,
        max_rooms: int = 30,
        room_min_size: int = 6,
        room_max_size: int = 10,
    ):
        super().__init__(
            width=width,
            height=height,
            wall=wall,
            floor=floor,
            dirs=dirs,
            rng=rng,
            dtype=dtype,
        )
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

    def tunnel_between(self, start: tuple[int, int], stop: tuple[int, int]):
        """Digs a tunnel between two tiles.

        Randomly decides whether to travel horizontally or vertically first.

        Args:
            start: Starting tile
            stop: Finishing tile
        Yields:
            x, y: Coordinates of tiles in the tunnel"""
        tunnel_between(start, stop, self.rng)

    def generate_map(self) -> tuple[npt.NDArray, Tile, Tile]:
        """
        Generates and returns a map made of rectangular rooms.
        
        Returns:
            The map
            The entrance tile
            The exit tile"""
        new_map = np.full(
            (self.width, self.height), fill_value=self.wall, dtype=self._dtype
        )

        center_of_last_room = (0,0)
        rooms: list[RectangularRoom] = []
        
        for _ in range(self.max_rooms):
            room_width = self.rng.randint(self.room_min_size, self.room_max_size)
            room_height = self.rng.randint(self.room_min_size, self.room_max_size)
            
            x = self.rng.randint(0, self.width - room_width - 1)
            y = self.rng.randint(0, self.height - room_height - 1)
            
            new_room = RectangularRoom(x, y, room_width, room_height)
            
            if any(new_room.intersects(other_room) for other_room in rooms):
                continue
            
            new_map[new_room.inner] = self.floor

            if len(rooms) == 0:
                entrance = Tile(Coordinate(*new_room.center))
            else:
                for x,y in self.tunnel_between(rooms[-1].center, new_room.center):
                    new_map[x, y] = self.floor
                
                center_of_last_room = new_room.center

            exit = Tile(Coordinate(*center_of_last_room))
            
            return new_map, entrance, exit
            