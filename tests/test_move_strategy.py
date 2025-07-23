from unittest import TestCase, main

from board import BOARD_SIZE, Board
from enums import Color
from game import Game
from move_strategies import KnightMoveStrategy, PawnMoveStrategy
from piece import Pawn


class TestIsBlocked(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.pawn_move_strategy = PawnMoveStrategy()
        self.knight_move_strategy = KnightMoveStrategy()

    def test_blocked_vertical(self) -> None:
        self.assertEqual(
            self.pawn_move_strategy._is_blocked(0, 0, 1, 0, self.board), False
        )
        self.assertEqual(
            self.pawn_move_strategy._is_blocked(0, 0, 2, 0, self.board), True
        )

    def test_blocked_horizontal(self) -> None:
        self.assertEqual(
            self.pawn_move_strategy._is_blocked(0, 0, 0, 1, self.board), False
        )
        self.assertEqual(
            self.pawn_move_strategy._is_blocked(0, 0, 0, 2, self.board), True
        )

    def test_blocked_diagonal(self) -> None:
        self.assertEqual(
            self.pawn_move_strategy._is_blocked(0, 0, 1, 1, self.board), False
        )
        self.assertEqual(
            self.pawn_move_strategy._is_blocked(0, 0, 2, 2, self.board), True
        )

    def test_move_pawn_forward_one(self) -> None:
        self.assertEqual(
            self.pawn_move_strategy.is_legal_move(Color.WHITE, 1, 0, 2, 0, self.board),
            True,
        )

    def test_move_pawn_forward_one_on_top(self) -> None:
        self.board.set_piece(2, 0, Pawn(Color.BLACK))
        self.assertEqual(
            self.pawn_move_strategy.is_legal_move(Color.WHITE, 1, 0, 2, 0, self.board),
            False,
        )

    def test_move_pawn_forward_two(self) -> None:
        self.assertEqual(
            self.pawn_move_strategy.is_legal_move(Color.WHITE, 1, 0, 3, 0, self.board),
            True,
        )
        piece = self.board.get_piece(1, 0)
        piece.has_moved = True
        self.assertEqual(
            self.pawn_move_strategy.is_legal_move(Color.WHITE, 1, 0, 3, 0, self.board),
            False,
        )

    def test_move_pawn_forward_two_on_top(self) -> None:
        self.board.set_piece(2, 0, Pawn(Color.BLACK))
        self.assertEqual(
            self.pawn_move_strategy.is_legal_move(Color.WHITE, 1, 0, 3, 0, self.board),
            False,
        )

    def test_move_pawn_forward_two_blocked(self) -> None:
        self.board.set_piece(2, 0, Pawn(Color.WHITE))
        self.assertEqual(
            self.pawn_move_strategy.is_legal_move(Color.WHITE, 1, 0, 3, 0, self.board),
            False,
        )

    def test_move_knight(self) -> None:
        self.assertEqual(
            self.knight_move_strategy.is_legal_move(
                Color.WHITE, 0, 1, 2, 1, self.board
            ),
            False,
        )
        self.assertEqual(
            self.knight_move_strategy.is_legal_move(
                Color.WHITE, 0, 1, 2, 2, self.board
            ),
            True,
        )
        self.assertEqual(
            self.knight_move_strategy.is_legal_move(
                Color.WHITE, 2, 2, 3, 4, self.board
            ),
            True,
        )
        self.assertEqual(
            self.knight_move_strategy.is_legal_move(
                Color.WHITE, 3, 4, 2, 6, self.board
            ),
            True,
        )


if __name__ == "__main__":
    main()
