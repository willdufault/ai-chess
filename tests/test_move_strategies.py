from unittest import TestCase, main

from enums import Color
from models.board import DIAGONAL_DIRECTIONS, ORTHOGONAL_DIRECTIONS, Board
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

    def test_move_pawn_forward_one(self) -> None:
        self.assertTrue(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(2, 0), self.board
            )
        )

    def test_move_pawn_forward_one_on_top(self) -> None:
        self.board.set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.board.set_piece(Coordinate(2, 1), Pawn(Color.BLACK))
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

    def test_move_pawn_forward_two(self) -> None:
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

    def test_move_pawn_forward_two_on_top(self) -> None:
        self.board.set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.board.set_piece(Coordinate(2, 1), Pawn(Color.BLACK))
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

    def test_move_pawn_forward_two_blocked(self) -> None:
        self.board.set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(3, 0), self.board
            )
        )

    def test_move_pawn_diagonal_one(self) -> None:
        self.assertFalse(
            self.move_strategy.is_valid_move(
                Color.WHITE, Coordinate(1, 0), Coordinate(2, 1), self.board
            )
        )

    def test_pawn_capture(self) -> None:
        self.board.set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.board.set_piece(Coordinate(2, 2), Pawn(Color.BLACK))
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

    def test_pawn_capture_forward_two(self) -> None:
        self.board.set_piece(Coordinate(3, 0), Pawn(Color.WHITE))
        self.board.set_piece(Coordinate(3, 2), Pawn(Color.BLACK))
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
        self.assertEqual(self.move_strategy.get_row_delta(Color.WHITE), 1)
        self.assertEqual(self.move_strategy.get_row_delta(Color.BLACK), -1)


class TestKnightMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = KnightMoveStrategy()
        self.move_patterns = KnightMoveStrategy.MOVE_PATTERNS

    def test_move_knight_valid(self) -> None:
        for move_pattern in self.move_patterns:
            row_delta = move_pattern.row_delta
            col_delta = move_pattern.col_delta
            with self.subTest(row_delta=row_delta, col_delta=col_delta):
                self.assertTrue(
                    self.move_strategy.is_valid_move(
                        Color.WHITE,
                        Coordinate(4, 4),
                        Coordinate(4 + row_delta, 4 + col_delta),
                        self.board,
                    ),
                )

    def test_move_knight_invalid(self) -> None:
        to_coords = (
            Coordinate(4, 2),
            Coordinate(4, 3),
            Coordinate(5, 3),
            Coordinate(4, 4),
            Coordinate(6, 6),
        )
        for to_coord in to_coords:
            with self.subTest(to_coord=to_coord):
                self.assertFalse(
                    self.move_strategy.is_valid_move(
                        Color.WHITE, Coordinate(3, 3), to_coord, self.board
                    )
                )


class TestBishopMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = BishopMoveStrategy()
        self.directions = DIAGONAL_DIRECTIONS

    def test_move_bishop_valid(self) -> None:
        for direction in self.directions:
            row_delta = direction.row_delta
            col_delta = direction.col_delta
            for distance in (1, 2):
                with self.subTest(
                    row_delta=row_delta, col_delta=col_delta, distance=distance
                ):
                    self.assertTrue(
                        self.move_strategy.is_valid_move(
                            Color.WHITE,
                            Coordinate(4, 4),
                            Coordinate(
                                4 + distance * row_delta, 4 + distance * col_delta
                            ),
                            self.board,
                        ),
                    )

    def test_move_bishop_invalid(self) -> None:
        to_coords = (
            Coordinate(3, 4),
            Coordinate(4, 3),
            Coordinate(5, 3),
            Coordinate(5, 4),
        )
        for to_coord in to_coords:
            with self.subTest(to_coord=to_coord):
                self.assertFalse(
                    self.move_strategy.is_valid_move(
                        Color.WHITE, Coordinate(3, 3), to_coord, self.board
                    )
                )


class TestRookMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = RookMoveStrategy()
        self.directions = ORTHOGONAL_DIRECTIONS

    def test_move_rook_valid(self) -> None:
        for direction in self.directions:
            row_delta = direction.row_delta
            col_delta = direction.col_delta
            for distance in (1, 2):
                with self.subTest(
                    row_delta=row_delta, col_delta=col_delta, distance=distance
                ):
                    self.assertTrue(
                        self.move_strategy.is_valid_move(
                            Color.WHITE,
                            Coordinate(4, 4),
                            Coordinate(
                                4 + distance * row_delta, 4 + distance * col_delta
                            ),
                            self.board,
                        ),
                    )

    def test_move_rook_invalid(self) -> None:
        to_coords = (
            Coordinate(4, 4),
            Coordinate(4, 5),
            Coordinate(5, 5),
            Coordinate(2, 1),
        )
        for to_coord in to_coords:
            with self.subTest(to_coord=to_coord):
                self.assertFalse(
                    self.move_strategy.is_valid_move(
                        Color.WHITE, Coordinate(3, 3), to_coord, self.board
                    )
                )


class TestQueenMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = QueenMoveStrategy()
        self.directions = ORTHOGONAL_DIRECTIONS + DIAGONAL_DIRECTIONS

    def test_move_queen_valid(self) -> None:
        for direction in self.directions:
            row_delta = direction.row_delta
            col_delta = direction.col_delta
            for distance in (1, 2):
                with self.subTest(
                    row_delta=row_delta, col_delta=col_delta, distance=distance
                ):
                    self.assertTrue(
                        self.move_strategy.is_valid_move(
                            Color.WHITE,
                            Coordinate(4, 4),
                            Coordinate(
                                4 + distance * row_delta, 4 + distance * col_delta
                            ),
                            self.board,
                        ),
                    )

    def test_move_queen_invalid(self) -> None:
        to_coords = (
            Coordinate(4, 5),
            Coordinate(5, 4),
            Coordinate(5, 6),
            Coordinate(4, 1),
        )
        for to_coord in to_coords:
            with self.subTest(to_coord=to_coord):
                self.assertFalse(
                    self.move_strategy.is_valid_move(
                        Color.WHITE, Coordinate(3, 3), to_coord, self.board
                    )
                )


class TestKingMoveStrategy(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move_strategy = KingMoveStrategy()
        self.move_patterns = KingMoveStrategy.MOVE_PATTERNS

    def test_move_king_valid(self) -> None:
        for move_pattern in self.move_patterns:
            row_delta = move_pattern.row_delta
            col_delta = move_pattern.col_delta
            with self.subTest(row_delta=row_delta, col_delta=col_delta):
                self.assertTrue(
                    self.move_strategy.is_valid_move(
                        Color.WHITE,
                        Coordinate(4, 4),
                        Coordinate(4 + row_delta, 4 + col_delta),
                        self.board,
                    ),
                )

    def test_move_king_invalid(self) -> None:
        to_coords = (
            Coordinate(4, 5),
            Coordinate(5, 4),
            Coordinate(5, 5),
            Coordinate(5, 3),
        )
        for to_coord in to_coords:
            with self.subTest(to_coord=to_coord):
                self.assertFalse(
                    self.move_strategy.is_valid_move(
                        Color.WHITE, Coordinate(3, 3), to_coord, self.board
                    )
                )


if __name__ == "__main__":
    main()
