from enum import Enum, auto


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def __str__(self) -> str:
        return self.name.capitalize()
    
    @property
    def opposite(self) -> Color:
        return Color.WHITE if self == Color.BLACK else Color.BLACK

    @property
    def forward_row_delta(self) -> int:
        return 1 if self == Color.WHITE else -1
