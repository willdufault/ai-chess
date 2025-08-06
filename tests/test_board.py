from unittest import TestCase, main

from enums import Color
from models.board import BOARD_SIZE, Board
from models.coordinate import Coordinate
from models.pieces import Bishop, Knight, Pawn, Queen, Rook


# TODO: this is not all testmove, fix for all test cases
class TestMove(TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_out_of_bounds(self) -> None:
        self.assertTrue(self.board.is_in_bounds(Coordinate(0, 0)))
        self.assertTrue(
            self.board.is_in_bounds(Coordinate(BOARD_SIZE - 1, BOARD_SIZE - 1))
        )
        self.assertFalse(self.board.is_in_bounds(Coordinate(-1, 0)))
        self.assertFalse(self.board.is_in_bounds(Coordinate(0, BOARD_SIZE)))

    def test_blocked_vertical(self) -> None:
        self.assertFalse(self.board.is_blocked(Coordinate(0, 0), Coordinate(1, 0)))
        self.assertTrue(self.board.is_blocked(Coordinate(0, 0), Coordinate(2, 0)))

    def test_blocked_horizontal(self) -> None:
        self.assertFalse(self.board.is_blocked(Coordinate(0, 0), Coordinate(0, 1)))
        self.assertTrue(self.board.is_blocked(Coordinate(0, 0), Coordinate(0, 2)))

    def test_blocked_diagonal(self) -> None:
        self.assertFalse(self.board.is_blocked(Coordinate(0, 0), Coordinate(1, 1)))
        self.assertTrue(self.board.is_blocked(Coordinate(0, 0), Coordinate(2, 2)))

    def test_is_attacking_out_of_bounds(self) -> None:
        self.assertEqual(
            self.board._get_attacker_coords(Color.WHITE, Coordinate(BOARD_SIZE, 0)),
            [],
        )

    def test_get_orthogonal_attacker_coords(self) -> None:
        self.board._set_piece(Coordinate(5, 3), Queen(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(Color.WHITE, Coordinate(3, 3)),
            [Coordinate(5, 3)],
        )

        self.board._set_piece(Coordinate(4, 3), Bishop(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(Color.WHITE, Coordinate(3, 3)),
            [],
        )

        self.board._set_piece(Coordinate(3, 1), Rook(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(Color.WHITE, Coordinate(3, 3)),
            [Coordinate(3, 1)],
        )

        self.board._set_piece(Coordinate(3, 2), Bishop(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(Color.WHITE, Coordinate(3, 3)),
            [],
        )

    def test_get_diagonal_attacker_coords(self) -> None:
        self.board._set_piece(Coordinate(5, 1), Queen(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(Color.WHITE, Coordinate(3, 3)),
            [Coordinate(5, 1)],
        )

        self.board._set_piece(Coordinate(4, 2), Rook(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(Color.WHITE, Coordinate(3, 3)), []
        )

        self.board._set_piece(Coordinate(5, 5), Bishop(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(Color.WHITE, Coordinate(3, 3)),
            [Coordinate(5, 5)],
        )

        self.board._set_piece(Coordinate(4, 4), Rook(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(Color.WHITE, Coordinate(3, 3)), []
        )

    def test_get_knight_attacker_coords(self) -> None:
        self.assertEqual(
            self.board._get_knight_attacker_coords(Color.WHITE, Coordinate(3, 3)), []
        )
        self.assertEqual(
            self.board._get_knight_attacker_coords(Color.WHITE, Coordinate(2, 2)),
            [Coordinate(0, 1)],
        )
        self.assertEqual(
            self.board._get_knight_attacker_coords(Color.WHITE, Coordinate(2, 1)), []
        )
        self.assertEqual(
            self.board._get_knight_attacker_coords(Color.WHITE, Coordinate(1, 3)),
            [Coordinate(0, 1)],
        )

    def test_get_pawn_attacker_coords(self) -> None:
        self.assertEqual(
            self.board._get_pawn_attacker_coords(Color.WHITE, Coordinate(3, 3)), []
        )
        self.assertEqual(
            self.board._get_pawn_attacker_coords(Color.WHITE, Coordinate(2, 3)),
            [Coordinate(1, 2), Coordinate(1, 4)],
        )
        self.assertEqual(
            self.board._get_pawn_attacker_coords(Color.WHITE, Coordinate(1, 3)), []
        )

    def test_is_king_trapped(self) -> None:
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), None)
        self.assertFalse(self.board.is_king_trapped(Color.WHITE))

        self.board._set_piece(Coordinate(2, 3), Bishop(Color.BLACK))
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

    def test_is_in_check(self) -> None:
        self.assertFalse(self.board.is_in_check(Color.WHITE))

        self.board._set_piece(Coordinate(3, 4), Queen(Color.BLACK))
        self.assertFalse(self.board.is_in_check(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), None)
        self.assertTrue(self.board.is_in_check(Color.WHITE))

    def test_is_in_checkmate(self) -> None:
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), Queen(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(3, 2), Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 5), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 6), None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), Rook(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(3, 2), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_block(self) -> None:
        self.board._set_piece(Coordinate(1, 3), None)
        self.board._set_piece(Coordinate(3, 1), Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 2), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), Bishop(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 2), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 1), None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 5), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_capture(self) -> None:
        self.board._set_piece(Coordinate(1, 5), None)
        self.board._set_piece(Coordinate(2, 6), Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 7), None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(2, 0), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_pin(self) -> None:
        self.board._set_piece(Coordinate(1, 5), None)
        self.board._set_piece(Coordinate(1, 6), None)
        self.board._set_piece(Coordinate(3, 7), Bishop(Color.BLACK))
        breakpoint()
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(3, 4), Rook(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_double_check(self) -> None:
        self.board._set_piece(Coordinate(1, 1), None)
        self.board._set_piece(Coordinate(1, 3), None)
        self.board._set_piece(Coordinate(1, 4), None)
        self.board._set_piece(Coordinate(5, 4), Rook(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(2, 2), Bishop(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))


if __name__ == "__main__":
    main()
