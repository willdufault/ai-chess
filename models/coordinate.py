from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coordinate:
    row_index: int
    column_index: int
