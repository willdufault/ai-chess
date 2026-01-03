from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from enums.color import Color


@dataclass(frozen=True, slots=True)
class Piece(ABC):
    VALUE: ClassVar[int] = 0
    color: Color


class Pawn(Piece):
    VALUE: ClassVar[int] = 1


class Knight(Piece):
    VALUE: ClassVar[int] = 3


class Bishop(Piece):
    VALUE: ClassVar[int] = 3


class Rook(Piece):
    VALUE: ClassVar[int] = 5


class Queen(Piece):
    VALUE: ClassVar[int] = 9


class King(Piece):
    VALUE: ClassVar[int] = 1000
