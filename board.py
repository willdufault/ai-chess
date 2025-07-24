from constants import KNIGHT_MOVE_PATTERNS
from enums import Color
from pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
PAWN_ROW_IDX = 1


class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._set_up_pieces()

    def __str__(self) -> str:
        rows = ["  ┌───┬───┬───┬───┬───┬───┬───┬───┐"]

        # Reverse rows to align matrix coordinates with chess coordinates.
        for row_idx in reversed(range(BOARD_SIZE)):
            current_row = [f"{row_idx + 1} │"]
            for col_idx in range(BOARD_SIZE):
                piece = self.get_piece(row_idx, col_idx)
                symbol = " " if piece is None else piece.symbol
                current_row.append(f" {symbol} │")
            rows.append("".join(current_row))

            if row_idx > 0:
                rows.append("  ├───┼───┼───┼───┼───┼───┼───┼───┤")

        rows.append("  └───┴───┴───┴───┴───┴───┴───┴───┘")
        rows.append("    a   b   c   d   e   f   g   h")
        return "\n".join(rows)

    def get_piece(self, row_idx: int, col_idx: int) -> Piece | None:
        """Get the piece at the coordinates."""
        return (
            self._squares[row_idx][col_idx]
            if self.is_in_bounds(row_idx, col_idx)
            else None
        )

    def set_piece(self, row_idx: int, col_idx: int, piece: Piece | None) -> None:
        """Set the piece at the coordinates."""
        if self.is_in_bounds(row_idx, col_idx):
            self._squares[row_idx][col_idx] = piece

    def is_in_bounds(self, row_idx: int, col_idx: int) -> bool:
        """Return whether the coordinates are in bounds."""
        return 0 <= row_idx < BOARD_SIZE and 0 <= col_idx < BOARD_SIZE

    def is_under_attack(self, color: Color, row_idx: int, col_idx: int) -> bool:
        """Return whether the coordinates are under attack by the color."""
        return (
            self._is_under_straight_attack(color, row_idx, col_idx)
            or self._is_under_diagonal_attack(color, row_idx, col_idx)
            or self._is_under_knight_attack(color, row_idx, col_idx)
        )

    def _set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col_idx, piece_class in enumerate(piece_order):
            self._squares[0][col_idx] = piece_class(Color.WHITE)
            self._squares[-1][col_idx] = piece_class(Color.BLACK)

        self._squares[PAWN_ROW_IDX] = [Pawn(Color.WHITE) for _ in range(BOARD_SIZE)]
        self._squares[-1 - PAWN_ROW_IDX] = [
            Pawn(Color.BLACK) for _ in range(BOARD_SIZE)
        ]

    def _is_under_straight_attack(
        self, color: Color, row_idx: int, col_idx: int
    ) -> bool:
        """Return whether the coordinates are under attack horizontally or
        vertically by the color."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for row_delta, col_delta in directions:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            while 0 <= curr_row_idx < BOARD_SIZE and 0 <= curr_col_idx < BOARD_SIZE:
                piece = self.get_piece(curr_row_idx, curr_col_idx)
                if piece is not None:
                    if piece.color == color and isinstance(piece, (Rook, Queen)):
                        return True

                    break

                curr_row_idx += row_delta
                curr_col_idx += col_delta

        return False

    def _is_under_diagonal_attack(
        self, color: Color, row_idx: int, col_idx: int
    ) -> bool:
        """Return whether the coordinates are under attack diagonally by the color."""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        pawn_row_delta = 1 if color == Color.WHITE else -1
        for row_delta, col_delta in directions:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            while 0 <= curr_row_idx < BOARD_SIZE and 0 <= curr_col_idx < BOARD_SIZE:
                piece = self.get_piece(curr_row_idx, curr_col_idx)
                if piece is not None:
                    if piece.color == color:
                        is_under_pawn_attack = (
                            isinstance(piece, Pawn)
                            and row_idx == curr_row_idx + pawn_row_delta
                            and abs(col_idx - curr_col_idx) == 1
                        )
                        if isinstance(piece, (Bishop, Queen)) or is_under_pawn_attack:
                            return True

                    break

                curr_row_idx += row_delta
                curr_col_idx += col_delta

        return False

    def _is_under_knight_attack(self, color: Color, row_idx: int, col_idx: int) -> bool:
        """Return whether the coordinates are under attack by a knight of the color."""
        for row_delta, col_delta in KNIGHT_MOVE_PATTERNS:
            piece = self.get_piece(row_idx + row_delta, col_idx + col_delta)
            if piece is not None and piece.color == color and isinstance(piece, Knight):
                return True

        return False
