from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from enums.color import Color


@dataclass(frozen=True, slots=True)
class Piece(ABC):
    color: Color

    @property
    @abstractmethod
    def VALUE(self) -> int: ...


@dataclass(frozen=True, slots=True)
class Pawn(Piece):
    VALUE: ClassVar[int] = 1


@dataclass(frozen=True, slots=True)
class Knight(Piece):
    VALUE: ClassVar[int] = 3


@dataclass(frozen=True, slots=True)
class Bishop(Piece):
    VALUE: ClassVar[int] = 3


@dataclass(frozen=True, slots=True)
class Rook(Piece):
    VALUE: ClassVar[int] = 5


@dataclass(frozen=True, slots=True)
class Queen(Piece):
    VALUE: ClassVar[int] = 9


@dataclass(frozen=True, slots=True)
class King(Piece):
    VALUE: ClassVar[int] = 100
