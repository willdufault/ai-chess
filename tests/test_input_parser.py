from models.coordinate import Coordinate
from models.input_parser import InputParser


def test_parse_input() -> None:
    assert InputParser.parse_input("1234") == (Coordinate(1, 2), Coordinate(3, 4))
    assert InputParser.parse_input("1122") == (Coordinate(1, 1), Coordinate(2, 2))
    assert InputParser.parse_input("9999") == (Coordinate(9, 9), Coordinate(9, 9))
