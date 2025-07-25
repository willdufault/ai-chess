from abc import ABC

from enums import Color
from move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    MoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
)


class Piece(ABC):
    """Represents an abstract chess piece."""

    def __init__(
        self, color: Color, value: int, symbol: str, move_strategy: MoveStrategy
    ) -> None:
        self._color = color
        self._value = value
        self._symbol = symbol
        self._move_strategy = move_strategy
        self._tracks_first_move = False

    @property
    def color(self) -> Color:
        """Get the color of the piece."""
        return self._color

    @property
    def value(self) -> int:
        """Get the value of the piece."""
        return self._value

    @property
    def symbol(self) -> str:
        """Get the symbol of the piece."""
        return self._symbol

    @property
    def move_strategy(self) -> MoveStrategy:
        """Get the move strategy of the piece."""
        return self._move_strategy

    @property
    def tracks_first_move(self) -> Color:
        """Get whether the piece tracks its first move."""
        return self._tracks_first_move


class FirstMovePiece(Piece, ABC):
    """Represents an abstract chess piece that tracks whether it has moved."""

    def __init__(
        self, color: Color, value: int, symbol: str, move_strategy: MoveStrategy
    ) -> None:
        super().__init__(color, value, symbol, move_strategy)
        self._tracks_first_move = True
        self._has_moved = False

    @property
    def tracks_first_move(self) -> Color:
        """Get whether the piece tracks its first move."""
        return self._tracks_first_move

    @property
    def has_moved(self) -> bool:
        """Get whether the piece has moved."""
        return self._has_moved

    @has_moved.setter
    def has_moved(self, has_moved: bool) -> None:
        """Set whether the piece has moved."""
        self._has_moved = has_moved


class Pawn(FirstMovePiece):
    """Represents a pawn."""

    def __init__(self, color: Color) -> None:
        value = 1
        symbol = "♙" if color is Color.WHITE else "♟"
        super().__init__(color, value, symbol, PawnMoveStrategy())


class Knight(Piece):
    """Represents a knight."""

    def __init__(self, color: Color) -> None:
        value = 3
        symbol = "♘" if color is Color.WHITE else "♞"
        super().__init__(color, value, symbol, KnightMoveStrategy())


class Bishop(Piece):
    """Represents a bishop."""

    def __init__(self, color: Color) -> None:
        value = 3
        symbol = "♗" if color is Color.WHITE else "♝"
        super().__init__(color, value, symbol, BishopMoveStrategy())


class Rook(FirstMovePiece):
    """Represents a rook."""

    def __init__(self, color: Color) -> None:
        value = 5
        symbol = "♖" if color is Color.WHITE else "♜"
        super().__init__(color, value, symbol, RookMoveStrategy())


class Queen(Piece):
    """Represents a queen."""

    def __init__(self, color: Color) -> None:
        value = 9
        symbol = "♕" if color is Color.WHITE else "♛"
        super().__init__(color, value, symbol, QueenMoveStrategy())


class King(FirstMovePiece):
    """Represents a king."""

    def __init__(self, color: Color) -> None:
        value = 99
        symbol = "♔" if color is Color.WHITE else "♚"
        super().__init__(color, value, symbol, KingMoveStrategy())
