from pytest import fixture

from controllers.board_controller import BoardController
from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.pieces import Bishop, King, Knight, Pawn, Queen, Rook


@fixture
def board_controller() -> BoardController:
    board = Board()
    return BoardController(board)


def test_make_move(board_controller: BoardController) -> None:
    board = board_controller.board
    from_coordinate = Coordinate(0, 0)
    to_coordinate = Coordinate(1, 1)
    from_piece = Pawn(Color.WHITE)
    to_piece = Pawn(Color.BLACK)
    board.set_piece(from_coordinate, from_piece)
    board.set_piece(to_coordinate, to_piece)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece
    move = Move(Color.WHITE, from_coordinate, to_coordinate, from_piece, to_piece)
    board_controller.make_move(move)
    assert board.get_piece(from_coordinate) == None
    assert board.get_piece(to_coordinate) == from_piece
    assert from_piece.has_moved is True


def test_undo_move(board_controller: BoardController) -> None:
    # TODO: this is copied from test_make_move, DRY
    board = board_controller.board
    from_coordinate = Coordinate(0, 0)
    to_coordinate = Coordinate(1, 1)
    from_piece = Pawn(Color.WHITE)
    to_piece = Pawn(Color.BLACK)
    board.set_piece(from_coordinate, from_piece)
    board.set_piece(to_coordinate, to_piece)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece
    move = Move(Color.WHITE, from_coordinate, to_coordinate, from_piece, to_piece)
    board_controller.make_move(move)
    assert board.get_piece(from_coordinate) == None
    assert board.get_piece(to_coordinate) == from_piece
    assert from_piece.has_moved is True
    board_controller.undo_move(move)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece
    assert from_piece.has_moved is False


def test_does_move_trigger_promotion(board_controller: BoardController) -> None:
    move_triggers = Move(
        Color.WHITE, Coordinate(0, 0), Coordinate(7, 0), Pawn(Color.WHITE), None
    )
    move_wrong_row = Move(
        Color.WHITE, Coordinate(0, 0), Coordinate(1, 0), Pawn(Color.WHITE), None
    )
    move_wrong_piece = Move(
        Color.WHITE, Coordinate(0, 0), Coordinate(7, 0), Knight(Color.WHITE), None
    )
    assert board_controller.does_move_trigger_promotion(move_triggers) is True
    assert board_controller.does_move_trigger_promotion(move_wrong_piece) is False
    assert board_controller.does_move_trigger_promotion(move_wrong_row) is False


def test_is_attacking_none(board_controller: BoardController) -> None:
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is False


def test_is_attacking_pawn(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(4, 2), Pawn(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is False
    board_controller.board.set_piece(Coordinate(2, 2), Pawn(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_attacking_knight(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(2, 1), Knight(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_attacking_bishop(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(2, 2), Bishop(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_attacking_rook(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(2, 3), Rook(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_attacking_queen_diagonal(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(2, 2), Queen(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_attacking_queen_straight(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(2, 3), Queen(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_attacking_king(board_controller: BoardController) -> None:
    board_controller.board.set_piece(Coordinate(2, 3), King(Color.WHITE))
    assert board_controller.is_attacking(Color.WHITE, Coordinate(3, 3)) is True


def test_is_in_check(board_controller: BoardController) -> None:
    board_controller.board.set_up_pieces()
    assert board_controller.is_in_check(Color.WHITE) is False
    board_controller.board.set_piece(Coordinate(1, 4), Rook(Color.BLACK))
    assert board_controller.is_in_check(Color.WHITE) is True

def test_is_in_checkmate_smother(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(0,5), Rook(Color.WHITE))
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(1,6), Knight(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is True


def test_is_in_checkmate_back_rank(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(0,5),None)
    board.set_piece(Coordinate(0,6),None)
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(0,7),Rook(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is True

def test_is_in_checkmate_back_rank_block(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(0,5),None)
    board.set_piece(Coordinate(0,6),None)
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(0,7),Rook(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is True
    board.set_piece(Coordinate(1,6),Rook(Color.WHITE))
    assert board_controller.is_in_checkmate(Color.WHITE) is False

def test_is_in_checkmate_back_rank_capture(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(0,5),None)
    board.set_piece(Coordinate(0,6),None)
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(0,7),Rook(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is True
    board.set_piece(Coordinate(1,7),Rook(Color.WHITE))
    assert board_controller.is_in_checkmate(Color.WHITE) is False

def test_is_in_checkmate_back_rank_escape(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(0,5),None)
    board.set_piece(Coordinate(0,6),None)
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(0,7),Rook(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is True
    board.set_piece(Coordinate(1,4),None)
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    

def test_is_in_checkmate_scholars(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(1,5), Queen(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(3,7), Bishop(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is True
    

def test_is_in_checkmate_double(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(2,4), Rook(Color.BLACK))
    board.set_piece(Coordinate(2,2), Bishop(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(1,3), None)
    board.set_piece(Coordinate(1,4), None)
    assert board_controller.is_in_checkmate(Color.WHITE) is True


def test_is_in_checkmate_double_escape(board_controller: BoardController) -> None:
    board = board_controller.board
    board.set_up_pieces()
    board.set_piece(Coordinate(2,4), Rook(Color.BLACK))
    board.set_piece(Coordinate(2,2), Bishop(Color.BLACK))
    assert board_controller.is_in_checkmate(Color.WHITE) is False
    board.set_piece(Coordinate(1,3), None)
    board.set_piece(Coordinate(1,4), None)
    assert board_controller.is_in_checkmate(Color.WHITE) is True
    board.set_piece(Coordinate(1,5), None)
    assert board_controller.is_in_checkmate(Color.WHITE) is False