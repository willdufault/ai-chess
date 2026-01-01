from enum import Enum, auto


class GameStatus(Enum):
    ACTIVE = auto()
    CHECKMATE = auto()
    STALEMATE = auto()
