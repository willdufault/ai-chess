from pytest import fixture

from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
    StraightMoveStrategy,
)
from models.pieces import Bishop, King, Knight, Pawn, Queen, Rook


@fixture
def board() -> Board:
    return Board()


def test_bishop_is_move_valid(board: Board) -> None:
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 3), None, None), board) is False
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 4), None, None), board) is False
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 5), None, None), board) is False
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 5), None, None), board) is False
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), None, None), board) is True
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 4), None, None), board) is True
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 2), None, None), board) is True
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 2), None, None), board) is True
    assert BishopMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(1, 5), None, None), board) is True

def test_rook_is_move_valid(board: Board) -> None:
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 3), None, None), board) is False
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), None, None), board) is False
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 5), None, None), board) is False
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 5), None, None), board) is False
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 4), None, None), board) is True
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 3), None, None), board) is True
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 2), None, None), board) is True
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is True
    assert RookMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), None, None), board) is True

def test_queen_is_move_valid(board: Board) -> None:
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 3), None, None), board) is False
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 5), None, None), board) is False
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 4), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 2), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 2), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(1, 5), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 4), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 3), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 2), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is True
    assert QueenMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), None, None), board) is True

def test_king_is_move_valid(board: Board) -> None:
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 3), None, None), board) is False
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 4), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 4), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 3), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 2), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 2), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 2), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is True
    assert KingMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), None, None), board) is True

def test_knight_is_move_valid(board: Board) -> None:
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(6, 3), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(6, 5), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(5, 6), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(3,6), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(2,5), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(2,3), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(3, 2), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(5,2), None, None), board) is True
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(5,3), None, None), board) is False
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(6,6), None, None), board) is False
    assert KnightMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(4, 4), Coordinate(4,7), None, None), board) is False

def test_pawn_is_valid_move_forward_white(board: Board) -> None:
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is True
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(2, 3), None, None), board) is False

def test_pawn_is_valid_move_forward_black(board: Board) -> None:
    assert PawnMoveStrategy.is_move_valid( Move(Color.BLACK, Coordinate(3, 3), Coordinate(2, 3), None, None), board) is True
    assert PawnMoveStrategy.is_move_valid( Move(Color.BLACK, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is False

def test_pawn_is_valid_move_illegal(board: Board) -> None:
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 3), None, None), board) is False
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 4), None, None), board) is False
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(3, 5), None, None), board) is False
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 5), None, None), board) is False

    
def test_pawn_is_valid_move_forward_one(board: Board) -> None:
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is True
    board.set_piece(Coordinate(4,3), Pawn(Color.WHITE))
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), None, None), board) is False
    
def test_pawn_is_valid_move_forward_two(board: Board) -> None:
    pawn_has_moved = Pawn(Color.WHITE)
    pawn_has_moved.has_moved = True
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), Pawn(Color.WHITE), None), board) is True
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), pawn_has_moved, None), board) is False
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), Pawn(Color.WHITE), Pawn(Color.WHITE)), board) is False
    board.set_piece(Coordinate(4,3),Pawn(Color.WHITE))
    assert PawnMoveStrategy.is_move_valid( Move(Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), Pawn(Color.WHITE), None), board) is False

def test_pawn_is_valid_capture(board: Board) -> None:
    assert PawnMoveStrategy.is_move_valid(Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None), board) is False
    assert PawnMoveStrategy.is_move_valid(Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, None), board) is False
    assert PawnMoveStrategy.is_move_valid(Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, Pawn(Color.WHITE)), board) is False
    assert PawnMoveStrategy.is_move_valid(Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, Pawn(Color.WHITE)), board) is False
    assert PawnMoveStrategy.is_move_valid(Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, Pawn(Color.BLACK)), board) is True
    assert PawnMoveStrategy.is_move_valid(Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, Pawn(Color.BLACK)), board) is True

def test_bishop_get_attacker_coordinates(board: Board) -> None:
    assert BishopMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(3,4), Bishop(Color.WHITE))
    board.set_piece(Coordinate(2,5), Rook(Color.WHITE))
    assert BishopMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(4,2), Bishop(Color.WHITE))
    board.set_piece(Coordinate(4,4), Rook(Color.WHITE))
    assert BishopMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(4,2)]
    board.set_piece(Coordinate(2,2), Bishop(Color.BLACK))
    board.set_piece(Coordinate(2,4), Rook(Color.BLACK))
    assert BishopMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(2,2)]