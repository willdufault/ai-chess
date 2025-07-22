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
        self.color = color
        self.value = value
        self.symbol = symbol
        self.move_strategy = move_strategy


class Pawn(Piece):
    """Represents a pawn."""

    def __init__(self, color: Color) -> None:
        value = 1
        symbol = "♟" if color == Color.WHITE else "♙"
        super().__init__(color, value, symbol, PawnMoveStrategy())
        self.has_moved = False


class Knight(Piece):
    """Represents a knight."""

    def __init__(self, color: Color) -> None:
        value = 3
        symbol = "♞" if color == Color.WHITE else "♘"
        super().__init__(color, value, symbol, KnightMoveStrategy())


class Bishop(Piece):
    """Represents a bishop."""

    def __init__(self, color: Color) -> None:
        value = 3
        symbol = "♝" if color == Color.WHITE else "♗"
        super().__init__(color, value, symbol, BishopMoveStrategy())


class Rook(Piece):
    """Represents a rook."""

    def __init__(self, color: Color) -> None:
        value = 5
        symbol = "♜" if color == Color.WHITE else "♖"
        super().__init__(color, value, symbol, RookMoveStrategy())
        self.has_moved = False


class Queen(Piece):
    """Represents a queen."""

    def __init__(self, color: Color) -> None:
        value = 9
        symbol = "♛" if color == Color.WHITE else "♕"
        super().__init__(color, value, symbol, QueenMoveStrategy())


class King(Piece):
    """Represents a king."""

    def __init__(self, color: Color) -> None:
        value = 99
        symbol = "♚" if color == Color.WHITE else "♔"
        super().__init__(color, value, symbol, KingMoveStrategy())
        self.has_moved = False
