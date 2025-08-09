from unittest import TestCase, main

from enums import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
)
from models.pieces import Pawn


class TestPawnMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = PawnMoveStrategy()

    def test_move_forward_one(self) -> None:
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(2, 0), self.board
            )
        )

    def test_move_forward_one_on_top(self) -> None:
        self.board._set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.board._set_piece(Coordinate(2, 1), Pawn(Color.BLACK))
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(2, 0), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 1), Coordinate(2, 1), self.board
            )
        )

    def test_move_forward_two(self) -> None:
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(3, 0), self.board
            )
        )

    def test_move_forward_two_has_moved(self) -> None:
        piece = self.board.get_piece(Coordinate(1, 0))
        piece.has_moved = True
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(3, 0), self.board
            )
        )

    def test_move_forward_two_on_top(self) -> None:
        self.board._set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.board._set_piece(Coordinate(2, 1), Pawn(Color.BLACK))
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(3, 0), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 1), Coordinate(3, 1), self.board
            )
        )

    def test_move_forward_two_blocked(self) -> None:
        self.board._set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(3, 0), self.board
            )
        )

    def test_move_diagonal_one(self) -> None:
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(2, 1), self.board
            )
        )

    def test_capture(self) -> None:
        self.board._set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.board._set_piece(Coordinate(2, 2), Pawn(Color.BLACK))
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 1), Coordinate(2, 0), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 1), Coordinate(2, 2), self.board
            )
        )

    def test_capture_forward_two(self) -> None:
        self.board._set_piece(Coordinate(3, 0), Pawn(Color.WHITE))
        self.board._set_piece(Coordinate(3, 2), Pawn(Color.BLACK))
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 1), Coordinate(3, 0), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 1), Coordinate(3, 2), self.board
            )
        )

    def test_get_row_delta(self) -> None:
        white = Color.WHITE
        black = Color.BLACK
        self.assertEqual(self.move_strategy.get_row_delta(white), black)
        self.assertEqual(self.move_strategy.get_row_delta(black), black)


class TestKnightMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = KnightMoveStrategy()

    def test_move_knight(self) -> None:
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 4), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(1, 2), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 2), self.board
            )
        )


class TestKnightMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = BishopMoveStrategy()

    def test_move_bishop(self) -> None:
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(3, 4), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(1, 1), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 4), self.board
            )
        )


class TestRookMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = RookMoveStrategy()

    def test_move_rook(self) -> None:
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(3, 6), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(2, 1), self.board
            )
        )


class TestQueenMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = QueenMoveStrategy()

    def test_move_queen(self) -> None:
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 5), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(2, 4), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 7), self.board
            )
        )


class TestKingMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = KingMoveStrategy()

    def test_move_king(self) -> None:
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 4), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 3), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(2, 3), self.board
            )
        )
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(4, 2), self.board
            )
        )
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(3, 3), Coordinate(5, 3), self.board
            )
        )


if __name__ == "__main__":
    main()
