class Coordinate:
    def __init__(self, row_index: int, column_index: int) -> None:
        self._row_index = row_index
        self._column_index = column_index

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return (
            self.row_index == other.row_index
            and self.column_index == other.column_index
        )

    def __repr__(self) -> str:
        return f"Coordinate({self.row_index}, {self.column_index})"

    def to_key(self) -> str:
        """Return an immutable version of the piece state for caching."""
        return f"{self.row_index},{self.column_index}"

    @property
    def row_index(self) -> int:
        return self._row_index

    @property
    def column_index(self) -> int:
        return self._column_index
