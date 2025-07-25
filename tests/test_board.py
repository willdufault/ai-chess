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
        self.assertFalse(self.board.is_under_attack(BOARD_SIZE, 0, Color.WHITE))

    def test_is_under_attack_straight(self) -> None:
        self.board.set_piece(5, 3, Queen(Color.WHITE))
        self.assertTrue(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(4, 3, Bishop(Color.WHITE))
        self.assertFalse(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(3, 1, Rook(Color.WHITE))
        self.assertTrue(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(3, 2, Bishop(Color.WHITE))
        self.assertFalse(self.board.is_under_attack(3, 3, Color.WHITE))

    def test_is_under_attack_diagonal(self) -> None:
        self.board.set_piece(5, 1, Queen(Color.WHITE))
        self.assertTrue(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(4, 2, Rook(Color.WHITE))
        self.assertFalse(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(5, 5, Bishop(Color.WHITE))
        self.assertTrue(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(4, 4, Rook(Color.WHITE))
        self.assertFalse(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(1, 1, Pawn(Color.WHITE))
        self.assertFalse(self.board.is_under_attack(3, 3, Color.WHITE))

        self.board.set_piece(2, 2, Pawn(Color.WHITE))
        self.assertTrue(self.board.is_under_attack(3, 3, Color.WHITE))

    def test_is_king_trapped(self) -> None:
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

        self.board.set_piece(1, 4, None)
        self.assertFalse(self.board.is_king_trapped(Color.WHITE))

        self.board.set_piece(2, 3, Bishop(Color.BLACK))
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))


if __name__ == "__main__":
    main()
