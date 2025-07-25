from enum import Enum


class Color(Enum):
    WHITE = True
    BLACK = False


class GameMode(Enum):
    TWO_PLAYER = 1
    AI = 2
