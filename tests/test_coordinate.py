from models.coordinate import Coordinate


def test_equal() -> None:
    assert Coordinate(0, 0) == Coordinate(0, 0)


def test_not_equal() -> None:
    assert Coordinate(0, 0) != Coordinate(1, 0)
    assert Coordinate(0, 0) != None
