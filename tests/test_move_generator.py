from pytest import fixture

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_generator import MoveGenerator
from models.piece import Bishop, Knight, Pawn, Rook


@fixture
def board() -> Board:
    return Board()


def test_generate_pawn_moves_forward_one(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1, 1), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2, 1), Pawn(Color.BLACK))
    board.set_piece(Coordinate(6, 6), Pawn(Color.WHITE))
    board.set_piece(Coordinate(7, 7), Pawn(Color.WHITE))
    assert set(MoveGenerator.generate_white_pawn_moves(board)) == set(
        [
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(1, 0)),
            Move(Color.WHITE, Coordinate(6, 6), Coordinate(7, 6)),
        ]
    )


def test_generate_knight_moves(board: Board) -> None:
    board.set_piece(Coordinate(7, 0), Knight(Color.WHITE))
    board.set_piece(Coordinate(7, 7), Knight(Color.WHITE))
    board.set_piece(Coordinate(0, 7), Knight(Color.WHITE))
    board.set_piece(Coordinate(0, 0), Knight(Color.WHITE))
    board.set_piece(Coordinate(3, 3), Knight(Color.WHITE))
    board.set_piece(Coordinate(4, 5), Pawn(Color.WHITE))
    board.set_piece(Coordinate(5, 1), Pawn(Color.BLACK))
    assert set(MoveGenerator.generate_white_knight_moves(board)) == set(
        [
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(5, 1)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(6, 2)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(6, 5)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(5, 6)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(1, 5)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(2, 6)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(2, 1)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(1, 2)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 2)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 4)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 5)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(1, 4)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(1, 2)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 1)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 1)),
        ]
    )


def test_generate_diagonal_moves(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), Bishop(Color.WHITE))
    board.set_piece(Coordinate(7, 0), Bishop(Color.WHITE))
    board.set_piece(Coordinate(7, 7), Bishop(Color.WHITE))
    board.set_piece(Coordinate(0, 7), Bishop(Color.WHITE))
    board.set_piece(Coordinate(3, 3), Bishop(Color.WHITE))
    board.set_piece(Coordinate(4, 2), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2, 4), Pawn(Color.BLACK))
    assert set(MoveGenerator.generate_white_bishop_moves(board)) == set(
        [
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(1, 1)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(2, 2)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(6, 1)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(5, 2)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(4, 3)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(3, 4)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(2, 5)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(1, 6)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(6, 6)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(5, 5)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(4, 4)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(4, 4)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(1, 6)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(2, 5)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(3, 4)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(4, 3)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(5, 2)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(6, 1)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 4)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 2)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(1, 1)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 4)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 5)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(6, 6)),
        ]
    )


def test_generate_horizontal_moves(board: Board) -> None:
    board.set_piece(Coordinate(0, 0), Rook(Color.WHITE))
    board.set_piece(Coordinate(7, 0), Rook(Color.WHITE))
    board.set_piece(Coordinate(7, 7), Rook(Color.WHITE))
    board.set_piece(Coordinate(0, 7), Rook(Color.WHITE))
    board.set_piece(Coordinate(3, 3), Rook(Color.WHITE))
    board.set_piece(Coordinate(4, 3), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2, 3), Pawn(Color.BLACK))
    assert set(MoveGenerator.generate_white_rook_moves(board)) == set(
        [
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 1)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 2)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 3)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 4)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 5)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(0, 6)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(1, 0)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(2, 0)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(3, 0)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(4, 0)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(5, 0)),
            Move(Color.WHITE, Coordinate(0, 0), Coordinate(6, 0)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(7, 1)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(7, 2)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(7, 3)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(7, 4)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(7, 5)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(7, 6)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(6, 0)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(5, 0)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(4, 0)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(3, 0)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(2, 0)),
            Move(Color.WHITE, Coordinate(7, 0), Coordinate(1, 0)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(7, 6)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(7, 5)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(7, 4)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(7, 3)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(7, 2)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(7, 1)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(6, 7)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(5, 7)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(4, 7)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(3, 7)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(2, 7)),
            Move(Color.WHITE, Coordinate(7, 7), Coordinate(1, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(1, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(2, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(3, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(4, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(5, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(6, 7)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(0, 6)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(0, 5)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(0, 4)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(0, 3)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(0, 2)),
            Move(Color.WHITE, Coordinate(0, 7), Coordinate(0, 1)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 3)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 0)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 1)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 2)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 4)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 5)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 6)),
            Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 7)),
        ]
    )
