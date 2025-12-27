from dataclasses import dataclass

from constants.board_constants import BOARD_SIZE


@dataclass
class Coordinate:
    row_index: int
    column_index: int

    @classmethod
    def from_mask(cls, square_mask: int) -> Coordinate:
        row_index, column_index = divmod(square_mask.bit_length() - 1, BOARD_SIZE)
        return cls(row_index, column_index)
