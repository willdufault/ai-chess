from enum import Enum, auto


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    @property
    def opposite(self) -> Color:
        return Color.WHITE if self.value == Color.BLACK else Color.BLACK

    @property
    def forward_row_delta(self) -> int:
        return 1 if self.value == Color.WHITE else -1
