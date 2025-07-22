class Move:
    """Represents a move in a chess game."""

    def __init__(
        self,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
    ) -> None:
        self.from_row_index = from_row_index
        self.from_column_index = from_column_index
        self.to_row_index = to_row_index
        self.to_column_index = to_column_index
        self.captured_piece = None
