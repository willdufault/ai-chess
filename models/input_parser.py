from .coordinate import Coordinate


class InputParser:
    @staticmethod
    def parse_input(move_input: str) -> tuple[Coordinate, Coordinate]:
        """Return the from and to coordinates from the valid input."""
        from_row_index, from_column_index, to_row_index, to_column_index = tuple(map(int, move_input))
        from_coordinate = Coordinate(from_row_index, from_column_index)
        to_coordinate = Coordinate(to_row_index, to_column_index)
        return from_coordinate, to_coordinate
