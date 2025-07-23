from unittest import TestCase, main

from enums import Color
from game import Game
from piece import Pawn


class TestMove(TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_move_no_piece(self) -> None:
        self.assertEqual(self.game.move(Color.WHITE, 2, 0, 3, 0), False)

    def test_move_piece_on_top_same_color(self) -> None:
        self.game._board._squares[2][0] = Pawn(Color.WHITE)
        self.assertEqual(self.game.move(Color.WHITE, 1, 0, 2, 0), False)

    def test_move_wrong_color_piece(self) -> None:
        self.assertEqual(self.game.move(Color.BLACK, 1, 0, 2, 0), False)

    def test_move_pawn_forward_one(self) -> None:
        self.assertEqual(self.game.move(Color.WHITE, 1, 0, 2, 0), True)

    def test_move_pawn_forward_one_on_top(self) -> None:
        self.game._board._squares[2][0] = Pawn(Color.BLACK)
        self.assertEqual(self.game.move(Color.WHITE, 1, 0, 2, 0), False)

    def test_move_pawn_forward_two(self) -> None:
        self.assertEqual(self.game.move(Color.WHITE, 1, 0, 3, 0), True)
        self.assertEqual(self.game.move(Color.WHITE, 3, 0, 5, 0), False)

    def test_move_pawn_forward_two_on_top(self) -> None:
        self.game._board._squares[2][0] = Pawn(Color.BLACK)
        self.assertEqual(self.game.move(Color.WHITE, 1, 0, 3, 0), False)

    def test_move_pawn_forward_two_blocked(self) -> None:
        self.game._board._squares[2][0] = Pawn(Color.WHITE)
        self.assertEqual(self.game.move(Color.WHITE, 1, 0, 3, 0), False)


if __name__ == "__main__":
    main()
