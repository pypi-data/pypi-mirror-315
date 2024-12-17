"""Definitions for various values that are used throughout the library."""

from __future__ import annotations
from enum import Enum, auto

import numpy as np

#: List of relative coordinates in a tile's neighborhood
NEIGHBORHOOD: list[tuple[int, int]] = [(x,y) for x in range(-2, 3) for y in range(-2, 3) if (x,y) != (0,0)]

#: List of relative coordinates for a tile's neighbors in 4 directions
DIR4: list[tuple[int, int]] = [(x,y) for x in range(-1, 2) for y in range(-1, 2) if ((x,y) != (0,0)) and (x == 0 or y ==0)]

#: List of relative coordinates for a tile's neighbors in 8 directions
DIR8: list[tuple[int, int]] = [(x,y) for x in range(-1, 2) for y in range(-1,2) if (x,y) !=(0,0)]

class DIRS(Enum):
    """Represents the choices available for movement directions."""
    #: 4 directions
    DIR4 = auto()
    #: 8 directions
    DIR8 = auto()


class STRINGS:
    """Strings for use throughout the library."""
    #: Used to reference whether a tile is walkable in :data:`TILE_DTYPE`
    WALKABLE = "walkable"
    #: Used to reference whether a tile passes light in :data:`TILE_DTYPE`
    TRANSPARENT = "transparent"
    #: Used to identify sprites in :data:`TILE_DTYPE`
    SPRITE = "sprite"


#: Used to create NDArrays of tiles
TILE_DTYPE = np.dtype(
    [
        (STRINGS.WALKABLE, np.bool),
        (STRINGS.TRANSPARENT, np.bool),
        (STRINGS.SPRITE, int),
    ]
)