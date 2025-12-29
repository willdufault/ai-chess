from dataclasses import dataclass

from constants.board_constants import BOARD_SIZE
from utils.board_utils import calculate_shift


@dataclass
class Coordinate:
    row_index: int
    column_index: int

    @classmethod
    def from_mask(cls, square_mask: int) -> Coordinate:
        row_index, column_index = divmod(calculate_shift(square_mask), BOARD_SIZE)
        return cls(row_index, column_index)
