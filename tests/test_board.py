from unittest import TestCase, main

from board import BOARD_SIZE, Board


class TestMove(TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_out_of_bounds(self) -> None:
        self.assertTrue(self.board.is_in_bounds(0, 0))
        self.assertTrue(self.board.is_in_bounds(BOARD_SIZE - 1, BOARD_SIZE - 1))
        self.assertFalse(self.board.is_in_bounds(-1, 0))
        self.assertFalse(self.board.is_in_bounds(0, BOARD_SIZE))

    # def test_is_under_attack(self) -> None:
        


if __name__ == "__main__":
    main()
