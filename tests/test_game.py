from unittest import TestCase, main

from enums import Color
from game import Game
from piece import Pawn


class TestMove(TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_move_no_piece(self) -> None:
        self.assertFalse(self.game.move(Color.WHITE, 2, 0, 3, 0))

    def test_move_piece_on_top_same_color(self) -> None:
        self.game._board.set_piece(2, 0, Pawn(Color.WHITE))
        self.assertFalse(self.game.move(Color.WHITE, 1, 0, 2, 0))

    def test_move_wrong_color_piece(self) -> None:
        self.assertFalse(self.game.move(Color.BLACK, 1, 0, 2, 0))


if __name__ == "__main__":
    main()
