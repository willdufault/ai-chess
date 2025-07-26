from enums import Color
from move_strategies import KnightMoveStrategy
from pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
PAWN_ROW_IDX = 1
KING_COL_IDX = 4


class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # TODO: only place i use tuple for coords, make rows/cols for consistency?
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
        opponent_color = Color.get_opposite_color(color)

        return self.is_under_attack(king_row_idx, king_col_idx, opponent_color)

    def is_in_checkmate(self, color: Color) -> bool:
        """Return whether the color is in checkmate."""
        if not self.is_in_check(color):
            return False

        # first, if can safely move away, false
        if not self.is_king_trapped(color):
            return False

        # get coordinates of attacking pieces
        king_row_idx, king_col_idx = self._get_king_coords(color)
        opponent_color = Color.get_opposite_color(color)
        attacker_coords = self._get_attacker_coords(
            king_row_idx, king_col_idx, opponent_color
        )

        # if >1, can't block all, return true
        if len(attacker_coords) > 1:
            return True

        attacker_row_idx, attacker_col_idx = attacker_coords[0]
        attacker = self.get_piece(attacker_row_idx, attacker_col_idx)

        # second, if it can capture attacking piece
        # ...call is_under_attack on attacking piece
        defender_coords = self._get_attacker_coords(
            attacker_row_idx, attacker_col_idx, color
        )
        for defender_row_idx, defender_col_idx in defender_coords:
            defender = self.get_piece(defender_row_idx, defender_col_idx)
            self.set_piece(defender_row_idx, defender_col_idx, None)
            self.set_piece(attacker_row_idx, attacker_col_idx, defender)
            is_still_in_check = self.is_in_check(color)
            self.set_piece(defender_row_idx, defender_col_idx, defender)
            self.set_piece(attacker_row_idx, attacker_col_idx, attacker)
            if not is_still_in_check:
                return False

        # second, if can block attack, false
        # ... check if can move into any space along line
        # TODO: taken from movestrat, refactor DRY
        row_diff = attacker_row_idx - king_row_idx
        col_diff = attacker_col_idx - king_col_idx
        step_cnt = max(abs(row_diff), abs(col_diff))
        row_delta = row_diff // step_cnt
        col_delta = col_diff // step_cnt
        for step in range(1, step_cnt):
            row_idx = king_row_idx + step * row_delta
            col_idx = king_col_idx + step * col_delta
            # if piece is not None:
            #     return True

        return False

        # else true

    def _get_blocking_pieces(self, row_idx: int, col_idx: int, color: Color) -> bool:
        """Return the coordinates of all pieces of the color that can move to
        the given coordinates. Assuming the square is empty."""
        coords = self._get_non_pawn_attacker_coords(row_idx, col_idx, color)

        # never occupied,

        # otherwise, check if pawn below or 2 below can move (through Movestrat)

    def _can_pawn_block(self, row_idx: int, col_idx: int, color: Color) -> bool:
        """Return whether a pawn of the color can block the coordinates."""
        row_delta = 1 if color is Color.WHITE else -1
        for distance in range(1, 3):
            curr_row_idx = row_idx + distance * row_delta
            piece = self.get_piece(curr_row_idx, col_idx)
            is_legal_pawn_move = (
                isinstance(piece, Pawn)
                and piece.color == color
                and piece.move_strategy.is_legal_move(
                    color, curr_row_idx, col_idx, curr_row_idx, col_idx
                )
            )
            if is_legal_pawn_move:
                return True

        return False

        # for
        one_below_row = row_idx - 1

        one_below_piece = self.get_piece(one_below_row, col_idx)

        if isinstance(
            one_below_piece, Pawn
        ) and one_below_piece.move_strategy.is_legal_move(
            color, one_below_row, col_idx, row_idx, col_idx
        ):
            coords.append(one_below_row, col_idx)

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has no available moves, not
        including captures."""
        king_row_idx, king_col_idx = self._get_king_coords(color)
        opponent_color = Color.get_opposite_color(color)

        for row_idx in range(king_row_idx - 1, king_row_idx + 2):
            for col_idx in range(king_col_idx - 1, king_col_idx + 2):
                if (row_idx, col_idx) == (king_row_idx, king_col_idx):
                    continue

                if not self.is_in_bounds(row_idx, col_idx):
                    continue

                # TODO: what if this piece is opp team attacker, it can take?
                piece = self.get_piece(row_idx, col_idx)
                if piece is not None:
                    continue

                if not self.is_under_attack(row_idx, col_idx, opponent_color):
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
            self._get_orthogonal_attacker_coords(row_idx, col_idx, color)
            + self._get_diagonal_attacker_coords(row_idx, col_idx, color)
            + self._get_knight_attacker_coords(row_idx, col_idx, color)
            + self._get_pawn_attacker_coords(row_idx, col_idx, color)
        )

    def _get_non_pawn_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all non-pawn pieces of the color
        attacking the given coordinates."""
        return (
            self._get_orthogonal_attacker_coords(row_idx, col_idx, color)
            + self._get_diagonal_attacker_coords(row_idx, col_idx, color)
            + self._get_knight_attacker_coords(row_idx, col_idx, color)
        )

    def _get_orthogonal_attacker_coords(
        self,
        row_idx: int,
        col_idx: int,
        color: Color,
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinates horizontally and vertically."""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        piece_types = (Rook, Queen)
        return self._get_straight_attacker_coords(
            row_idx, col_idx, color, directions, piece_types
        )

    def _get_diagonal_attacker_coords(
        self,
        row_idx: int,
        col_idx: int,
        color: Color,
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinates diagonally."""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        piece_types = (Bishop, Queen)
        return self._get_straight_attacker_coords(
            row_idx, col_idx, color, directions, piece_types
        )

    def _get_straight_attacker_coords(
        self,
        row_idx: int,
        col_idx: int,
        color: Color,
        directions: list[tuple[int, int]],
        piece_types: tuple[type[Piece]],
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color and types
        attacking the given coordinates along a straight line in the directions."""
        coords = []
        for row_delta, col_delta in directions:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            while 0 <= curr_row_idx < BOARD_SIZE and 0 <= curr_col_idx < BOARD_SIZE:
                piece = self.get_piece(curr_row_idx, curr_col_idx)
                if piece is not None:
                    if isinstance(piece, piece_types) and piece.color == color:
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
        for row_delta, col_delta in KnightMoveStrategy.move_patterns:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            piece = self.get_piece(curr_row_idx, curr_col_idx)
            if isinstance(piece, Knight) and piece.color == color:
                coords.append((curr_row_idx, curr_col_idx))
        return coords

    def _get_pawn_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pawns of the color attacking the
        given coordinates."""
        coords = []
        row_delta = 1 if color is Color.WHITE else -1
        col_deltas = (-1, 1)
        for col_delta in col_deltas:
            curr_row_idx = row_idx - row_delta
            curr_col_idx = col_idx + col_delta
            if not self.is_in_bounds(curr_row_idx, curr_col_idx):
                continue

            piece = self.get_piece(curr_row_idx, curr_col_idx)
            if isinstance(piece, Pawn) and piece.color == color:
                coords.append((curr_row_idx, curr_col_idx))
        return coords

    def _set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col_idx, piece_type in enumerate(piece_order):
            self._squares[0][col_idx] = piece_type(Color.WHITE)
            self._squares[-1][col_idx] = piece_type(Color.BLACK)

        self._squares[PAWN_ROW_IDX] = [Pawn(Color.WHITE) for _ in range(BOARD_SIZE)]
        self._squares[-1 - PAWN_ROW_IDX] = [
            Pawn(Color.BLACK) for _ in range(BOARD_SIZE)
        ]
