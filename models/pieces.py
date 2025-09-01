from abc import ABC, abstractmethod

from enums.color import Color

from .move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    MoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
)


class Piece(ABC):
    def __init__(self, color: Color) -> None:
        self._color = color

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.color == other.color

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(color={self.color})"

    def to_key(self) -> str:
        """Return an immutable version of the piece state for caching."""
        return self.symbol

    @property
    def color(self) -> Color:
        return self._color

    @property
    @abstractmethod
    def VALUE(self) -> int:
        pass

    @property
    @abstractmethod
    def MOVE_STRATEGY(self) -> MoveStrategy:
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass


class FirstMovePiece(Piece, ABC):
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self._has_moved = False

    def to_key(self) -> str:
        """Return an immutable version of the piece state for caching."""
        return f"{self.symbol}{'+' if self._has_moved else '-'}"

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    @has_moved.setter
    def has_moved(self, has_moved: bool) -> None:
        self._has_moved = has_moved


class Pawn(FirstMovePiece):
    @property
    def VALUE(self) -> int:
        return 1

    @property
    def MOVE_STRATEGY(self) -> MoveStrategy:
        return PawnMoveStrategy()

    @property
    def symbol(self) -> str:
        return "♙" if self.color is Color.WHITE else "♟"


class Knight(Piece):
    @property
    def VALUE(self) -> int:
        return 3

    @property
    def MOVE_STRATEGY(self) -> MoveStrategy:
        return KnightMoveStrategy()

    @property
    def symbol(self) -> str:
        return "♘" if self.color is Color.WHITE else "♞"


class Bishop(Piece):
    @property
    def VALUE(self) -> int:
        return 3

    @property
    def MOVE_STRATEGY(self) -> MoveStrategy:
        return BishopMoveStrategy()

    @property
    def symbol(self) -> str:
        return "♗" if self.color is Color.WHITE else "♝"


class Rook(FirstMovePiece):
    @property
    def VALUE(self) -> int:
        return 5

    @property
    def MOVE_STRATEGY(self) -> MoveStrategy:
        return RookMoveStrategy()

    @property
    def symbol(self) -> str:
        return "♖" if self.color is Color.WHITE else "♜"


class Queen(Piece):
    @property
    def VALUE(self) -> int:
        return 9

    @property
    def MOVE_STRATEGY(self) -> MoveStrategy:
        return QueenMoveStrategy()

    @property
    def symbol(self) -> str:
        return "♕" if self.color is Color.WHITE else "♛"


class King(FirstMovePiece):
    @property
    def VALUE(self) -> int:
        return 100

    @property
    def MOVE_STRATEGY(self) -> MoveStrategy:
        return KingMoveStrategy()

    @property
    def symbol(self) -> str:
        return "♔" if self.color is Color.WHITE else "♚"
