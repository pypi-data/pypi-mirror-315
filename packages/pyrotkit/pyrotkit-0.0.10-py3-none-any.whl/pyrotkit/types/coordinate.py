from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Coordinate:
    """A location on a 2D grid"""
    x: int
    y: int

