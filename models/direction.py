from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Direction:
    row_delta: int
    column_delta: int
