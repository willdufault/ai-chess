from .coordinate import Coordinate
from .pieces import FirstMovePiece, Piece


class Move:
    def __init__(
        self,
        from_coord: Coordinate,
        to_coord: Coordinate,
        from_piece: Piece,
        to_piece: Piece | None,
    ) -> None:
        self._from_coord = from_coord
        self._to_coord = to_coord
        self._from_piece = from_piece
        self._from_piece_has_moved = (
            from_piece.has_moved if isinstance(from_piece, FirstMovePiece) else False
        )
        self._to_piece = to_piece

    @property
    def from_coord(self) -> Coordinate:
        return self._from_coord

    @property
    def to_coord(self) -> Coordinate:
        return self._to_coord

    @property
    def from_piece(self) -> Piece:
        return self._from_piece

    @property
    def from_piece_has_moved(self) -> bool:
        return self._from_piece_has_moved

    @property
    def to_piece(self) -> Piece | None:
        return self._to_piece
