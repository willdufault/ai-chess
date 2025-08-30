from pytest import fixture

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.pieces import Bishop, Knight, Pawn, Queen, Rook
from models.rules import Rules


@fixture
def board() -> Board:
    return Board()


def test_is_in_check(board: Board) -> None:
    board.set_up_pieces()
    assert Rules.is_in_check(Color.WHITE, board) is False
    board.set_piece(Coordinate(1, 4), Rook(Color.BLACK))
    assert Rules.is_in_check(Color.WHITE, board) is True


def test_is_in_checkmate_smother(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(0, 5), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(1, 6), Knight(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is True


def test_is_in_checkmate_back_rank(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(0, 5), None)
    board.set_piece(Coordinate(0, 6), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(0, 7), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is True


def test_is_in_checkmate_back_rank_block(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(0, 5), None)
    board.set_piece(Coordinate(0, 6), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(0, 7), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is True
    board.set_piece(Coordinate(1, 6), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) is False


def test_is_in_checkmate_back_rank_capture(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(0, 5), None)
    board.set_piece(Coordinate(0, 6), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(0, 7), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is True
    board.set_piece(Coordinate(1, 7), Rook(Color.WHITE))
    assert Rules.is_in_checkmate(Color.WHITE, board) is False


def test_is_in_checkmate_back_rank_escape(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(0, 5), None)
    board.set_piece(Coordinate(0, 6), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(0, 7), Rook(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is True
    board.set_piece(Coordinate(1, 4), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is False


def test_is_in_checkmate_scholars(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(1, 5), Queen(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(3, 7), Bishop(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is True


def test_is_in_checkmate_double(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(2, 4), Rook(Color.BLACK))
    board.set_piece(Coordinate(2, 2), Bishop(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(1, 3), None)
    board.set_piece(Coordinate(1, 4), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is True


def test_is_in_checkmate_double_escape(board: Board) -> None:
    board = board
    board.set_up_pieces()
    board.set_piece(Coordinate(2, 4), Rook(Color.BLACK))
    board.set_piece(Coordinate(2, 2), Bishop(Color.BLACK))
    assert Rules.is_in_checkmate(Color.WHITE, board) is False
    board.set_piece(Coordinate(1, 3), None)
    board.set_piece(Coordinate(1, 4), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is True
    board.set_piece(Coordinate(1, 5), None)
    assert Rules.is_in_checkmate(Color.WHITE, board) is False

def test_does_move_trigger_promotion(board: Board) -> None:
    move_triggers = Move(
        Color.WHITE, Coordinate(0, 0), Coordinate(7, 0), Pawn(Color.WHITE), None
    )
    move_wrong_row = Move(
        Color.WHITE, Coordinate(0, 0), Coordinate(1, 0), Pawn(Color.WHITE), None
    )
    move_wrong_piece = Move(
        Color.WHITE, Coordinate(0, 0), Coordinate(7, 0), Knight(Color.WHITE), None
    )
    assert Rules.does_move_trigger_promotion(move_triggers) is True
    assert Rules.does_move_trigger_promotion(move_wrong_piece) is False
    assert Rules.does_move_trigger_promotion(move_wrong_row) is False

def test_get_legal_moves(board: Board) -> None:
    assert Rules.get_legal_moves(Color.WHITE, board) == []
    board.set_up_pieces()
    board.set_piece(Coordinate(1, 0), None)
    board.set_piece(Coordinate(1, 4), None)
    board.set_piece(Coordinate(4, 7), Bishop(Color.BLACK))
    pawn = board.get_piece(Coordinate(1, 1))
    assert isinstance(pawn, Pawn)
    pawn.has_moved = True
    assert Rules.get_legal_moves(Color.WHITE, board) == [
        Move(Color.WHITE, Coordinate(0,0), Coordinate(1,0), Rook(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(2,0), Rook(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(3,0), Rook(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(4,0), Rook(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(5,0), Rook(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(6,0), Rook(Color.WHITE), Pawn(Color.BLACK)),
        Move(Color.WHITE, Coordinate(0,1), Coordinate(2,2), Knight(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,1), Coordinate(2,0), Knight(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,3), Coordinate(1,4), Queen(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,3), Coordinate(2,5), Queen(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,3), Coordinate(3,6), Queen(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,3), Coordinate(4,7), Queen(Color.WHITE), Bishop(Color.BLACK)),
        Move(Color.WHITE, Coordinate(0,5), Coordinate(1,4), Bishop(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,5), Coordinate(2,3), Bishop(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,5), Coordinate(3,2), Bishop(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,5), Coordinate(4,1), Bishop(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,5), Coordinate(5,0), Bishop(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,6), Coordinate(1,4), Knight(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,6), Coordinate(2,7), Knight(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(0,6), Coordinate(2,5), Knight(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,1), Coordinate(2,1), pawn, None),
        Move(Color.WHITE, Coordinate(1,2), Coordinate(2,2), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,2), Coordinate(3,2), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,3), Coordinate(2,3), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,3), Coordinate(3,3), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,5), Coordinate(2,5), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,5), Coordinate(3,5), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,6), Coordinate(2,6), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,6), Coordinate(3,6), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,7), Coordinate(2,7), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(1,7), Coordinate(3,7), Pawn(Color.WHITE), None),
    ]