class Direction:
    def __init__(self, row_delta: int, column_delta: int) -> None:
        self._row_delta = row_delta
        self._column_delta = column_delta

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Direction):
            return False

        return (
            self.row_delta == other.row_delta
            and self.column_delta == other.column_delta
        )

    @property
    def row_delta(self) -> int:
        return self._row_delta

    @property
    def column_delta(self) -> int:
        return self._column_delta
