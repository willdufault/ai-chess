from dataclasses import dataclass

from enums.color import Color
from models.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class Move:
    color: Color
    from_coordinate: Coordinate
    to_coordinate: Coordinate
