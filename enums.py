from __future__ import annotations

from enum import Enum


class Color(Enum):
    WHITE = True
    BLACK = False

    @staticmethod
    def get_other_color(color: Color):
        return Color.WHITE if color is Color.WHITE else Color.BLACK


class GameMode(Enum):
    TWO_PLAYER = 0
    AI = 1
