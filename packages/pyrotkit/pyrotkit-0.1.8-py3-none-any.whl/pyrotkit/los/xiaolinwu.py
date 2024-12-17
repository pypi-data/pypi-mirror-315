from __future__ import annotations
from math import trunc

from pyrotkit.types import Coordinate, Tile, WuTile


def _swap(x, y):
    return y, x


def _fpart(x):
    return x - trunc(x)


def _rfpart(x):
    return 1 - _fpart(x)


def xiaolinwu(start: Tile, stop: Tile)->list[WuTile]:
    """Caluclates a line using Xiaolin Wu's algorithm.
    
    This produces an anti-aliased line which can be used for
    line damage calculations.
    
    Args:
        start: start tile of the line
        stop: end tile of the line
    Returns:
        A list of tiles and their "brightness"
    """
    tiles = list[WuTile]
    steep = abs(stop.y - start.y) > abs(stop.x - start.x)
    x1, y1 = start.coords
    x2, y2 = stop.coords
    if steep:
        _swap(x1, y1)
        _swap(x2, y2)
    if x1 > x2:
        _swap(x1, x2)
        _swap(y1, y2)

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0.0:
        gradient = 1.0
    else:
        gradient = dy / dx

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = _rfpart(x1 + 0.5)
    xpixel1 = xend
    ypixel1 = trunc(yend)

    if steep:
        tiles.append(WuTile(Coordinate(ypixel1, xpixel1), _rfpart(yend) * xgap))
        tiles.append(
            WuTile(
                Coordinate(
                    ypixel1 + 1,
                    xpixel1,
                )
            ),
            _fpart(yend) * xgap,
        )
    else:
        tiles.append(WuTile(Coordinate(xpixel1, ypixel1), _rfpart(yend) * xgap))
        tiles.append(WuTile(Coordinate(xpixel1, ypixel1 + 1), _fpart(yend) * xgap))
    intery = yend + gradient

    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = _fpart(x2 + 0.5)
    xpixel2 = xend
    ypixel2 = trunc(yend)
    if steep:
        tiles.append(WuTile(Coordinate(ypixel2, xpixel2), _rfpart(yend) * xgap))
        tiles.append(WuTile(Coordinate(ypixel2 + 1, xpixel2), _fpart(yend) * xgap))
    else:
        tiles.append(WuTile(Coordinate(xpixel2, ypixel2), _rfpart(yend) * xgap))
        tiles.append(WuTile(Coordinate(xpixel2, ypixel2 + 1), _fpart(yend) * xgap))

    if steep:
        for x in range(xpixel1 + 1, xpixel2):
            tiles.append(WuTile(Coordinate(trunc(intery), x), _rfpart(intery)))
            tiles.append(WuTile(Coordinate(trunc(intery) + 1, x), _fpart(intery)))
            intery += gradient
    else:
        for x in range(xpixel1 + 1, xpixel2):
            tiles.append(WuTile(Coordinate(x, trunc(intery)), _rfpart(intery)))
            tiles.append(WuTile(Coordinate(x, trunc(intery) + 1), _fpart(intery)))
            intery += gradient
    return tiles
