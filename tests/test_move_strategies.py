from pytest import fixture

from enums.color import Color
from models.board import BitBoard, Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
)
from models.pieces import Bishop, King, Knight, Pawn, Queen, Rook


@fixture
def board() -> Board:
    return BitBoard()


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
    board.set_piece(Coordinate(2,5), Bishop(Color.WHITE))
    assert BishopMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(4,2), Bishop(Color.WHITE))
    board.set_piece(Coordinate(4,4), Pawn(Color.WHITE))
    assert BishopMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(4,2)]
    board.set_piece(Coordinate(2,2), Bishop(Color.BLACK))
    board.set_piece(Coordinate(2,4), Pawn(Color.BLACK))
    assert BishopMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(2,2)]

def test_rook_get_attacker_coordinates(board: Board) -> None:
    assert RookMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(2,4), Rook(Color.WHITE))
    board.set_piece(Coordinate(2,5), Rook(Color.WHITE))
    assert RookMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(4,3), Rook(Color.WHITE))
    board.set_piece(Coordinate(3,4), Pawn(Color.WHITE))
    assert RookMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(4,3)]
    board.set_piece(Coordinate(3,2), Rook(Color.BLACK))
    board.set_piece(Coordinate(2,3), Pawn(Color.BLACK))
    assert RookMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(3,2)]

def test_queen_get_attacker_coordinates(board: Board) -> None:
    assert QueenMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(2,5), Queen(Color.WHITE))
    assert QueenMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(3,4), Queen(Color.WHITE))
    board.set_piece(Coordinate(4,3), Queen(Color.WHITE))
    assert QueenMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(3, 4),Coordinate(4,3)]
    board.set_piece(Coordinate(2,3), Queen(Color.BLACK))
    board.set_piece(Coordinate(3,2), Queen(Color.BLACK))
    assert QueenMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(3,2),Coordinate(2,3)]

def test_king_get_attacker_coordinates(board: Board) -> None:
    assert KingMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(2,5), King(Color.WHITE))
    assert KingMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(3,4), King(Color.WHITE))
    board.set_piece(Coordinate(2,4), King(Color.WHITE))
    board.set_piece(Coordinate(2,3), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2,2), Pawn(Color.WHITE))
    assert KingMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(3, 4),Coordinate(2,4)]
    board.set_piece(Coordinate(3,2), King(Color.BLACK))
    board.set_piece(Coordinate(4,2), King(Color.BLACK))
    board.set_piece(Coordinate(4,3), Pawn(Color.BLACK))
    board.set_piece(Coordinate(4,4), Pawn(Color.BLACK))
    assert KingMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(3,2),Coordinate(4,2)]

def test_knight_get_attacker_coordinates(board: Board) -> None:
    assert KnightMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(4,2), Knight(Color.WHITE))
    board.set_piece(Coordinate(4,3), Knight(Color.WHITE))
    board.set_piece(Coordinate(4,4), Knight(Color.WHITE))
    board.set_piece(Coordinate(3,4), Knight(Color.WHITE))
    board.set_piece(Coordinate(2,4), Knight(Color.WHITE))
    board.set_piece(Coordinate(2,3), Knight(Color.WHITE))
    board.set_piece(Coordinate(2,2), Knight(Color.WHITE))
    board.set_piece(Coordinate(3,2), Knight(Color.WHITE))
    assert KnightMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(5,4), Knight(Color.WHITE))
    board.set_piece(Coordinate(4,5), Knight(Color.WHITE))
    assert KnightMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(4,5),Coordinate(5,4)]
    board.set_piece(Coordinate(5,2), Knight(Color.BLACK))
    board.set_piece(Coordinate(4,1), Knight(Color.BLACK))
    assert KnightMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(4,1),Coordinate(5,2)]

def test_pawn_get_attacker_coordinates(board: Board) -> None:
    assert PawnMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(2,5), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1,5), Pawn(Color.WHITE))
    board.set_piece(Coordinate(3,4), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(2,2), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2,3), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2,4), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1,3), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_attacker_coordinates(Color.WHITE,Coordinate(3,3), board) == [Coordinate(2,2),Coordinate(2,4)]
    board.set_piece(Coordinate(4,2), Pawn(Color.BLACK))
    board.set_piece(Coordinate(4,3), Pawn(Color.BLACK))
    board.set_piece(Coordinate(4,4), Pawn(Color.BLACK))
    board.set_piece(Coordinate(5,3), Pawn(Color.BLACK))
    assert PawnMoveStrategy.get_attacker_coordinates(Color.BLACK,Coordinate(3,3), board) == [Coordinate(4,2),Coordinate(4,4)]

