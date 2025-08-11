from textwrap import dedent
from unittest import TestCase, main

from enums import Color
from models.board import Board
from models.coordinate import Coordinate
from models.game import Game
from models.pieces import Pawn


class TestGame(TestCase):
    def setUp(self) -> None:
        self.game = Game(Board())

    def test_move_no_piece(self) -> None:
        self.assertFalse(
            self.game.move(Color.WHITE, Coordinate(2, 0), Coordinate(3, 0))
        )

    def test_move_piece_on_top_same_color(self) -> None:
        self.game._board.set_piece(Coordinate(2, 0), Pawn(Color.WHITE))
        self.assertFalse(
            self.game.move(Color.WHITE, Coordinate(1, 0), Coordinate(2, 0))
        )

    def test_move_wrong_color_piece(self) -> None:
        self.assertFalse(
            self.game.move(Color.BLACK, Coordinate(1, 0), Coordinate(2, 0))
        )

    def test_is_user_input_valid(self) -> None:
        self.assertFalse(self.game._is_valid_input("00000"))
        self.assertFalse(self.game._is_valid_input("0099"))
        self.assertFalse(self.game._is_valid_input("abcd"))
        self.assertFalse(self.game._is_valid_input("0000a"))
        self.assertFalse(self.game._is_valid_input("007a"))
        self.assertTrue(self.game._is_valid_input("0000"))
        self.assertTrue(self.game._is_valid_input("0543"))
        self.assertTrue(self.game._is_valid_input("7273"))
        self.assertTrue(self.game._is_valid_input("0543"))

    def test_parse_user_input(self) -> None:
        self.assertEqual(
            self.game._parse_input("0000"), (Coordinate(0, 0), Coordinate(0, 0))
        )
        self.assertEqual(
            self.game._parse_input("0345"), (Coordinate(0, 3), Coordinate(4, 5))
        )


if __name__ == "__main__":
    main()
