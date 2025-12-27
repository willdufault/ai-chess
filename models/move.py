from dataclasses import dataclass

from enums.color import Color
from models.coordinate import Coordinate
from models.piece import Piece
from utils.board_utils import calculate_mask


@dataclass
class Move:
    from_square_mask: int
    to_square_mask: int
    from_piece: Piece | None
    to_piece: Piece | None
    color: Color

    @classmethod
    def from_coordinates(
        cls,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        from_piece: Piece | None,
        to_piece: Piece | None,
        color: Color,
    ) -> Move:
        from_square_mask = calculate_mask(
            from_coordinate.row_index, from_coordinate.column_index
        )
        to_square_mask = calculate_mask(
            to_coordinate.row_index, to_coordinate.column_index
        )
        return cls(from_square_mask, to_square_mask, from_piece, to_piece, color)
