from unittest import TestCase, main

from board import BOARD_SIZE, Board


class TestMove(TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_out_of_bounds(self) -> None:
        self.assertEqual(self.board.is_in_bounds(0, 0), True)
        self.assertEqual(self.board.is_in_bounds(BOARD_SIZE - 1, BOARD_SIZE - 1), True)
        self.assertEqual(self.board.is_in_bounds(-1, 0), False)
        self.assertEqual(self.board.is_in_bounds(0, BOARD_SIZE), False)


if __name__ == "__main__":
    main()
