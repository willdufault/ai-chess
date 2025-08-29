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
        self._to_piece = to_piece
        self._from_piece_has_moved = getattr(from_piece, "has_moved", False)

    def __repr__(self) -> str:
        return f"Move(color={self._color}, from_c={self._from_coordinate}, to_c={self._to_coordinate}, from_p={self._from_piece}, to_p={self._to_piece})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return False
        return (
            self._color == other.color
            and self._from_coordinate == other.from_coordinate
            and self._to_coordinate == other.to_coordinate
            and self._from_piece == other.from_piece
            and self._to_piece == other.to_piece
            and self._from_piece_has_moved == other.from_piece_has_moved
        )

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
    def to_piece(self) -> Piece | None:
        return self._to_piece

    @property
    def from_piece_has_moved(self) -> bool:
        return self._from_piece_has_moved
