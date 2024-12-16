from __future__ import annotations
from typing import overload

from pyrotkit.types import Coordinate, Tile


class Camera:
    """
    Translates world coordinates to facilitate maps larger than the screen.

    Args:
        map: Dimensions of the map
        screen: Dimensions of the screen
        center: Focused tile
        lock_view: Whether the camera is kept inside the world
    """

    def __init__(
        self,
        *,
        map: tuple[int, int],
        screen: tuple[int, int],
        center: Tile = None,
        lock_view: bool = True,
    ):
        self._map = map
        self._screen = screen
        self.lock_view = lock_view
        if center is not None:
            self._center = center
        else:
            self._center = Tile(Coordinate(0, 0))

    @property
    def x_min(self) -> int:
        """x coordinate of the top-left tile"""
        target = self._center[0] - self._screen[0] // 2
        if self.lock_view is True:
            return max(0, min(target, self._map[0] - self._screen[0]))
        else:
            return target

    @property
    def y_min(self) -> int:
        """y coordinate of the top-left tile"""
        target = self._center[1] - self._screen[1] // 2
        if self.lock_view is True:
            return max(0, min(target, self._map[1] - self._screen[1]))
        else:
            return target

    @property
    def x_max(self) -> int:
        """x coordinate of the bottom right tile"""
        return self.x_min + self._screen[0]

    @property
    def y_max(self) -> int:
        """y coordinate of the bottom right tile"""
        return self.y_min + self._screen[1]

    @property
    def origin(self) -> Tile:
        """Get the top-left tile of the camera."""
        return Tile(Coordinate(self.x_min, self.y_min))

    @property
    def view_slice(self) -> tuple[slice, slice]:
        """Get a slice that can be used on an NDArray."""
        return slice(self.x_min, self.x_max), slice(self.y_min, self.y_max)

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
