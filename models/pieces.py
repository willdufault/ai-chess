from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

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


@dataclass(slots=True)
class Piece(ABC):
    color: Color

    @property
    @abstractmethod
    def VALUE(self) -> int: ...

    @property
    @abstractmethod
    def MOVE_STRATEGY(self) -> MoveStrategy: ...

    @property
    @abstractmethod
    def symbol(self) -> str: ...

    def to_key(self) -> str:
        """Return an immutable version of the piece state for caching."""
        return self.symbol


@dataclass(slots=True)
class FirstMovePiece(Piece, ABC):
    has_moved: bool = False

    def to_key(self) -> str:
        """Return an immutable version of the piece state for caching."""
        return f"{self.symbol}{'+' if self.has_moved else '-'}"


@dataclass(slots=True)
class Pawn(FirstMovePiece):
    VALUE: ClassVar[int] = 1
    MOVE_STRATEGY: ClassVar[MoveStrategy] = PawnMoveStrategy()
    symbol: str = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = "♙" if self.color is Color.WHITE else "♟"


@dataclass(slots=True)
class Knight(Piece):
    VALUE: ClassVar[int] = 3
    MOVE_STRATEGY: ClassVar[MoveStrategy] = KnightMoveStrategy()
    symbol: str = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = "♘" if self.color is Color.WHITE else "♞"


@dataclass(slots=True)
class Bishop(Piece):
    VALUE: ClassVar[int] = 3
    MOVE_STRATEGY: ClassVar[MoveStrategy] = BishopMoveStrategy()
    symbol: str = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = "♗" if self.color is Color.WHITE else "♝"


@dataclass(slots=True)
class Rook(FirstMovePiece):
    VALUE: ClassVar[int] = 5
    MOVE_STRATEGY: ClassVar[MoveStrategy] = RookMoveStrategy()
    symbol: str = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = "♖" if self.color is Color.WHITE else "♜"


@dataclass(slots=True)
class Queen(Piece):
    VALUE: ClassVar[int] = 9
    MOVE_STRATEGY: ClassVar[MoveStrategy] = QueenMoveStrategy()
    symbol: str = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = "♕" if self.color is Color.WHITE else "♛"


@dataclass(slots=True)
class King(FirstMovePiece):
    VALUE: ClassVar[int] = 100
    MOVE_STRATEGY: ClassVar[MoveStrategy] = KingMoveStrategy()
    symbol: str = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = "♔" if self.color is Color.WHITE else "♚"
