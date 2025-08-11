from __future__ import annotations

from enum import Enum


class Color(Enum):
    WHITE = True
    BLACK = False

    def __str__(self) -> str:
        return self.name.capitalize()

    @staticmethod
    def get_other_color(color: Color):
        """Return the other color than the one given."""
        return Color.WHITE if color is Color.BLACK else Color.BLACK


class GameMode(Enum):
    TWO_PLAYER = 0
    AI = 1