def test_pawn_get_blocker_coordinates(board: Board) -> None:
    assert PawnMoveStrategy.get_blocker_coordinate(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(2,5), Pawn(Color.WHITE))
    board.set_piece(Coordinate(1,5), Pawn(Color.WHITE))
    board.set_piece(Coordinate(3,4), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2,2), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2,4), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_blocker_coordinate(Color.WHITE,Coordinate(3,3), board) == []
    board.set_piece(Coordinate(1,3), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_blocker_coordinate(Color.WHITE,Coordinate(3,3), board) == [Coordinate(1,3)]
    board.set_piece(Coordinate(2,3), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_blocker_coordinate(Color.WHITE,Coordinate(3,3), board) == [Coordinate(2,3)]
    board.set_piece(Coordinate(5,3), Pawn(Color.BLACK))
    assert PawnMoveStrategy.get_blocker_coordinate(Color.BLACK,Coordinate(3,3), board) == [Coordinate(5,3)]
    board.set_piece(Coordinate(4,3), Pawn(Color.BLACK))
    assert PawnMoveStrategy.get_blocker_coordinate(Color.BLACK,Coordinate(3,3), board) == [Coordinate(4,3)]

def test_pawn_get_candidate_moves(board: Board) -> None:
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(-1,-1), board) == []
    board.set_piece(Coordinate(3,3), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), Pawn(Color.WHITE), None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,3), Pawn(Color.WHITE), None),
    ]
    board.set_piece(Coordinate(3,3), Pawn(Color.WHITE, True))
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), Pawn(Color.WHITE, True), None),
    ]
    board.set_piece(Coordinate(3,3), Pawn(Color.WHITE))
    board.set_piece(Coordinate(5,3), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), Pawn(Color.WHITE), None),
    ]
    board.set_piece(Coordinate(4,3), Pawn(Color.BLACK))
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == []
    board.set_piece(Coordinate(5,3), None)
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == []
    board.set_piece(Coordinate(6,0), Pawn(Color.WHITE))
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(6,0), board) == [
        Move(Color.WHITE, Coordinate(6,0), Coordinate(7,0), Pawn(Color.WHITE), None)
    ]
    board.set_piece(Coordinate(4,2), Pawn(Color.WHITE))
    board.set_piece(Coordinate(4,4), Pawn(Color.BLACK))
    assert PawnMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), Pawn(Color.WHITE), Pawn(Color.BLACK))
    ]
    
def test_knight_get_candidate_moves(board: Board) -> None:
    assert KnightMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(-1,-1), board) == []
    assert KnightMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,2), None, None),
    ]
    board.set_piece(Coordinate(4,5), Pawn(Color.WHITE))
    board.set_piece(Coordinate(4,1), Pawn(Color.BLACK))
    assert KnightMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,1), None, Pawn(Color.BLACK)),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,2), None, None),
    ]
    assert KnightMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(0,0), board) == [
        Move(Color.WHITE, Coordinate(0,0), Coordinate(1,2), None, None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(2,1), None, None)
    ]

def test_king_get_candidate_moves(board: Board) -> None:
    assert KingMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(-1,-1), board) == []
    assert KingMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,2), None, None),
    ]
    board.set_piece(Coordinate(3,4), Pawn(Color.WHITE))
    board.set_piece(Coordinate(3,2), Pawn(Color.BLACK))
    assert KingMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,2), None, Pawn(Color.BLACK)),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,2), None, None),
    ]
    assert KingMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(0,0), board) == [
        Move(Color.WHITE, Coordinate(0,0), Coordinate(0,1), None, None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(1,0), None, None),
        Move(Color.WHITE, Coordinate(0,0), Coordinate(1,1), None, None),
    ]

def test_bishop_get_candidate_moves(board: Board) -> None:
    assert BishopMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(-1,-1), board) == []
    assert BishopMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(7,7), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,0), None, None),
    ]
    board.set_piece(Coordinate(4,4), Pawn(Color.WHITE))
    board.set_piece(Coordinate(2,4), Pawn(Color.BLACK))
    assert BishopMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,4), None, Pawn(Color.BLACK)),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,0), None, None),
    ]

def test_rook_get_candidate_moves(board: Board) -> None:
    assert RookMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(-1,-1), board) == []
    assert RookMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,7), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(7,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,3), None, None),
    ]
    board.set_piece(Coordinate(4,3), Pawn(Color.WHITE))
    board.set_piece(Coordinate(3,4), Pawn(Color.BLACK))
    assert RookMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,4), None, Pawn(Color.BLACK)),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,3), None, None),
    ]

def test_queen_get_candidate_moves(board: Board) -> None:
    assert QueenMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(-1,-1), board) == []
    assert QueenMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,7), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(7,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(7,7), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,0), None, None),
    ]
    board.set_piece(Coordinate(3,4), Pawn(Color.WHITE))
    board.set_piece(Coordinate(4,4), Pawn(Color.BLACK))
    assert QueenMoveStrategy.get_candidate_moves(Color.WHITE, Coordinate(3,3), board) == [
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(3,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(7,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,3), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,4), None, Pawn(Color.BLACK)),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(4,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(5,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(6,0), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,4), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,5), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,6), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(2,2), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(1,1), None, None),
        Move(Color.WHITE, Coordinate(3,3), Coordinate(0,0), None, None),
    ]