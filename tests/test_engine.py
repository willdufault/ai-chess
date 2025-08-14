from unittest import TestCase, main

from models.board import Board
from models.coordinate import Coordinate
from models.engine import Engine


class TestEngine(TestCase):
    def setUp(self):
        self.board = Board()
        self.engine = Engine(self.board)

    def test_evaluate(self) -> None:
        self.assertEqual(self.engine.evaluate(), 0)
        self.board.set_piece(Coordinate(7, 0), None)
        self.assertEqual(self.engine.evaluate(), 5)


if __name__ == "__main__":
    main()
