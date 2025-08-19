from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums.color import Color
    from models.coordinate import Coordinate
    from models.pieces import Piece


class Move:
    def __init__(
        self,
        color: Color,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        from_piece: Piece | None,
        to_piece: Piece | None,
    ) -> None:
        self._color = color
        self._from_coordinate = from_coordinate
        self._to_coordinate = to_coordinate
        self._from_piece = from_piece
        self._from_piece_has_moved = getattr(from_piece, "has_moved", False)
        self._to_piece = to_piece

    @property
    def color(self) -> Color:
        return self._color

    @property
    def from_coordinate(self) -> Coordinate:
        return self._from_coordinate

    @property
    def to_coordinate(self) -> Coordinate:
        return self._to_coordinate

    @property
    def from_piece(self) -> Piece | None:
        return self._from_piece

    @property
    def from_piece_has_moved(self) -> bool:
        return self._from_piece_has_moved

    @property
    def to_piece(self) -> Piece | None:
        return self._to_piece
