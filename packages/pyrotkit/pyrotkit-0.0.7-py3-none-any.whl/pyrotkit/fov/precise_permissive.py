from __future__ import annotations
import copy
from typing import Callable, Self

from pyrotkit.types import Coordinate, Tile

"""
    Author:         Aaron MacDonald
    Date:           June 14, 2007

    Description:    An implementation of the precise permissive field
                    of view algorithm for use in tile-based games.
                    Based on the algorithm presented at
                    http://roguebasin.roguelikedevelopment.org/
                      index.php?title=
                      Precise_Permissive_Field_of_View.

    You are free to use or modify this code as long as this notice is
    included.
    This code is released without warranty.

    Modified 2024:
        Added typing
        Turned the function into a class that remembers the basics
"""


class PrecisePermissiveView:
    """Executes the precise permissive view algorithm from roguebasin.com.

    Args:
        map: dimensions of the map
        passes_light: function that returns whether the tile is see through"""

    def __init__(
        self, map: tuple[int, int], passes_light: Callable[[Tile], bool]
    ):
        self.map = map
        self.passes_light = passes_light

    def get_view(
        self,
        center: Tile,
        radius: int,
        visible_callback: Callable[[Tile], None],
    ) -> None:
        """
        Executes the algorithm cenetered on the supplied tile.

        Args:
            center: Center of the field
            radius: Distance of vision
            visible_callback: function called for each visible tile
        """
        visited = set()

        visible_callback(center)
        visited.add(center)

        start_x, start_y = center.coords
        map_width, map_height = self.map

        if start_x < radius:
            min_extent_x = start_x
        else:
            min_extent_x = radius

        if map_width - start_x - 1 < radius:
            max_extent_x = map_width - start_x - 1
        else:
            max_extent_x = radius

        if start_y < radius:
            min_extent_y = start_y
        else:
            min_extent_y = radius

        if map_height - start_y - 1 < radius:
            max_extent_y = map_height - start_y - 1
        else:
            max_extent_y = radius

        _check_quadrant(
            visited,
            start_x,
            start_y,
            1,
            1,
            max_extent_x,
            max_extent_y,
            visible_callback,
            self.passes_light,
        )
        _check_quadrant(
            visited,
            start_x,
            start_y,
            1,
            -1,
            max_extent_x,
            min_extent_y,
            visible_callback,
            self.passes_light,
        )
        _check_quadrant(
            visited,
            start_x,
            start_y,
            -1,
            -1,
            min_extent_x,
            min_extent_y,
            visible_callback,
            self.passes_light,
        )
        _check_quadrant(
            visited,
            start_x,
            start_y,
            -1,
            1,
            min_extent_x,
            max_extent_y,
            visible_callback,
            self.passes_light,
        )


class _Line:
    def __init__(self, xi: int, yi: int, xf: int, yf: int):
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf

    @property
    def dx(self) -> int:
        return self.xf - self.xi

    @property
    def dy(self) -> int:
        return self.yf - self.yi

    def p_below(self, x: int, y: int) -> bool:
        return self.relative_slope(x, y) > 0

    def p_below_or_colinear(self, x: int, y: int) -> bool:
        return self.relative_slope(x, y) >= 0

    def p_above(self, x: int, y: int) -> bool:
        return self.relative_slope(x, y) < 0

    def p_above_or_colinear(self, x: int, y: int) -> bool:
        return self.relative_slope(x, y) <= 0

    def p_colinear(self, x: int, y: int) -> bool:
        return self.relative_slope(x, y) == 0

    def line_colinear(self, line: Self) -> bool:
        return self.p_colinear(line.xi, line.yi) and self.p_colinear(line.xf, line.yf)

    def relative_slope(self, x: int, y: int) -> int:
        return (self.dy * (self.xf - x)) - (self.dx * (self.yf - y))


class _ViewBump:
    def __init__(self, x: int, y: int, parent):
        self.x = x
        self.y = y
        self.parent = parent


class _View:
    def __init__(self, shallow_line: _Line, steep_line: _Line):
        self.shallow_line = shallow_line
        self.steep_line = steep_line

        self.shallow_bump: _ViewBump = None
        self.steep_bump: _ViewBump = None


