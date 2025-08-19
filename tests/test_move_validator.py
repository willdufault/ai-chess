from pytest import fixture

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_validator import MoveValidator
from models.pieces import Pawn


@fixture
def board() -> Board:
    return Board()


def test_is_move_valid_coordinate_out_of_bounds(board: Board) -> None:
    assert (
        MoveValidator.is_move_valid(
            Move(Color.WHITE, Coordinate(-1, 0), Coordinate(0, 0), None, None), board
        )
        is False
    )
    assert (
        MoveValidator.is_move_valid(
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(-1, 0), None, None), board
        )
        is False
    )


def test_is_move_valid_from_piece_none(board: Board) -> None:
    assert (
        MoveValidator.is_move_valid(
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 0), None, None), board
        )
        is False
    )


def test_is_move_valid_from_piece_opposite_color(board: Board) -> None:
    assert (
        MoveValidator.is_move_valid(
            Move(Color.BLACK, Coordinate(0, 0), Coordinate(0, 0), None, None), board
        )
        is False
    )


def test_is_move_valid_to_piece_same_color(board: Board) -> None:
    assert (
        MoveValidator.is_move_valid(
            Move(
                Color.WHITE, Coordinate(0, 0), Coordinate(0, 0), None, Pawn(Color.WHITE)
            ),
            board,
        )
        is False
    )
