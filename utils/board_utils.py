from models.board import BOARD_SIZE
from models.coordinate import Coordinate


def is_coordinate_in_bounds(coordinate: Coordinate) -> bool:
    return (
        0 <= coordinate.row_index < BOARD_SIZE
        and 0 <= coordinate.column_index < BOARD_SIZE
    )
