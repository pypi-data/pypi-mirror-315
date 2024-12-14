from __future__ import annotations
from typing import overload

from pyrotkit.types import Coordinate, Tile

class Camera:
    """
    Translates world coordinates to facilitate maps larger than the screen.

    Recalculates properties when setting the center of the camera's view.

    Args:
        lock_view: Whether the camera is kept inside the world
    """

    def __init__(self, *, lock_view: bool = True):
        self.lock_view = lock_view
        pass

    @property
    def screen_origin(self) -> Tile:
        """Get the top-left tile of the camera."""
        pass

    @property
    def view_slice(self) -> slice:
        """Get a slice that can be used on an NDArray."""
        pass


    @overload
    def set_center(self, x: int, y: int) -> None: ...
    @overload
    def set_center(self, center: Tile) -> None: ...
    def set_center(self, x, y) -> None:
        """
        Set the center of the camera.

        Raises:
            AttributeError: If the arguments are the wrong type
        """
        if isinstance(x, Tile):
            self.center = x
        elif isinstance(x, int) and isinstance(y, int):
            self.center = Tile(Coordinate(x, y))
        else:
            raise AttributeError