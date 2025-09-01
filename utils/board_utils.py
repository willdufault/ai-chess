from constants.board_constants import BOARD_SIZE
from enums.color import Color
from models.coordinate import Coordinate


@staticmethod
def is_index_in_bounds(index: int) -> bool:
    """Return whether the index is in bounds."""
    return 0 <= index < BOARD_SIZE


@staticmethod
def is_coordinate_in_bounds(coordinate: Coordinate) -> bool:
    """Return whether the coordinate is in bounds."""
    return is_index_in_bounds(coordinate.row_index) and is_index_in_bounds(
        coordinate.column_index
    )


@staticmethod
def get_last_row_index(color: Color) -> int:
    """Return the index of the last row for the color."""
    return BOARD_SIZE - 1 if color is Color.WHITE else 0


def get_board_index(coordinate: Coordinate) -> int:
    """Return the index of the square that corresponds with the coordinate."""
    return coordinate.row_index * BOARD_SIZE + coordinate.column_index
