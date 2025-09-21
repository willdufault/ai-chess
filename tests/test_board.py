from pytest import fixture

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Pawn


@fixture
def board() -> Board:
    return Board()


def test_make_move(board: Board) -> None:
    from_coordinate = Coordinate(0, 0)
    to_coordinate = Coordinate(0, 1)
    from_piece = Pawn(Color.WHITE)
    to_piece = Pawn(Color.BLACK)
    move = Move(Color.WHITE, from_coordinate, to_coordinate)

    board.set_piece(from_coordinate, from_piece)
    board.set_piece(to_coordinate, to_piece)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece

    board.make_move(move)
    assert board.get_piece(from_coordinate) is None
    assert board.get_piece(to_coordinate) == from_piece


def test_generate_white_pawn_moves(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1, 1), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2, 1), Pawn(Color.BLACK))
    board.set_piece(Coordinate(6, 6), Pawn(Color.WHITE))
    board.set_piece(Coordinate(7, 7), Pawn(Color.WHITE))
    assert set(board.generate_white_pawn_moves()) == set(
        [
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(1, 0)),
            Move(Color.WHITE, Coordinate(6, 6), Coordinate(7, 6)),
        ]
    )
