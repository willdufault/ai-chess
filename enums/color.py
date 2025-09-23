from enum import Enum


class Color(Enum):
    WHITE = True
    BLACK = False

    @property
    def opposite(self) -> Color:
        return Color.WHITE if self.value is Color.BLACK else Color.BLACK
