from unittest import TestCase, main

from models.coordinate import Coordinate


class TestMove(TestCase):
    def test_equals(self) -> None:
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 1)
        coord3 = Coordinate(1, 0)
        coord4 = Coordinate(0, 0)
        self.assertTrue(coord1 == coord1)
        self.assertFalse(coord1 == coord2)
        self.assertFalse(coord1 == coord3)
        self.assertTrue(coord1 == coord4)


if __name__ == "__main__":
    main()
