class Coordinate:
    def __init__(self, row_idx: int, col_idx: int) -> None:
        self._row_idx = row_idx
        self._col_idx = col_idx

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return self.row_idx == other.row_idx and self.col_idx == other.col_idx

    @property
    def row_idx(self) -> int:
        return self._row_idx

    @property
    def col_idx(self) -> int:
        return self._col_idx