def _check_quadrant(
    visited: set[tuple[int, int]],
    start_x: int,
    start_y: int,
    dx: int,
    dy: int,
    extent_x: int,
    extent_y: int,
    visible_callback: Callable[[Tile], None],
    passes_light: Callable[[Tile], bool],
) -> None:
    active_views = []
    shallow_line = _Line(0, 1, extent_x, 0)
    steep_line = _Line(1, 0, 0, extent_y)

    active_views.append(_View(shallow_line, steep_line))
    view_index = 0

    max_i = extent_x + extent_y
    i = 1
    while i != max_i + 1 and len(active_views) > 0:
        if 0 > i - extent_x:
            start_j = 0
        else:
            start_j = i - extent_x

        if i < extent_y:
            max_j = i
        else:
            max_j = extent_y

        j = start_j

        while j != max_j + 1 and view_index < len(active_views):
            x = i - j
            y = j
            _visit_coord(
                visited,
                start_x,
                start_y,
                x,
                y,
                dx,
                dy,
                view_index,
                active_views,
                visible_callback,
                passes_light,
            )
            j += 1
        i += 1


def _visit_coord(
    visited: set[tuple[int, int]],
    start_x: int,
    start_y: int,
    x: int,
    y: int,
    dx: int,
    dy: int,
    view_index: int,
    active_views: list[_View],
    visible_callback: Callable[[Tile], None],
    passes_light: Callable[[Tile], bool],
) -> None:
    top_left = (x, y + 1)
    bottom_right = (x + 1, y)
    while view_index < len(active_views) and active_views[
        view_index
    ].steep_line.p_below_or_colinear(bottom_right[0], bottom_right[1]):
        view_index += 1

    if view_index == len(active_views) or active_views[
        view_index
    ].shallow_line.p_above_or_colinear(top_left[0], top_left[1]):
        return

    is_blocked = False
    real_x = x * dx
    real_y = y * dy
    working_x = start_x + real_x
    working_y = start_y + real_y
    if (working_x, working_y) not in visited:
        visited.add((working_x, working_y))
        visible_callback(Tile(Coordinate((working_x, working_y))))

    is_blocked = passes_light(Tile(Coordinate((working_x, working_y))))

    if not is_blocked:
        return

    if active_views[view_index].shallow_line.p_above(
        bottom_right[0], bottom_right[1]
    ) and active_views[view_index].steep_line.p_below(top_left[0], top_left[1]):
        del active_views[view_index]
    elif active_views[view_index].shallow_line.p_above(
        bottom_right[0], bottom_right[1]
    ):
        _add_shallow_bump(top_left[0], top_left[1], active_views, view_index)
        _check_view(active_views, view_index)
    elif active_views[view_index].steep_line.p_below(top_left[0], top_left[1]):
        _add_steep_bump(bottom_right[0], bottom_right[1], active_views, view_index)
        _check_view(active_views, view_index)
    else:
        shallow_view_index = view_index
        view_index += 1
        steep_view_index = view_index

        active_views.insert(
            shallow_view_index, copy.deepcopy(active_views[shallow_view_index])
        )
        _add_steep_bump(
            bottom_right[0], bottom_right[1], active_views, shallow_view_index
        )
        if not _check_view(active_views, view_index):
            view_index -= 1
            steep_view_index -= 1
        _add_shallow_bump(top_left[0], top_left[1], active_views, steep_view_index)
        _check_view(active_views, steep_view_index)


def _add_shallow_bump(
    x: int, y: int, active_views: list[_View], view_index: int
) -> None:
    active_views[view_index].shallow_line.xf = x
    active_views[view_index].shallow_line.yf = y

    active_views[view_index].shallow_bump = _ViewBump(
        x, y, active_views[view_index].shallow_bump
    )

    cur_bump = active_views[view_index].steep_bump
    while cur_bump is not None:
        if active_views[view_index].shallow_line.p_above(cur_bump.x, cur_bump.y):
            active_views[view_index].shallow_line.xi = cur_bump.x
            active_views[view_index].shallow_line.yi = cur_bump.y

        cur_bump = cur_bump.parent


def _add_steep_bump(x: int, y: int, active_views: list[_View], view_index: int) -> None:
    active_views[view_index].steep_line.xf = x
    active_views[view_index].steep_line.yf = y

    active_views[view_index].steep_bump = _ViewBump(
        x, y, active_views[view_index].steep_bump
    )

    cur_bump = active_views[view_index].shallow_bump

    while cur_bump is not None:
        if active_views[view_index].steep_line.p_below(cur_bump.x, cur_bump.y):
            active_views[view_index].steep_line.xi = cur_bump.x
            active_views[view_index].steep_line.yi = cur_bump.y

        cur_bump = cur_bump.parent


def _check_view(active_views: list[_View], view_index: int) -> bool:
    shallow_line = active_views[view_index].shallow_line
    steep_line = active_views[view_index].steep_line

    if shallow_line.line_colinear(steep_line) and (
        shallow_line.p_colinear(0, 1) or shallow_line.p_colinear(1, 0)
    ):
        del active_views[view_index]
        return False
    else:
        return True
