from enums import Color
from move_strategies import KingMoveStrategy, KnightMoveStrategy, PawnMoveStrategy
from pieces import Bishop, FirstMovePiece, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8


class Board:
    """Represents a chessboard."""

    # DONE
    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        king_col_idx = 4
        self._white_king_row_idx = 0
        self._white_king_col_idx = king_col_idx
        self._black_king_row_idx = BOARD_SIZE - 1
        self._black_king_col_idx = king_col_idx

        # TODO: for castling, false once castle or king/rook moved
        self._can_white_short_castle = True
        self._can_white_long_castle = True
        self._can_black_short_castle = True
        self._can_black_long_castle = True

        self._set_up_pieces()

        # DONE

    # DONE
    @staticmethod
    def is_in_bounds(row_idx: int, col_idx: int) -> bool:
        """Return whether the coordinate is in bounds."""
        is_row_in_bounds = 0 <= row_idx < BOARD_SIZE
        is_col_in_bounds = 0 <= col_idx < BOARD_SIZE
        return is_row_in_bounds and is_col_in_bounds

    # DONE
    def draw(self, color: Color) -> None:
        """Draw the board from the perspective of the color."""
        top_border = "  ┌───┬───┬───┬───┬───┬───┬───┬───┐"
        middle_border = "  ├───┼───┼───┼───┼───┼───┼───┼───┤"
        bottom_border = "  └───┴───┴───┴───┴───┴───┴───┴───┘"

        rows = [top_border]

        if color is Color.WHITE:
            row_idxs = tuple(reversed(range(BOARD_SIZE)))
            col_idxs = tuple(range(BOARD_SIZE))
        else:
            row_idxs = tuple(range(BOARD_SIZE))
            col_idxs = tuple(reversed(range(BOARD_SIZE)))

        for row_idx in row_idxs:
            curr_row = [f"{row_idx} │"]

            for col_idx in col_idxs:
                piece = self.get_piece(row_idx, col_idx)
                symbol = " " if piece is None else piece.symbol

                curr_row.append(f" {symbol} │")

            rows.append("".join(curr_row))

            if row_idx != row_idxs[-1]:
                rows.append(middle_border)

        rows.append(bottom_border)
        rows.append(f"    {'   '.join(map(str, col_idxs))}")

        print("\n".join(rows))

    # DONE
    def get_piece(self, row_idx: int, col_idx: int) -> Piece | None:
        """Get the piece at the coordinate."""
        return (
            self._squares[row_idx][col_idx]
            if Board.is_in_bounds(row_idx, col_idx)
            else None
        )

    def is_occupied(self, row_idx: int, col_idx: int) -> bool:
        """Return whether the coordinate has a piece on it."""
        if not Board.is_in_bounds(row_idx, col_idx):
            return False

        return self._squares[row_idx][col_idx] is not None

    # DONE
    def move(
        self, from_row_idx: int, from_col_idx: int, to_row_idx: int, to_col_idx: int
    ) -> Piece | None:
        """Move a piece and return the piece at the to coordinate."""
        are_coords_in_bounds = Board.is_in_bounds(
            from_row_idx, from_col_idx
        ) and Board.is_in_bounds(to_row_idx, to_col_idx)

        if not are_coords_in_bounds:
            return None

        from_piece = self.get_piece(from_row_idx, from_col_idx)
        to_piece = self.get_piece(to_row_idx, to_col_idx)

        self._set_piece(from_row_idx, from_col_idx, None)
        self._set_piece(to_row_idx, to_col_idx, from_piece)

        if isinstance(from_piece, FirstMovePiece):
            from_piece.has_moved = True

        return to_piece

    # DONE
    def undo_move(
        self,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        from_piece: Piece | None,
        to_piece: Piece | None,
        from_piece_has_moved: bool,
    ) -> Piece | None:
        """Undo a move and restore the state of both pieces."""
        are_coords_in_bounds = Board.is_in_bounds(
            from_row_idx, from_col_idx
        ) and Board.is_in_bounds(to_row_idx, to_col_idx)

        if not are_coords_in_bounds:
            return None

        self._set_piece(from_row_idx, from_col_idx, from_piece)
        self._set_piece(to_row_idx, to_col_idx, to_piece)

        if isinstance(from_piece, FirstMovePiece):
            from_piece.has_moved = from_piece_has_moved

    def is_under_attack(self, row_idx: int, col_idx: int, color: Color) -> bool:
        """Return whether the coordinate is under attack by the color."""
        if not Board.is_in_bounds(row_idx, col_idx):
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
            self._set_piece(defender_row_idx, defender_col_idx, None)
            self._set_piece(attacker_row_idx, attacker_col_idx, defender)
            is_still_in_check = self.is_in_check(color)
            self._set_piece(defender_row_idx, defender_col_idx, defender)
            self._set_piece(attacker_row_idx, attacker_col_idx, attacker)
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
            blocker_coords = self._get_blocker_coords(row_idx, col_idx, color)
            for blocker_row_idx, blocker_col_idx in blocker_coords:
                blocker = self.get_piece(blocker_row_idx, blocker_col_idx)
                self._set_piece(blocker_row_idx, blocker_col_idx, None)
                self._set_piece(row_idx, col_idx, blocker)
                is_still_in_check = self.is_in_check(color)
                self._set_piece(blocker_row_idx, blocker_col_idx, blocker)
                self._set_piece(row_idx, col_idx, None)
                if not is_still_in_check:
                    return False

        return True

    def is_blocked(
        self, from_row_idx: int, from_col_idx: int, to_row_idx: int, to_col_idx: int
    ) -> bool:
        """Return whether there is a piece between the from and to coordinates.
        Assumes horizontal, vertical, or diagonal movement."""
        row_diff = to_row_idx - from_row_idx
        col_diff = to_col_idx - from_col_idx
        step_cnt = max(abs(row_diff), abs(col_diff))

        if step_cnt == 0:
            return False

        row_delta = row_diff // step_cnt
        col_delta = col_diff // step_cnt

        for step in range(1, step_cnt):
            row_idx = from_row_idx + step * row_delta
            col_idx = from_col_idx + step * col_delta
            piece = self.get_piece(row_idx, col_idx)

            if piece is not None:
                return True

        return False

    def _get_blocker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return the coordinates of all pieces of the color that can block an
        attack by moving to the given coordinate. Assuming the square is empty."""
        return (
            self._get_orthogonal_attacker_coords(row_idx, col_idx, color)
            + self._get_diagonal_attacker_coords(row_idx, col_idx, color)
            + self._get_knight_attacker_coords(row_idx, col_idx, color)
            + self._get_king_attacker_coords(row_idx, col_idx, color)
            + self._get_pawn_blocker_coords(row_idx, col_idx, color)
        )

    def _get_pawn_blocker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return the coordinates of a pawn of the color that can block an
        attack by moving to the given coordinate. Assuming the square is empty."""
        row_direction = PawnMoveStrategy.get_row_direction(color)

        one_down_piece = self.get_piece(row_idx - row_direction, col_idx)
        if one_down_piece is not None:
            if not (isinstance(one_down_piece, Pawn) and one_down_piece.color == color):
                return []

            return [(row_idx - row_direction, col_idx)]

        two_down_piece = self.get_piece(row_idx - 2 * row_direction, col_idx)
        if not (isinstance(two_down_piece, Pawn) and two_down_piece.color == color):
            return []

        # TODO: should board know about this? abstraction/refactor needed?
        if two_down_piece.has_moved:
            return []

        return [(row_idx - 2 * row_direction, col_idx)]

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has no available moves, not
        including captures."""
        king_row_idx, king_col_idx = self._get_king_coords(color)
        opponent_color = Color.get_opposite_color(color)

        for row_idx in range(king_row_idx - 1, king_row_idx + 2):
            for col_idx in range(king_col_idx - 1, king_col_idx + 2):
                if (row_idx, col_idx) == (king_row_idx, king_col_idx):
                    continue

                if not Board.is_in_bounds(row_idx, col_idx):
                    continue

                # TODO: what if this piece is opp team attacker, it can take?
                piece = self.get_piece(row_idx, col_idx)
                if piece is not None:
                    continue

                if not self.is_under_attack(row_idx, col_idx, opponent_color):
                    return False

        return True

    def _get_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate."""
        return (
            self._get_orthogonal_attacker_coords(row_idx, col_idx, color)
            + self._get_diagonal_attacker_coords(row_idx, col_idx, color)
            + self._get_knight_attacker_coords(row_idx, col_idx, color)
            + self._get_king_attacker_coords(row_idx, col_idx, color)
            + self._get_pawn_attacker_coords(row_idx, col_idx, color)
        )

    def _get_orthogonal_attacker_coords(
        self,
        row_idx: int,
        col_idx: int,
        color: Color,
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate horizontally and vertically."""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        piece_types = [Rook, Queen]
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
        given coordinate diagonally."""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        piece_types = [Bishop, Queen]
        return self._get_straight_attacker_coords(
            row_idx, col_idx, color, directions, piece_types
        )

    def _get_straight_attacker_coords(
        self,
        row_idx: int,
        col_idx: int,
        color: Color,
        directions: list[tuple[int, int]],
        piece_types: list[type[Piece]],
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pieces of the color and types
        attacking the given coordinate in a straight line in the directions."""
        coords = []
        for row_delta, col_delta in directions:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            while 0 <= curr_row_idx < BOARD_SIZE and 0 <= curr_col_idx < BOARD_SIZE:
                piece = self.get_piece(curr_row_idx, curr_col_idx)
                if piece is not None:
                    if isinstance(piece, tuple(piece_types)) and piece.color == color:
                        coords.append((curr_row_idx, curr_col_idx))

                    break

                curr_row_idx += row_delta
                curr_col_idx += col_delta
        return coords

    def _get_knight_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all knights of the color attacking
        the given coordinate."""
        coords = []
        for row_delta, col_delta in KnightMoveStrategy.move_patterns:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta
            piece = self.get_piece(curr_row_idx, curr_col_idx)
            if isinstance(piece, Knight) and piece.color == color:
                coords.append((curr_row_idx, curr_col_idx))
        return coords

    def _get_king_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all kings of the color attacking the
        given coordinate."""
        coords = []

        for row_delta, col_delta in KingMoveStrategy.move_patterns:
            curr_row_idx = row_idx + row_delta
            curr_col_idx = col_idx + col_delta

            if not Board.is_in_bounds(curr_row_idx, curr_col_idx):
                continue

            piece = self.get_piece(curr_row_idx, curr_col_idx)
            is_same_color_king = isinstance(piece, King) and piece.color == color

            if is_same_color_king:
                coords.append((curr_row_idx, curr_col_idx))

        return coords

    # DONE
    def _get_pawn_attacker_coords(
        self, row_idx: int, col_idx: int, color: Color
    ) -> list[tuple[int, int]]:
        """Return a list of coordinates of all pawns of the color attacking the
        given coordinate."""
        coords = []
        row_direction = PawnMoveStrategy.get_row_direction(color)

        # TODO: what to do with col deltas?
        # TODO: should this be in movestrat?
        for col_delta in (-1, 1):
            curr_row_idx = row_idx - row_direction
            curr_col_idx = col_idx + col_delta

            if not Board.is_in_bounds(curr_row_idx, curr_col_idx):
                continue

            piece = self.get_piece(curr_row_idx, curr_col_idx)
            is_same_color_pawn = isinstance(piece, Pawn) and piece.color == color

            if is_same_color_pawn:
                coords.append((curr_row_idx, curr_col_idx))

        return coords

    # DONE
    def _get_king_coords(self, color: Color) -> tuple[int, int]:
        """Get the coordinate of the king of the color."""
        return (
            (self._white_king_row_idx, self._white_king_col_idx)
            if color is Color.WHITE
            else (self._black_king_row_idx, self._black_king_col_idx)
        )

    # DONE
    def _set_king_coords(self, color: Color, row_idx: int, col_idx: int) -> None:
        """Set the coordinate of the king of the color."""
        if color is Color.WHITE:
            self._white_king_row_idx = row_idx
            self._white_king_col_idx = col_idx
        else:
            self._black_king_row_idx = row_idx
            self._black_king_col_idx = col_idx

    # DONE
    def _set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        white_pawn_row_idx = 1
        black_pawn_row_idx = BOARD_SIZE - 2

        for col_idx, piece_type in enumerate(piece_order):
            self._set_piece(0, col_idx, piece_type(Color.WHITE))
            self._set_piece(BOARD_SIZE - 1, col_idx, piece_type(Color.BLACK))
            self._set_piece(white_pawn_row_idx, col_idx, Pawn(Color.WHITE))
            self._set_piece(black_pawn_row_idx, col_idx, Pawn(Color.BLACK))

    # DONE
    def _set_piece(self, row_idx: int, col_idx: int, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        if not Board.is_in_bounds(row_idx, col_idx):
            return

        self._squares[row_idx][col_idx] = piece

        if isinstance(piece, King):
            self._set_king_coords(piece.color, row_idx, col_idx)
