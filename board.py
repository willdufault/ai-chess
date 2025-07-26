from constants import KNIGHT_MOVE_PATTERNS
from enums import Color
from pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
PAWN_ROW_IDX = 1
KING_COL_IDX = 4


class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._white_king_coords = (0, KING_COL_IDX)
        self._black_king_coords = (BOARD_SIZE - 1, KING_COL_IDX)

        # TODO: for castling, false once castle or king/rook moved
        self._can_white_short_castle = True
        self._can_white_long_castle = True
        self._can_black_short_castle = True
        self._can_black_long_castle = True

        self._set_up_pieces()

    def draw(self, color: Color) -> None:
        """Draw the board and rotate the perspective based on the color."""
        rows = ["  ┌───┬───┬───┬───┬───┬───┬───┬───┐"]

        if color is Color.WHITE:
            row_idxs = tuple(reversed(range(BOARD_SIZE)))
            col_idxs = range(BOARD_SIZE)
        else:
            # col_idxs is a tuple so inner loop doesn't exhaust iterator.
            row_idxs = tuple(range(BOARD_SIZE))
            col_idxs = tuple(reversed(range(BOARD_SIZE)))

        for row_idx in row_idxs:
            current_row = [f"{row_idx} │"]
            for col_idx in col_idxs:
                piece = self.get_piece(row_idx, col_idx)
                symbol = " " if piece is None else piece.symbol
                current_row.append(f" {symbol} │")
            rows.append("".join(current_row))

            if row_idx != row_idxs[-1]:
                rows.append("  ├───┼───┼───┼───┼───┼───┼───┼───┤")

        rows.append("  └───┴───┴───┴───┴───┴───┴───┴───┘")
        rows.append(f"    {'   '.join(map(str, col_idxs))}")
        print("\n".join(rows))

    def get_piece(self, row_idx: int, col_idx: int) -> Piece | None:
        """Get the piece at the coordinates."""
        return (
            self._squares[row_idx][col_idx]
            if self.is_in_bounds(row_idx, col_idx)
            else None
        )

    def set_piece(self, row_idx: int, col_idx: int, piece: Piece | None) -> None:
        """Set the piece at the coordinates."""
        if not self.is_in_bounds(row_idx, col_idx):
            return

        self._squares[row_idx][col_idx] = piece

        if isinstance(piece, King):
            if piece.color is Color.WHITE:
                self._white_king_coords = (row_idx, col_idx)
            else:
                self._black_king_coords = (row_idx, col_idx)

    def is_in_bounds(self, row_idx: int, col_idx: int) -> bool:
        """Return whether the coordinates are in bounds."""
        return 0 <= row_idx < BOARD_SIZE and 0 <= col_idx < BOARD_SIZE

    def is_under_attack(self, row_idx: int, col_idx: int, color: Color) -> bool:
        """Return whether the coordinates are under attack by the color."""
        if not self.is_in_bounds(row_idx, col_idx):
            return False

        return len(self._get_attacker_coords(row_idx, col_idx, color)) > 0

    def is_in_check(self, color: Color) -> bool:
        """Return whether the color is in check."""
        king_row_idx, king_col_idx = self._get_king_coords(color)
        other_color = Color.get_other_color(color)

        return self.is_under_attack(king_row_idx, king_col_idx, other_color)

    def is_in_checkmate(self, color: Color) -> bool:
        """Return whether the color is in checkmate."""
        if not self.is_in_check(color):
            return False

        # first, if can safely move away, false
        if not self.is_king_trapped(color):
            return False

        # get coordinates of attacking pieces

        # if >1, can't block all, return true

        # second, if it can capture attacking piece
        # ...call is_under_attack on attacking piece

        # second, if can block attack, false
        # ... check if can move into any space along line

        # else true

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has no available moves."""
        king_row_idx, king_col_idx = self._get_king_coords(color)
        other_color = Color.get_other_color(color)

        for row_idx in range(king_row_idx - 1, king_row_idx + 2):
            for col_idx in range(king_col_idx - 1, king_col_idx + 2):
                if (row_idx, col_idx) == (king_row_idx, king_col_idx):
                    continue

                if not self.is_in_bounds(row_idx, col_idx):
                    continue

                piece = self.get_piece(row_idx, col_idx)
                if piece is not None:
                    continue

                if not self.is_under_attack(row_idx, col_idx, other_color):
                    return False

        return True

    def _get_king_coords(self, color: Color) -> tuple[int, int]:
        """Return the coordinates of the king of the color."""
        return (
            self._white_king_coords if color is Color.WHITE else self._black_king_coords
        )

    def _get_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinates."""
        return (
            self._get_straight_attacker_coords(row_idx, col_idx, color)
            + self._get_diagonal_attacker_coords(row_idx, col_idx, color)
            + self._get_knight_attacker_coords(row_idx, col_idx, color)
        )

    def _get_straight_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinates horizontally or vertically."""
        coords = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for row_delta, col_delta in directions:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            while 0 <= curr_row_idx < BOARD_SIZE and 0 <= curr_col_idx < BOARD_SIZE:
                piece = self.get_piece(curr_row_idx, curr_col_idx)
                if piece is not None:
                    if piece.color == color and isinstance(piece, (Rook, Queen)):
                        coords.append((curr_row_idx, curr_col_idx))

                    break

                curr_row_idx += row_delta
                curr_col_idx += col_delta
        return coords

    def _get_diagonal_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinates diagonally."""
        coords = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        pawn_row_delta = 1 if color is Color.WHITE else -1
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
                            coords.append((curr_row_idx, curr_col_idx))

                    break

                curr_row_idx += row_delta
                curr_col_idx += col_delta
        return coords

    def _get_knight_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all knights of the color attacking
        the given coordinates."""
        coords = []
        for row_delta, col_delta in KNIGHT_MOVE_PATTERNS:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            piece = self.get_piece(curr_row_idx, curr_col_idx)
            if piece is not None and piece.color == color and isinstance(piece, Knight):
                coords.append((curr_row_idx, curr_col_idx))
        return coords

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
