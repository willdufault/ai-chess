class Direction:
    def __init__(self, row_delta: int, col_delta: int) -> None:
        self._row_delta = row_delta
        self._col_delta = col_delta

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Direction):
            return False

        return self.row_delta == other.row_delta and self.col_delta == other.col_delta

    @property
    def row_delta(self) -> int:
        return self._row_delta

    @property
    def col_delta(self) -> int:
        return self._col_delta
