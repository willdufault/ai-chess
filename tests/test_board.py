from pytest import fixture

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.pieces import Bishop, King, Knight, Pawn, Queen, Rook


@fixture
def board() -> Board:
    return Board()


def test_get_set_piece(board: Board) -> None:
    assert board.get_piece(Coordinate(0, 0)) is None
    board.set_piece(Coordinate(0, 0), Pawn(Color.WHITE))
    assert board.get_piece(Coordinate(0, 0)) == Pawn(Color.WHITE)


def test_set_up_pieces_white(board: Board) -> None:
    board.set_up_pieces()
    assert board.get_piece(Coordinate(0, 0)) == Rook(Color.WHITE)
    assert board.get_piece(Coordinate(0, 1)) == Knight(Color.WHITE)
    assert board.get_piece(Coordinate(0, 2)) == Bishop(Color.WHITE)
    assert board.get_piece(Coordinate(0, 3)) == Queen(Color.WHITE)
    assert board.get_piece(Coordinate(0, 4)) == King(Color.WHITE)
    assert board.get_piece(Coordinate(0, 5)) == Bishop(Color.WHITE)
    assert board.get_piece(Coordinate(0, 6)) == Knight(Color.WHITE)
    assert board.get_piece(Coordinate(0, 7)) == Rook(Color.WHITE)
    assert board.get_piece(Coordinate(1, 0)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 1)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 2)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 3)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 4)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 5)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 6)) == Pawn(Color.WHITE)
    assert board.get_piece(Coordinate(1, 7)) == Pawn(Color.WHITE)


def test_set_up_pieces_black(board: Board) -> None:
    board.set_up_pieces()
    assert board.get_piece(Coordinate(7, 0)) == Rook(Color.BLACK)
    assert board.get_piece(Coordinate(7, 1)) == Knight(Color.BLACK)
    assert board.get_piece(Coordinate(7, 2)) == Bishop(Color.BLACK)
    assert board.get_piece(Coordinate(7, 3)) == Queen(Color.BLACK)
    assert board.get_piece(Coordinate(7, 4)) == King(Color.BLACK)
    assert board.get_piece(Coordinate(7, 5)) == Bishop(Color.BLACK)
    assert board.get_piece(Coordinate(7, 6)) == Knight(Color.BLACK)
    assert board.get_piece(Coordinate(7, 7)) == Rook(Color.BLACK)
    assert board.get_piece(Coordinate(6, 0)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 1)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 2)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 3)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 4)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 5)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 6)) == Pawn(Color.BLACK)
    assert board.get_piece(Coordinate(6, 7)) == Pawn(Color.BLACK)


def test_get_king_coordinate(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), King(Color.WHITE))
    assert board.get_king_coordinate(Color.WHITE) == Coordinate(0, 0)
    board.set_piece(Coordinate(1, 1), King(Color.BLACK))
    assert board.get_king_coordinate(Color.BLACK) == Coordinate(1, 1)


def test_is_occupied(board: Board) -> None:
    assert board.is_occupied(Coordinate(0, 0)) is False
    board.set_piece(Coordinate(0, 0), Pawn(Color.WHITE))
    assert board.is_occupied(Coordinate(0, 0)) is True


def test_get_coordinates_between_close(board: Board) -> None:
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(3, 3)) == []
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(3, 4)) == []


def test_get_coordinates_between_far(board: Board) -> None:
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(3, 5)) == [
        Coordinate(3, 4)
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(3, 6)) == [
        Coordinate(3, 4),
        Coordinate(3, 5),
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(0, 6)) == [
        Coordinate(2, 4),
        Coordinate(1, 5),
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(0, 3)) == [
        Coordinate(2, 3),
        Coordinate(1, 3),
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(0, 0)) == [
        Coordinate(2, 2),
        Coordinate(1, 1),
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(3, 0)) == [
        Coordinate(3, 2),
        Coordinate(3, 1),
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(6, 3)) == [
        Coordinate(4, 3),
        Coordinate(5, 3),
    ]
    assert board.get_coordinates_between(Coordinate(3, 3), Coordinate(6, 6)) == [
        Coordinate(4, 4),
        Coordinate(5, 5),
    ]


def test_is_blocked(board: Board) -> None:
    assert board.is_path_blocked(Coordinate(3, 3), Coordinate(3, 3)) is False
    assert board.is_path_blocked(Coordinate(3, 3), Coordinate(3, 4)) is False
    assert board.is_path_blocked(Coordinate(3, 3), Coordinate(3, 5)) is False
    board.set_piece(Coordinate(3, 4), Pawn(Color.WHITE))
    assert board.is_path_blocked(Coordinate(3, 3), Coordinate(3, 5)) is True


def test_make_move(board: Board) -> None:
    from_coordinate = Coordinate(0, 0)
    to_coordinate = Coordinate(1, 1)
    from_piece = Pawn(Color.WHITE)
    to_piece = Pawn(Color.BLACK)
    board.set_piece(from_coordinate, from_piece)
    board.set_piece(to_coordinate, to_piece)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece
    move = Move(Color.WHITE, from_coordinate, to_coordinate, from_piece, to_piece)
    board.make_move(move)
    assert board.get_piece(from_coordinate) == None
    assert board.get_piece(to_coordinate) == from_piece
    assert from_piece.has_moved is True


def test_undo_move(board: Board) -> None:
    # TODO: this is copied from test_make_move, DRY
    from_coordinate = Coordinate(0, 0)
    to_coordinate = Coordinate(1, 1)
    from_piece = Pawn(Color.WHITE)
    to_piece = Pawn(Color.BLACK)
    board.set_piece(from_coordinate, from_piece)
    board.set_piece(to_coordinate, to_piece)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece
    move = Move(Color.WHITE, from_coordinate, to_coordinate, from_piece, to_piece)
    board.make_move(move)
    assert board.get_piece(from_coordinate) == None
    assert board.get_piece(to_coordinate) == from_piece
    assert from_piece.has_moved is True
    board.undo_move(move)
    assert board.get_piece(from_coordinate) == from_piece
    assert board.get_piece(to_coordinate) == to_piece
    assert from_piece.has_moved is False

def test_is_attacking_coordinate_out_of_bounds(board: Board) -> None:
    assert board.is_attacking(Color.WHITE, Coordinate(-1,-1)) == False
