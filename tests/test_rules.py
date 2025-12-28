import pytest

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook
from models.rules import Rules


@pytest.fixture
def board() -> Board:
    return Board()


def test_is_in_check_pawn(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(3, 3))
    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 4))
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(None, Coordinate(4, 4))
    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 2))
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 3))
    board.set_piece(Pawn(Color.WHITE), Coordinate(4, 2))
    board.set_piece(Pawn(Color.BLACK), Coordinate(5, 5))
    assert Rules.is_in_check(Color.WHITE, board) == False


def test_is_in_check_knight(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(3, 3))
    board.set_piece(Knight(Color.BLACK), Coordinate(4, 3))
    board.set_piece(Knight(Color.BLACK), Coordinate(4, 2))
    board.set_piece(Knight(Color.WHITE), Coordinate(5, 2))
    assert Rules.is_in_check(Color.WHITE, board) == False

    board.set_piece(Knight(Color.BLACK), Coordinate(5, 2))
    assert Rules.is_in_check(Color.WHITE, board) == True


def test_is_in_check_diagonal(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(3, 3))
    board.set_piece(Bishop(Color.BLACK), Coordinate(4, 3))
    board.set_piece(Bishop(Color.WHITE), Coordinate(4, 2))
    board.set_piece(Bishop(Color.BLACK), Coordinate(5, 2))
    board.set_piece(Bishop(Color.BLACK), Coordinate(5, 1))
    assert Rules.is_in_check(Color.WHITE, board) == False

    board.set_piece(None, Coordinate(4, 2))
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Queen(Color.BLACK), Coordinate(4, 3))
    assert Rules.is_in_check(Color.WHITE, board) == True


def test_is_in_check_orthogonal(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(3, 3))
    board.set_piece(Rook(Color.WHITE), Coordinate(4, 3))
    board.set_piece(Rook(Color.BLACK), Coordinate(4, 2))
    board.set_piece(Rook(Color.BLACK), Coordinate(5, 2))
    board.set_piece(Rook(Color.BLACK), Coordinate(5, 3))
    assert Rules.is_in_check(Color.WHITE, board) == False

    board.set_piece(None, Coordinate(4, 3))
    assert Rules.is_in_check(Color.WHITE, board) == True

    board.set_piece(Queen(Color.BLACK), Coordinate(5, 3))
    assert Rules.is_in_check(Color.WHITE, board) == True


def test_is_in_checkmate_no_escape(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Pawn(Color.WHITE), Coordinate(0, 1))
    board.set_piece(Pawn(Color.WHITE), Coordinate(1, 1))
    board.set_piece(Rook(Color.WHITE), Coordinate(1, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(None, Coordinate(1, 0))
    board.set_piece(Rook(Color.WHITE), Coordinate(2, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(None, Coordinate(2, 0))
    board.set_piece(Rook(Color.BLACK), Coordinate(3, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_smother(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Rook(Color.WHITE), Coordinate(0, 1))
    board.set_piece(Bishop(Color.WHITE), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Knight(Color.BLACK), Coordinate(1, 2))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Rook(Color.BLACK), Coordinate(1, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Rook(Color.WHITE), Coordinate(1, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_capture(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Pawn(Color.WHITE), Coordinate(0, 1))
    board.set_piece(Pawn(Color.WHITE), Coordinate(1, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Bishop(Color.BLACK), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Rook(Color.BLACK), Coordinate(1, 2))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_double(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Rook(Color.BLACK), Coordinate(0, 2))
    board.set_piece(Rook(Color.BLACK), Coordinate(2, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Pawn(Color.WHITE), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_guarded(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Rook(Color.BLACK), Coordinate(0, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Rook(Color.BLACK), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_block(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Rook(Color.WHITE), Coordinate(0, 1))
    board.set_piece(Rook(Color.WHITE), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Rook(Color.BLACK), Coordinate(3, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Pawn(Color.WHITE), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_in_checkmate_pinned(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(0, 0))
    board.set_piece(Rook(Color.WHITE), Coordinate(0, 1))
    board.set_piece(Rook(Color.WHITE), Coordinate(1, 1))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Rook(Color.BLACK), Coordinate(2, 0))
    assert Rules.is_in_checkmate(Color.WHITE, board) == False

    board.set_piece(Bishop(Color.BLACK), Coordinate(2, 2))
    assert Rules.is_in_checkmate(Color.WHITE, board) == True


def test_is_legal_pawn_move(board: Board) -> None:
    board.set_piece(Pawn(Color.WHITE), Coordinate(3, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 3), Pawn(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == True

    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 3),
        Pawn(Color.WHITE),
        Pawn(Color.BLACK),
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == False

    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 4), Pawn(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == False

    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 4))
    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 4),
        Pawn(Color.WHITE),
        Pawn(Color.BLACK),
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True

    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(2, 3),
        Pawn(Color.WHITE),
        None,
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == False


def test_is_legal_bishop_move(board: Board) -> None:
    board.set_piece(Bishop(Color.WHITE), Coordinate(3, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(3, 4), Bishop(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == False

    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 4),
        Bishop(Color.WHITE),
        None,
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True

    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 4))
    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 4),
        Bishop(Color.WHITE),
        Pawn(Color.BLACK),
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True

    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(5, 5),
        Bishop(Color.WHITE),
        None,
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == False


def test_is_legal_rook_move(board: Board) -> None:
    board.set_piece(Rook(Color.WHITE), Coordinate(3, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 4), Rook(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == False

    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 3),
        Rook(Color.WHITE),
        None,
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True

    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 3),
        Rook(Color.WHITE),
        Pawn(Color.BLACK),
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True

    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(5, 3),
        Rook(Color.WHITE),
        None,
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == False


def test_is_legal_knight_move(board: Board) -> None:
    board.set_piece(Knight(Color.WHITE), Coordinate(3, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 3), Knight(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == False

    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 4), Knight(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == False

    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(5, 2), Knight(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == True

    board.set_piece(Pawn(Color.BLACK), Coordinate(5, 4))
    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(5, 4),
        Knight(Color.WHITE),
        Pawn(Color.BLACK),
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True


def test_is_legal_king_move(board: Board) -> None:
    board.set_piece(King(Color.WHITE), Coordinate(3, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 3), King(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == True

    move = Move.from_coordinates(
        Coordinate(3, 3), Coordinate(4, 4), King(Color.WHITE), None, Color.WHITE
    )
    assert Rules.is_legal_move(move, board) == True

    board.set_piece(Pawn(Color.BLACK), Coordinate(4, 3))
    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(4, 3),
        King(Color.WHITE),
        Pawn(Color.BLACK),
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == True

    move = Move.from_coordinates(
        Coordinate(3, 3),
        Coordinate(5, 3),
        King(Color.WHITE),
        None,
        Color.WHITE,
    )
    assert Rules.is_legal_move(move, board) == False
