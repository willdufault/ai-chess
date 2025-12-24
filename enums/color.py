from enum import Enum, auto


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(self, color: Color) -> Color:
        return Color.WHITE if color == Color.BLACK else Color.BLACK
