import pytest

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook
from models.rules import Rules


@pytest.fixture
def board() -> Board:
    return Board()


def test_is_in_check_pawn(board: Board) -> None:
    board.set_piece(Coordinate(3, 3), King(Color.WHITE))
    board.set_piece(Coordinate(4, 4), Pawn(Color.BLACK))
    board.set_piece(Coordinate(4, 4), Pawn(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Coordinate(4, 4), None)
    board.set_piece(Coordinate(4, 2), Pawn(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Coordinate(4, 3), Pawn(Color.BLACK))
    board.set_piece(Coordinate(4, 2), Pawn(Color.WHITE))
    board.set_piece(Coordinate(5, 5), Pawn(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == False


def test_is_in_check_knight(board: Board) -> None:
    board.set_piece(Coordinate(3, 3), King(Color.WHITE))
    board.set_piece(Coordinate(4, 3), Knight(Color.BLACK))
    board.set_piece(Coordinate(4, 2), Knight(Color.BLACK))
    board.set_piece(Coordinate(5, 2), Knight(Color.WHITE))
    assert Rules.is_in_check(Color.WHITE, board) == False

    board.set_piece(Coordinate(5, 2), Knight(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == True


def test_is_in_check_diagonal(board: Board) -> None:
    board.set_piece(Coordinate(3, 3), King(Color.WHITE))
    board.set_piece(Coordinate(4, 3), Bishop(Color.BLACK))
    board.set_piece(Coordinate(4, 2), Bishop(Color.WHITE))
    board.set_piece(Coordinate(5, 2), Bishop(Color.BLACK))
    board.set_piece(Coordinate(5, 1), Bishop(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == False

    board.set_piece(Coordinate(4, 2), None)
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Coordinate(4, 3), Queen(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == True


def test_is_in_check_horizontal(board: Board) -> None:
    board.set_piece(Coordinate(3, 3), King(Color.WHITE))
    board.set_piece(Coordinate(4, 3), Rook(Color.WHITE))
    board.set_piece(Coordinate(4, 2), Rook(Color.BLACK))
    board.set_piece(Coordinate(5, 2), Rook(Color.BLACK))
    board.set_piece(Coordinate(5, 3), Rook(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == False

    board.set_piece(Coordinate(4, 3), None)
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Coordinate(5, 3), Queen(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) == True