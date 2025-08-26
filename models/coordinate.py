class Coordinate:
    def __init__(self, row_index: int, column_index: int) -> None:
        self._row_index = row_index
        self._column_index = column_index

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return self.row_index == other.row_index and self.column_index == other.column_index

    @property
    def row_index(self) -> int:
        return self._row_index

    @property
    def column_index(self) -> int:
        return self._column_index
