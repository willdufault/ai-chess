from constants.board_constants import BOARD_SIZE
from models.coordinate import Coordinate


def is_coordinate_in_bounds(coordinate: Coordinate) -> bool:
    return (
        0 <= coordinate.row_index < BOARD_SIZE
        and 0 <= coordinate.column_index < BOARD_SIZE
    )


def signed_shift(base: int, shift: int) -> int:
    return base << shift if shift > 0 else base >> -shift
