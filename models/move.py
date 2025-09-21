from dataclasses import dataclass

from enums.color import Color
from models.coordinate import Coordinate
from models.piece import Piece


@dataclass(frozen=True, slots=True)
class Move:
    color: Color
    from_coordinate: Coordinate
    to_coordinate: Coordinate
    # from_piece: Piece | None
    # to_piece: Piece | None
