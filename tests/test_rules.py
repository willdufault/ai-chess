import pytest

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook
from models.rules import Rules
from utils.board_utils import print_bitboard as _pb


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


def test_is_in_checkmate_no_escape(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 1), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1, 1), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1, 0), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 0), None)
    board.set_piece(Coordinate(2, 0), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(2, 0), None)
    board.set_piece(Coordinate(3, 0), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_smother(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 1), Rook(Color.WHITE))
    board.set_piece(Coordinate(1, 1), Bishop(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 2), Knight(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 0), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 0), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_capture(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 1), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1, 0), Pawn(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 1), Bishop(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 2), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_double(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 2), Rook(Color.BLACK))
    board.set_piece(Coordinate(2, 0), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 1), Pawn(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_guarded(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 1), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 1), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_block(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 1), Rook(Color.WHITE))
    board.set_piece(Coordinate(1, 1), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(3, 0), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(1, 1), Pawn(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_pinned(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    board.set_piece(Coordinate(0, 1), Rook(Color.WHITE))
    board.set_piece(Coordinate(1, 1), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(2, 0), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Coordinate(2, 2), Bishop(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True
