from unittest import TestCase, main

from board import BOARD_SIZE, Board
from enums import Color
from pieces import Bishop, Knight, Pawn, Queen, Rook


class TestMove(TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_out_of_bounds(self) -> None:
        self.assertTrue(self.board.is_in_bounds(0, 0))
        self.assertTrue(self.board.is_in_bounds(BOARD_SIZE - 1, BOARD_SIZE - 1))
        self.assertFalse(self.board.is_in_bounds(-1, 0))
        self.assertFalse(self.board.is_in_bounds(0, BOARD_SIZE))

    def test_is_under_attack_out_of_bounds(self) -> None:
        self.assertEqual(
            self.board._get_attacker_coords(BOARD_SIZE, 0, Color.WHITE), []
        )

    def test_get_orthogonal_attacker_coords(self) -> None:
        self.board.set_piece(5, 3, Queen(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(3, 3, Color.WHITE), [(5, 3)]
        )

        self.board.set_piece(4, 3, Bishop(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(3, 3, Color.WHITE), []
        )

        self.board.set_piece(3, 1, Rook(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(3, 3, Color.WHITE), [(3, 1)]
        )

        self.board.set_piece(3, 2, Bishop(Color.WHITE))
        self.assertEqual(
            self.board._get_orthogonal_attacker_coords(3, 3, Color.WHITE), []
        )

    def test_get_diagonal_attacker_coords(self) -> None:
        self.board.set_piece(5, 1, Queen(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(3, 3, Color.WHITE), [(5, 1)]
        )

        self.board.set_piece(4, 2, Rook(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(3, 3, Color.WHITE), []
        )

        self.board.set_piece(5, 5, Bishop(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(3, 3, Color.WHITE), [(5, 5)]
        )

        self.board.set_piece(4, 4, Rook(Color.WHITE))
        self.assertEqual(
            self.board._get_diagonal_attacker_coords(3, 3, Color.WHITE), []
        )

    def test_get_knight_attacker_coords(self) -> None:
        self.assertEqual(self.board._get_knight_attacker_coords(3, 3, Color.WHITE), [])
        self.assertEqual(
            self.board._get_knight_attacker_coords(2, 2, Color.WHITE), [(0, 1)]
        )
        self.assertEqual(self.board._get_knight_attacker_coords(2, 1, Color.WHITE), [])
        self.assertEqual(
            self.board._get_knight_attacker_coords(1, 3, Color.WHITE), [(0, 1)]
        )

    def test_get_pawn_attacker_coords(self) -> None:
        self.assertEqual(self.board._get_pawn_attacker_coords(3, 3, Color.WHITE), [])
        self.assertEqual(
            self.board._get_pawn_attacker_coords(2, 3, Color.WHITE), [(1, 2), (1, 4)]
        )
        self.assertEqual(self.board._get_pawn_attacker_coords(1, 3, Color.WHITE), [])

    def test_is_king_trapped(self) -> None:
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

        self.board.set_piece(1, 4, None)
        self.assertFalse(self.board.is_king_trapped(Color.WHITE))

        self.board.set_piece(2, 3, Bishop(Color.BLACK))
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

    def test_is_in_check(self) -> None:
        self.assertFalse(self.board.is_in_check(Color.WHITE))

        self.board.set_piece(3, 4, Queen(Color.BLACK))
        self.assertFalse(self.board.is_in_check(Color.WHITE))

        self.board.set_piece(1, 4, None)
        self.assertTrue(self.board.is_in_check(Color.WHITE))

    def test_is_in_checkmate(self) -> None:
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(1, 4, Queen(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(3, 2, Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 3, Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 5, Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 6, None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(1, 4, Rook(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(3, 2, None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_block(self) -> None:
        self.board.set_piece(1, 3, None)
        self.board.set_piece(3, 1, Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(1, 2, None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 3, Bishop(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 2, None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 1, None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 5, None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_capture(self) -> None:
        self.board.set_piece(1, 5, None)
        self.board.set_piece(2, 6, Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(1, 7, None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(2, 0, Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_pin(self) -> None:
        self.board.set_piece(1, 5, None)
        self.board.set_piece(1, 6, None)
        self.board.set_piece(3, 7, Bishop(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(1, 4, Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(3, 4, Rook(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 3, None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_double_check(self) -> None:
        self.board.set_piece(1, 1, None)
        self.board.set_piece(1, 3, None)
        self.board.set_piece(1, 4, None)
        self.board.set_piece(5, 4, Rook(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(2, 2, Bishop(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board.set_piece(0, 3, None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))


if __name__ == "__main__":
    main()
