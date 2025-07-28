from unittest import TestCase, main

from board import Board
from enums import Color
from move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
)
from pieces import Pawn


class TestIsBlocked(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.pawn_move_strategy = PawnMoveStrategy()
        self.knight_move_strategy = KnightMoveStrategy()
        self.bishop_move_strategy = BishopMoveStrategy()
        self.rook_move_strategy = RookMoveStrategy()
        self.queen_move_strategy = QueenMoveStrategy()
        self.king_move_strategy = KingMoveStrategy()

    def test_move_pawn_forward_one(self) -> None:
        self.assertTrue(
            self.pawn_move_strategy.is_valid_move(Color.WHITE, 1, 0, 2, 0, self.board)
        )

    def test_move_pawn_forward_one_on_top(self) -> None:
        self.board._set_piece(2, 0, Pawn(Color.BLACK))
        self.assertFalse(
            self.pawn_move_strategy.is_valid_move(Color.WHITE, 1, 0, 2, 0, self.board)
        )

    def test_move_pawn_forward_two(self) -> None:
        self.assertTrue(
            self.pawn_move_strategy.is_valid_move(Color.WHITE, 1, 0, 3, 0, self.board)
        )

        piece = self.board.get_piece(1, 0)
        piece.has_moved = True
        self.assertFalse(
            self.pawn_move_strategy.is_valid_move(Color.WHITE, 1, 0, 3, 0, self.board)
        )

    def test_move_pawn_forward_two_on_top(self) -> None:
        self.board._set_piece(2, 0, Pawn(Color.BLACK))
        self.assertFalse(
            self.pawn_move_strategy.is_valid_move(Color.WHITE, 1, 0, 3, 0, self.board)
        )

    def test_move_pawn_forward_two_blocked(self) -> None:
        self.board._set_piece(2, 0, Pawn(Color.WHITE))
        self.assertFalse(
            self.pawn_move_strategy.is_valid_move(Color.WHITE, 1, 0, 3, 0, self.board)
        )

    def test_move_knight(self) -> None:
        self.assertFalse(
            self.knight_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 3, self.board)
        )
        self.assertTrue(
            self.knight_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 4, self.board)
        )
        self.assertTrue(
            self.knight_move_strategy.is_valid_move(Color.WHITE, 3, 3, 1, 2, self.board)
        )
        self.assertTrue(
            self.knight_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 2, self.board)
        )

    def test_move_bishop(self) -> None:
        self.assertFalse(
            self.bishop_move_strategy.is_valid_move(Color.WHITE, 3, 3, 3, 4, self.board)
        )
        self.assertTrue(
            self.bishop_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 4, self.board)
        )
        self.assertTrue(
            self.bishop_move_strategy.is_valid_move(Color.WHITE, 3, 3, 1, 1, self.board)
        )
        self.assertFalse(
            self.bishop_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 4, self.board)
        )

    def test_move_rook(self) -> None:
        self.assertFalse(
            self.rook_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 4, self.board)
        )
        self.assertTrue(
            self.rook_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 3, self.board)
        )
        self.assertTrue(
            self.rook_move_strategy.is_valid_move(Color.WHITE, 3, 3, 3, 6, self.board)
        )
        self.assertFalse(
            self.rook_move_strategy.is_valid_move(Color.WHITE, 3, 3, 2, 1, self.board)
        )

    def test_move_queen(self) -> None:
        self.assertTrue(
            self.queen_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 4, self.board)
        )
        self.assertTrue(
            self.queen_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 3, self.board)
        )
        self.assertTrue(
            self.queen_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 5, self.board)
        )
        self.assertTrue(
            self.queen_move_strategy.is_valid_move(Color.WHITE, 3, 3, 2, 4, self.board)
        )
        self.assertFalse(
            self.queen_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 7, self.board)
        )

    def test_move_king(self) -> None:
        self.assertTrue(
            self.king_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 4, self.board)
        )
        self.assertTrue(
            self.king_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 3, self.board)
        )
        self.assertTrue(
            self.king_move_strategy.is_valid_move(Color.WHITE, 3, 3, 2, 3, self.board)
        )
        self.assertTrue(
            self.king_move_strategy.is_valid_move(Color.WHITE, 3, 3, 4, 2, self.board)
        )
        self.assertFalse(
            self.king_move_strategy.is_valid_move(Color.WHITE, 3, 3, 5, 3, self.board)
        )


if __name__ == "__main__":
    main()
