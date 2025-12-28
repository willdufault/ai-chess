from constants.board_constants import BOARD_SIZE
from models.coordinate import Coordinate
from utils.bit_utils import intersects


def is_index_in_bounds(index: int) -> bool:
    return 0 <= index < BOARD_SIZE


def is_coordinate_in_bounds(coordinate: Coordinate) -> bool:
    return is_index_in_bounds(coordinate.row_index) and is_index_in_bounds(
        coordinate.column_index
    )


def calculate_mask(row_index: int, column_index: int) -> int:
    shift = BOARD_SIZE * row_index + column_index
    return 1 << shift


def is_orthogonal(row_delta: int, column_delta: int) -> bool:
    return (row_delta, column_delta).count(0) == 1


def is_diagonal(row_delta: int, column_delta: int) -> bool:
    return abs(row_delta) == abs(column_delta)


def enumerate_mask(mask: int) -> list[int]:
    bits = []
    for shift in range(BOARD_SIZE**2):
        bit = 1 << shift
        if intersects(mask, bit):
            bits.append(bit)
    return bits


def print_bitboard(bitboard: int) -> None:
    for row_index in reversed(range(BOARD_SIZE)):
        for column_index in range(BOARD_SIZE):
            square_mask = calculate_mask(row_index, column_index)
            if bitboard & square_mask != 0:
                print("x", end=" ")
            else:
                print(".", end=" ")
        print()
