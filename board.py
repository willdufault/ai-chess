from enums import Color
from piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8


class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.__set_up_pieces()

    def __str__(self) -> str:
        rows = ["  ┌───┬───┬───┬───┬───┬───┬───┬───┐"]

        # Reverse rows to align matrix coordinates with chess coordinates.
        for row_index in reversed(range(BOARD_SIZE)):
            current_row = [f"{row_index + 1} │"]
            for column_index in range(BOARD_SIZE):
                piece = self.get_piece(row_index, column_index)
                symbol = " " if piece is None else piece.symbol
                current_row.append(f" {symbol} │")
            rows.append("".join(current_row))

            if row_index > 0:
                rows.append("  ├───┼───┼───┼───┼───┼───┼───┼───┤")

        rows.append("  └───┴───┴───┴───┴───┴───┴───┴───┘")
        rows.append("    a   b   c   d   e   f   g   h")
        return "\n".join(rows)

    def get_piece(self, row_index: int, column_index: int) -> Piece | None:
        """Get the piece at the coordinates."""
        return self._squares[row_index][column_index]

    def set_piece(self, row_index: int, column_index: int, piece: Piece | None) -> None:
        """Set the piece at the coordinates."""
        self._squares[row_index][column_index] = piece

    def is_in_bounds(self, row_index: int, column_index: int) -> bool:
        """Return whether the coordinates are in bounds."""
        return 0 <= row_index < BOARD_SIZE and 0 <= column_index < BOARD_SIZE

    def __set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for column_index, piece_class in enumerate(piece_order):
            self._squares[0][column_index] = piece_class(Color.WHITE)
            self._squares[-1][column_index] = piece_class(Color.BLACK)

        self._squares[1] = [Pawn(Color.WHITE) for _ in range(BOARD_SIZE)]
        self._squares[-2] = [Pawn(Color.BLACK) for _ in range(BOARD_SIZE)]
