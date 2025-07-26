from unittest import TestCase, main

from board import Board
from enums import Color
from game import Game
from pieces import Pawn


class TestMove(TestCase):
    def setUp(self) -> None:
        self.game = Game(Board())

    def test_move_no_piece(self) -> None:
        self.assertFalse(self.game.move(Color.WHITE, 2, 0, 3, 0))

    def test_move_piece_on_top_same_color(self) -> None:
        self.game._board._set_piece(2, 0, Pawn(Color.WHITE))
        self.assertFalse(self.game.move(Color.WHITE, 1, 0, 2, 0))

    def test_move_wrong_color_piece(self) -> None:
        self.assertFalse(self.game.move(Color.BLACK, 1, 0, 2, 0))

    def test_is_user_input_valid(self) -> None:
        self.assertFalse(self.game.is_valid_input("00000"))
        self.assertFalse(self.game.is_valid_input("0099"))
        self.assertFalse(self.game.is_valid_input("abcd"))
        self.assertFalse(self.game.is_valid_input("0000a"))
        self.assertFalse(self.game.is_valid_input("007a"))
        self.assertTrue(self.game.is_valid_input("0000"))
        self.assertTrue(self.game.is_valid_input("0543"))
        self.assertTrue(self.game.is_valid_input("7273"))
        self.assertTrue(self.game.is_valid_input("0543"))

    def test_parse_user_input(self) -> None:
        self.assertEqual(self.game._parse_input("0000"), (0, 0, 0, 0))
        self.assertEqual(self.game._parse_input("0345"), (0, 3, 4, 5))


if __name__ == "__main__":
    main()
