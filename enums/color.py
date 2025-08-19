from enum import Enum


class Color(Enum):
    WHITE = True
    BLACK = False

    def __str__(self) -> str:
        return self.name.capitalize()

    @property
    def opposite(self) -> Color:
        """Return the opposite color."""
        return Color.WHITE if self is Color.BLACK else Color.BLACK
