from models.direction import Direction


def test_equal() -> None:
    assert Direction(0, 0) == Direction(0, 0)


def test_not_equal() -> None:
    assert Direction(0, 0) != Direction(1, 0)
    assert Direction(0, 0) != None
