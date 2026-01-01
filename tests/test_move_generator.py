import pytest

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_generator import MoveGenerator
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook


@pytest.fixture
def board() -> Board:
    return Board()


def test_generate_candidate_moves(board: Board) -> None:
    assert MoveGenerator.generate_candidate_moves(Color.WHITE, board) == []

    board.set_up_pieces()
    # fmt: off
    legal_moves = [
        Move.from_coordinates(Coordinate(1, 0), Coordinate(2, 0), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 1), Coordinate(2, 1), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 2), Coordinate(2, 2), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 3), Coordinate(2, 3), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 4), Coordinate(2, 4), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 5), Coordinate(2, 5), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 6), Coordinate(2, 6), Pawn(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(1, 7), Coordinate(2, 7), Pawn(Color.WHITE), None, Color.WHITE),

        Move.from_coordinates(Coordinate(0, 1), Coordinate(2, 0), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 1), Coordinate(2, 2), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 6), Coordinate(2, 5), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 6), Coordinate(2, 7), Knight(Color.WHITE), None, Color.WHITE),
    ]
    # fmt: on
    assert set(MoveGenerator.generate_candidate_moves(Color.WHITE, board)) == set(
        legal_moves
    )

    board.set_piece(None, Coordinate(1, 0))
    board.set_piece(None, Coordinate(1, 1))
    board.set_piece(None, Coordinate(1, 2))
    board.set_piece(None, Coordinate(1, 3))
    board.set_piece(None, Coordinate(1, 4))
    board.set_piece(None, Coordinate(1, 5))
    board.set_piece(None, Coordinate(1, 6))
    board.set_piece(None, Coordinate(1, 7))
    # fmt: off
    legal_moves = [
        Move.from_coordinates(Coordinate(0, 1), Coordinate(2, 0), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 1), Coordinate(2, 2), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 1), Coordinate(1, 3), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 6), Coordinate(2, 5), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 6), Coordinate(2, 7), Knight(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 6), Coordinate(1, 4), Knight(Color.WHITE), None, Color.WHITE),

        Move.from_coordinates(Coordinate(0, 2), Coordinate(1, 1), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 2), Coordinate(2, 0), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 2), Coordinate(1, 3), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 2), Coordinate(2, 4), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 2), Coordinate(3, 5), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 2), Coordinate(4, 6), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 2), Coordinate(5, 7), Bishop(Color.WHITE), None, Color.WHITE),

        Move.from_coordinates(Coordinate(0, 5), Coordinate(1, 6), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 5), Coordinate(2, 7), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 5), Coordinate(1, 4), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 5), Coordinate(2, 3), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 5), Coordinate(3, 2), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 5), Coordinate(4, 1), Bishop(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 5), Coordinate(5, 0), Bishop(Color.WHITE), None, Color.WHITE),

        Move.from_coordinates(Coordinate(0, 0), Coordinate(1, 0), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 0), Coordinate(2, 0), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 0), Coordinate(3, 0), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 0), Coordinate(4, 0), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 0), Coordinate(5, 0), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 0), Coordinate(6, 0), Rook(Color.WHITE), Pawn(Color.BLACK), Color.WHITE),

        Move.from_coordinates(Coordinate(0, 7), Coordinate(1, 7), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 7), Coordinate(2, 7), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 7), Coordinate(3, 7), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 7), Coordinate(4, 7), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 7), Coordinate(5, 7), Rook(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 7), Coordinate(6, 7), Rook(Color.WHITE), Pawn(Color.BLACK), Color.WHITE),
        
        Move.from_coordinates(Coordinate(0, 3), Coordinate(1, 2), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(2, 1), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(3, 0), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(1, 4), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(2, 5), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(3, 6), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(4, 7), Queen(Color.WHITE), None, Color.WHITE),

        Move.from_coordinates(Coordinate(0, 3), Coordinate(1, 3), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(2, 3), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(3, 3), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(4, 3), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(5, 3), Queen(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 3), Coordinate(6, 3), Queen(Color.WHITE), Pawn(Color.BLACK), Color.WHITE),

        Move.from_coordinates(Coordinate(0, 4), Coordinate(1, 3), King(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 4), Coordinate(1, 4), King(Color.WHITE), None, Color.WHITE),
        Move.from_coordinates(Coordinate(0, 4), Coordinate(1, 5), King(Color.WHITE), None, Color.WHITE),
    ]
    # fmt: on
    assert set(MoveGenerator.generate_candidate_moves(Color.WHITE, board)) == set(
        legal_moves
    )
