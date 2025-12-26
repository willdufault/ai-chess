from constants.board_constants import BOARD_SIZE
from models.coordinate import Coordinate


def is_coordinate_in_bounds(coordinate: Coordinate) -> bool:
    return (
        0 <= coordinate.row_index < BOARD_SIZE
        and 0 <= coordinate.column_index < BOARD_SIZE
    )


def signed_shift(base: int, shift: int) -> int:
    return base << shift if shift > 0 else base >> -shift


def calculate_mask(row_index: int, column_index: int) -> int:
    shift = row_index * BOARD_SIZE + column_index
    return 1 << shift


def print_bitboard(bitboard: int) -> None:
    for row_index in reversed(range(BOARD_SIZE)):
        for column_index in range(BOARD_SIZE):
            square = calculate_mask(row_index, column_index)
            if bitboard & square != 0:
                print("x", end=" ")
            else:
                print(".", end=" ")
        print()
