from enums.color import Color
from models.coordinate import Coordinate
from utils.board_utils import (
    get_last_row_index,
    is_coordinate_in_bounds,
    is_index_in_bounds,
)


def test_is_index_in_bounds() -> None:
    assert is_index_in_bounds(0) is True
    assert is_index_in_bounds(4) is True
    assert is_index_in_bounds(7) is True
    assert is_index_in_bounds(8) is False
    assert is_index_in_bounds(20) is False
    assert is_index_in_bounds(-1) is False

def test_is_coordinate_in_bounds() -> None:
    assert is_coordinate_in_bounds(Coordinate(0, 0)) is True
    assert is_coordinate_in_bounds(Coordinate(0, 4)) is True
    assert is_coordinate_in_bounds(Coordinate(7, 0)) is True
    assert is_coordinate_in_bounds(Coordinate(0, 8)) is False
    assert is_coordinate_in_bounds(Coordinate(20, 0)) is False
    assert is_coordinate_in_bounds(Coordinate(0, -1)) is False

def test_get_last_row_index() -> None:
    assert get_last_row_index(Color.WHITE) == 7
    assert get_last_row_index(Color.BLACK) == 0