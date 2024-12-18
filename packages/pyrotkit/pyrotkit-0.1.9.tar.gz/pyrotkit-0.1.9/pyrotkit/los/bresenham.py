from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from pyrotkit.types import Tile

if TYPE_CHECKING:
    from numpy.typing import NDArray


def _bresenham_low(start: tuple[int, int], stop: tuple[int, int]) -> NDArray[np.intc]:
    x1, y1 = start
    x2, y2 = stop
    dx = x2 - x1
    dy = y2 - y1
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    d = (2 * dy) - dx
    y = y1
    result = []
    for x in range(x1, x2+1):
        result.append((x, y))
        if d > 0:
            y = y + yi
            d = d + (2 * (dy - dx))
        else:
            d = d + 2 * dy
    return np.array(result)


def _bresenham_high(start: tuple[int, int], stop: tuple[int, int]) -> NDArray[np.intc]:
    x1, y1 = start
    x2, y2 = stop
    dx = x2-x1
    dy = y2-y1
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    d = (2*dx)-dy
    x=x1
    result = []
    for y in range(y1, y2+1):
        result.append(x, y)
        if d>0:
            x = x + xi
            d = d+(2*(dx-dy))
        else:
            d = d+2*dx
    return np.array(result)


def bresenham(start: Tile, stop: Tile) -> NDArray[np.intc]:
    """Uses Bresenham's algorithm to determin line of sight.

    Note that this isn't a field of view algorithm; it **does not
    check** that any tile in the line in visible. It would be more
    accurate to say it is simply a line algorithm, but in the context
    of roguelikes, line of sight seems to be the accepted nomenclature.
    
    Args:
        start: the Tile to start from
        stop: the Tile to look at
    Returns:
        A numpy array of tiles in the line"""
    x0, y0 = start.x, start.y
    x1, y1 = stop.x, stop.y
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            return _bresenham_low((x1, y1), (x0, y0))
        else:
            return _bresenham_low((x0, y0), (x1, y1))
    else:
        if y0 > y1:
            return _bresenham_high((x1, y1), (x0, y0))
        else:
            return _bresenham_high((x0, y0), (x1, y1))
    pass
