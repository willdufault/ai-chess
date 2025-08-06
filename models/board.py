from enums import Color

from .coordinate import Coordinate
from .direction import Direction
from .move_strategies import KingMoveStrategy, KnightMoveStrategy, PawnMoveStrategy
from .pieces import Bishop, FirstMovePiece, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
KING_COL_IDX = 4
WHITE_PAWN_ROW_IDX = 1
BLACK_PAWN_ROW_IDX = BOARD_SIZE - 2


class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        self._white_king_coord = Coordinate(0, KING_COL_IDX)
        self._black_king_coord = Coordinate(BOARD_SIZE - 1, KING_COL_IDX)

        # TODO: for castling, false once castle or king/rook moved
        self._can_white_short_castle = True
        self._can_white_long_castle = True
        self._can_black_short_castle = True
        self._can_black_long_castle = True

        self._set_up_pieces()

    @staticmethod
    def is_in_bounds(coord: Coordinate) -> bool:
        """Return whether the coordinate is in bounds."""
        is_row_in_bounds = 0 <= coord.row_idx < BOARD_SIZE
        is_col_in_bounds = 0 <= coord.col_idx < BOARD_SIZE
        return is_row_in_bounds and is_col_in_bounds

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
                coord = Coordinate(row_idx, col_idx)
                piece = self.get_piece(coord)
                symbol = " " if piece is None else piece.symbol
                curr_row.append(f" {symbol} │")
            rows.append("".join(curr_row))

            if row_idx != row_idxs[-1]:
                rows.append(middle_border)

        rows.append(bottom_border)
        rows.append(f"    {'   '.join(map(str, col_idxs))}")
        print("\n".join(rows))

    def get_piece(self, coord: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        if not Board.is_in_bounds(coord):
            return None
        return self._squares[coord.row_idx][coord.col_idx]

    def is_occupied(self, coord: Coordinate) -> bool:
        """Return whether the coordinate has a piece on it."""
        if not Board.is_in_bounds(coord):
            return False
        return self._squares[coord.row_idx][coord.col_idx] is not None

    def move(self, from_coord: Coordinate, to_coord: Coordinate) -> Piece | None:
        """Move a piece and return the piece at the to coordinate."""
        are_coords_in_bounds = Board.is_in_bounds(from_coord) and Board.is_in_bounds(
            to_coord
        )
        if not are_coords_in_bounds:
            return None

        from_piece = self.get_piece(from_coord)
        to_piece = self.get_piece(to_coord)
        self._set_piece(from_coord, None)
        self._set_piece(to_coord, from_piece)

        if isinstance(from_piece, FirstMovePiece):
            from_piece.has_moved = True

        return to_piece

    def undo_move(
        self,
        from_coord: Coordinate,
        to_coord: Coordinate,
        to_piece: Piece | None,
        from_piece_has_moved: bool,
    ) -> Piece | None:
        """Undo a move and restore the state of both pieces."""
        are_coords_in_bounds = Board.is_in_bounds(from_coord) and Board.is_in_bounds(
            to_coord
        )
        if not are_coords_in_bounds:
            return None

        from_piece = self.get_piece(to_coord)
        self._set_piece(from_coord, from_piece)
        self._set_piece(to_coord, to_piece)

        if isinstance(from_piece, FirstMovePiece):
            from_piece.has_moved = from_piece_has_moved

    def is_attacking(self, color: Color, coord: Coordinate) -> bool:
        """Return whether the color is attacking the coordinate."""
        if not Board.is_in_bounds(coord):
            return False
        return len(self._get_attacker_coords(color, coord)) > 0

    def is_in_check(self, color: Color) -> bool:
        """Return whether the color is in check."""
        king_coord = self._get_king_coord(color)
        opponent_color = Color.get_opposite_color(color)
        return self.is_attacking(opponent_color, king_coord)

    # TODO
    def is_in_checkmate(self, color: Color) -> bool:
        """Return whether the color is in checkmate."""
        if not self.is_in_check(color):
            return False

        # first, if can safely move away, false
        if not self.is_king_trapped(color):
            return False

        # get coordinates of attacking pieces
        king_coord = self._get_king_coord(color)
        king_row_idx = king_coord.row_idx
        king_col_idx = king_coord.col_idx
        opponent_color = Color.get_opposite_color(color)
        attacker_coords = self._get_attacker_coords(opponent_color, king_coord)

        # if >1, can't block all, return true
        if len(attacker_coords) > 1:
            return True

        attacker_coord = attacker_coords[0]
        attacker_row_idx = attacker_coord.row_idx
        attacker_col_idx = attacker_coord.col_idx
        attacker = self.get_piece(attacker_coord)

        # second, if it can capture attacking piece
        # ...call is_attacking on attacking piece
        defender_coords = self._get_attacker_coords(color, attacker_coord)
        for defender_coord in defender_coords:
            defender = self.get_piece(defender_coord)
            self._set_piece(defender_coord, None)
            self._set_piece(attacker_coord, defender)
            is_still_in_check = self.is_in_check(color)
            self._set_piece(defender_coord, defender)
            self._set_piece(attacker_coord, attacker)
            if not is_still_in_check:
                return False

        # TODO: PICK UP HERE, REFACTORING row,col -> coord AND reorder args so color is first

        # second, if can block attack, false
        # ... check if can move into any space along line
        # TODO: taken from movestrat, refactor DRY
        row_diff = attacker_row_idx - king_row_idx
        col_diff = attacker_col_idx - king_col_idx
        step_cnt = max(abs(row_diff), abs(col_diff))
        row_delta = row_diff // step_cnt
        col_delta = col_diff // step_cnt
        for step in range(1, step_cnt):
            curr_coord = Coordinate(
                king_row_idx + step * row_delta,
                king_col_idx + step * col_delta,
            )
            blocker_coords = self._get_blocker_coords(color, curr_coord)
            for blocker_coord in blocker_coords:
                blocker = self.get_piece(blocker_coord)
                self._set_piece(blocker_coord, None)
                self._set_piece(curr_coord, blocker)
                is_still_in_check = self.is_in_check(color)
                self._set_piece(blocker_coord, blocker)
                self._set_piece(curr_coord, None)
                if not is_still_in_check:
                    return False

        return True

    def is_blocked(self, from_coord: Coordinate, to_coord: Coordinate) -> bool:
        """Return whether there is a piece between the from and to coordinates.
        Assumes horizontal, vertical, or diagonal movement."""
        row_diff = to_coord.row_idx - from_coord.row_idx
        col_diff = to_coord.col_idx - from_coord.col_idx
        step_cnt = max(abs(row_diff), abs(col_diff))
        if step_cnt == 0:
            return False

        row_delta = row_diff // step_cnt
        col_delta = col_diff // step_cnt
        for step in range(1, step_cnt):
            curr_coord = Coordinate(
                from_coord.row_idx + step * row_delta,
                from_coord.col_idx + step * col_delta,
            )
            piece = self.get_piece(curr_coord)
            if piece is not None:
                return True

        return False

    # TODO: DO THESE MAKE SENSE IN BOARD? THIS LOGIC FEELS LIKE IT SHOULD BE IN MOVESTRAT INSTEAD

    def _get_blocker_coords(self, color: Color, coord: Coordinate) -> list[Coordinate]:
        """Return the coordinates of all pieces of the color that can block an
        attack by moving to the given coordinate. Assuming the square is empty."""
        return (
            self._get_orthogonal_attacker_coords(color, coord)
            + self._get_diagonal_attacker_coords(color, coord)
            + self._get_knight_attacker_coords(color, coord)
            + self._get_king_attacker_coords(color, coord)
            + self._get_pawn_blocker_coords(color, coord)
        )

    def _get_pawn_blocker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return the coordinates of a pawn of the color that can block an
        attack by moving to the given coordinate. Assuming the square is empty."""
        pawn_row_delta = PawnMoveStrategy.get_row_delta(color)
        row_idx = coord.row_idx
        col_idx = coord.col_idx
        one_back_coord = Coordinate(row_idx - pawn_row_delta, col_idx)
        one_back_piece = self.get_piece(one_back_coord)

        if one_back_piece is not None:
            is_one_back_same_color_pawn = (
                isinstance(one_back_piece, Pawn) and one_back_piece.color == color
            )

            if not is_one_back_same_color_pawn:
                return []

            return [one_back_coord]

        two_back_coord = Coordinate(row_idx - 2 * pawn_row_delta, col_idx)
        two_back_piece = self.get_piece(two_back_coord)
        is_two_back_same_color_pawn = (
            isinstance(two_back_piece, Pawn) and two_back_piece.color == color
        )

        # TODO: should board know about this? abstraction/refactor needed?
        if not is_two_back_same_color_pawn or two_back_piece.has_moved:
            return []

        return [two_back_coord]

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has no available moves, not
        including captures."""
        opponent_color = Color.get_opposite_color(color)
        king_coord = self._get_king_coord(color)
        king_row_idx = king_coord.row_idx
        king_col_idx = king_coord.col_idx

        for curr_row_idx in range(king_row_idx - 1, king_row_idx + 2):
            for curr_col_idx in range(king_col_idx - 1, king_col_idx + 2):
                curr_coord = Coordinate(curr_row_idx, curr_col_idx)

                if curr_coord == king_coord:
                    continue

                if not Board.is_in_bounds(curr_coord):
                    continue

                # TODO: what if this piece is opp team attacker, it can take?
                piece = self.get_piece(curr_coord)
                if piece is not None:
                    continue

                if not self.is_attacking(opponent_color, curr_coord):
                    return False

        return True

    def _get_attacker_coords(self, color: Color, coord: Coordinate) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate."""
        return (
            self._get_orthogonal_attacker_coords(color, coord)
            + self._get_diagonal_attacker_coords(color, coord)
            + self._get_knight_attacker_coords(color, coord)
            + self._get_king_attacker_coords(color, coord)
            + self._get_pawn_attacker_coords(color, coord)
        )

    def _get_orthogonal_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate horizontally and vertically."""
        directions = (
            Direction(1, 0),
            Direction(0, 1),
            Direction(-1, 0),
            Direction(0, -1),
        )
        piece_types = (Rook, Queen)
        return self._get_straight_attacker_coords(color, coord, directions, piece_types)

    def _get_diagonal_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate diagonally."""
        directions = (
            Direction(1, 1),
            Direction(1, -1),
            Direction(-1, 1),
            Direction(-1, -1),
        )
        piece_types = (Bishop, Queen)
        return self._get_straight_attacker_coords(color, coord, directions, piece_types)

    def _get_straight_attacker_coords(
        self,
        color: Color,
        coord: Coordinate,
        directions: tuple[Direction],
        piece_types: tuple[type[Piece]],
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color and types
        attacking the given coordinate in a straight line in the directions."""
        coords = []

        for direction in directions:
            curr_coord = Coordinate(
                coord.row_idx + direction.row_delta, coord.col_idx + direction.col_delta
            )

            while Board.is_in_bounds(curr_coord):
                piece = self.get_piece(curr_coord)

                if piece is not None:
                    is_same_color_correct_piece = (
                        isinstance(piece, tuple(piece_types)) and piece.color == color
                    )

                    if is_same_color_correct_piece:
                        coords.append(curr_coord)

                    break

                curr_coord = Coordinate(
                    curr_coord.row_idx + direction.row_delta,
                    curr_coord.col_idx + direction.col_delta,
                )

        return coords

    def _get_knight_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all knights of the color attacking
        the given coordinate."""
        coords = []

        for row_delta, col_delta in KnightMoveStrategy.MOVE_PATTERNS:
            curr_coord = Coordinate(
                coord.row_idx + row_delta, coord.col_idx + col_delta
            )
            piece = self.get_piece(curr_coord)
            is_same_color_knight = isinstance(piece, Knight) and piece.color == color

            if is_same_color_knight:
                coords.append(curr_coord)

        return coords

    def _get_king_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all kings of the color attacking the
        given coordinate."""
        coords = []

        for row_delta, col_delta in KingMoveStrategy.MOVE_PATTERNS:
            curr_coord = Coordinate(
                coord.row_idx + row_delta, coord.col_idx + col_delta
            )

            if not Board.is_in_bounds(curr_coord):
                continue

            piece = self.get_piece(curr_coord)
            is_same_color_king = isinstance(piece, King) and piece.color == color

            if is_same_color_king:
                coords.append(curr_coord)

        return coords

    # TODO
    def _get_pawn_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pawns of the color attacking the
        given coordinate."""
        pawn_row_delta = PawnMoveStrategy.get_row_delta(color)
        coords = []

        # TODO: what to do with col deltas? should this be in movestrat?

        for col_delta in (-1, 1):
            curr_coord = Coordinate(
                coord.row_idx - pawn_row_delta, coord.col_idx + col_delta
            )
            if not Board.is_in_bounds(curr_coord):
                continue

            piece = self.get_piece(curr_coord)
            is_same_color_pawn = isinstance(piece, Pawn) and piece.color == color

            if is_same_color_pawn:
                coords.append(curr_coord)

        return coords

    # DONE
    def _get_king_coord(self, color: Color) -> Coordinate:
        """Get the coordinate of the king of the color."""
        return (
            self._white_king_coord if color is Color.WHITE else self._black_king_coord
        )

    # DONE
    def _set_king_coords(self, color: Color, coord: Coordinate) -> None:
        """Set the coordinate of the king of the color."""
        if color is Color.WHITE:
            self._white_king_coord = coord
        else:
            self._black_king_coord = coord

    # DONE
    def _set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for col_idx, piece_type in enumerate(piece_order):
            white_piece_coord = Coordinate(0, col_idx)
            black_piece_coord = Coordinate(BOARD_SIZE - 1, col_idx)
            white_pawn_coord = Coordinate(WHITE_PAWN_ROW_IDX, col_idx)
            black_pawn_coord = Coordinate(BLACK_PAWN_ROW_IDX, col_idx)

            self._set_piece(white_piece_coord, piece_type(Color.WHITE))
            self._set_piece(black_piece_coord, piece_type(Color.BLACK))
            self._set_piece(white_pawn_coord, Pawn(Color.WHITE))
            self._set_piece(black_pawn_coord, Pawn(Color.BLACK))

    # DONE
    def _set_piece(self, coord: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        if not Board.is_in_bounds(coord):
            return

        self._squares[coord.row_idx][coord.col_idx] = piece

        if isinstance(piece, King):
            self._set_king_coords(piece.color, coord)
