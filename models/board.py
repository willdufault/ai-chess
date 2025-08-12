from enums import Color

from .coordinate import Coordinate
from .direction import Direction
from .move import Move
from .move_strategies import (
    DIAGONAL_DIRECTIONS,
    ORTHOGONAL_DIRECTIONS,
    KingMoveStrategy,
    KnightMoveStrategy,
    PatternMoveStrategy,
    PawnMoveStrategy,
    StraightMoveStrategy,
)
from .pieces import Bishop, FirstMovePiece, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
KING_COL_IDX = 4
WHITE_PAWN_ROW_IDX = 1
BLACK_PAWN_ROW_IDX = BOARD_SIZE - 2


# TODO: when generating legal moves, cache per board, make sure hash is efficient
class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        self._white_king_coord = Coordinate(0, KING_COL_IDX)
        self._black_king_coord = Coordinate(BOARD_SIZE - 1, KING_COL_IDX)

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

    @staticmethod
    def get_last_row(color: Color) -> int:
        """Return the index of the last row for the color."""
        return BOARD_SIZE - 1 if color is Color.WHITE else 0

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

    def set_piece(self, coord: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        if not Board.is_in_bounds(coord):
            return
        self._squares[coord.row_idx][coord.col_idx] = piece
        if isinstance(piece, King):
            self._set_king_coords(piece.color, coord)

    def is_occupied(self, coord: Coordinate) -> bool:
        """Return whether the coordinate has a piece on it."""
        if not Board.is_in_bounds(coord):
            return False
        return self._squares[coord.row_idx][coord.col_idx] is not None

    def make_move(self, move: Move) -> Piece | None:
        """Make the move and return the piece at the to coordinate."""
        from_coord = move.from_coord
        to_coord = move.to_coord
        from_piece = move._from_piece
        to_piece = move._to_piece
        are_coords_in_bounds = Board.is_in_bounds(from_coord) and Board.is_in_bounds(
            to_coord
        )
        if not are_coords_in_bounds:
            return None

        self.set_piece(from_coord, None)
        self.set_piece(to_coord, from_piece)

        if isinstance(from_piece, FirstMovePiece):
            from_piece.has_moved = True

        return to_piece

    # TODO: make private?
    def undo_move(self, move: Move) -> Piece | None:
        """Undo a move and restore the state of both the from and to pieces."""
        from_coord = move.from_coord
        to_coord = move.to_coord
        from_piece = move.from_piece
        from_piece_has_moved = move.from_piece_has_moved
        to_piece = move.to_piece
        reversed_move = Move(to_coord, from_coord, from_piece, None)
        self.make_move(reversed_move)
        self.set_piece(to_coord, to_piece)

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
        opponent_color = Color.get_other_color(color)
        return self.is_attacking(opponent_color, king_coord)

    # TODO: after board refactor, SRP
    def is_in_checkmate(self, color: Color) -> bool:
        """Return whether the color is in checkmate."""
        if not self.is_in_check(color):
            return False

        if not self.is_king_trapped(color):
            return False

        other_color = Color.get_other_color(color)
        king_coord = self._get_king_coord(color)
        attacker_coords = self._get_attacker_coords(other_color, king_coord)
        is_defense_possible = len(attacker_coords) == 1
        if not is_defense_possible:
            return True

        attacker_coord = attacker_coords[0]
        if self._can_capture_attack(color, attacker_coord):
            return False

        if self._can_block_attack(color, attacker_coord):
            return False

        return True

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has no empty escape squares."""
        opponent_color = Color.get_other_color(color)
        king_coord = self._get_king_coord(color)
        for direction in KingMoveStrategy.MOVE_PATTERNS:
            curr_coord = Coordinate(
                king_coord.row_idx + direction.row_delta,
                king_coord.col_idx + direction.col_delta,
            )
            if not self.is_in_bounds(curr_coord):
                continue

            piece = self.get_piece(curr_coord)
            if piece is not None:
                continue

            if not self.is_attacking(opponent_color, curr_coord):
                return False

        return True

    def is_blocked(self, from_coord: Coordinate, to_coord: Coordinate) -> bool:
        """Return whether there is a piece between the from and to coordinates.
        Assumes horizontal, vertical, or diagonal movement."""
        row_diff = to_coord.row_idx - from_coord.row_idx
        col_diff = to_coord.col_idx - from_coord.col_idx
        step_count = max(abs(row_diff), abs(col_diff))
        if step_count == 0:
            return False

        row_delta = row_diff // step_count
        col_delta = col_diff // step_count
        for step in range(1, step_count):
            curr_coord = Coordinate(
                from_coord.row_idx + step * row_delta,
                from_coord.col_idx + step * col_delta,
            )
            piece = self.get_piece(curr_coord)
            if piece is not None:
                return True

        return False

    def _simulate_defense(
        self, color: Color, target_coord: Coordinate, piece_coords: Coordinate
    ) -> bool:
        """Return whether moving any of the pieces at the coordinates can move
        to the target coordinate without putting the color in check."""
        target_piece = self.get_piece(target_coord)
        for piece_coord in piece_coords:
            curr_piece = self.get_piece(piece_coord)
            self.set_piece(piece_coord, None)
            self.set_piece(target_coord, curr_piece)
            is_still_in_check = self.is_in_check(color)
            self.set_piece(piece_coord, curr_piece)
            self.set_piece(target_coord, target_piece)
            if not is_still_in_check:
                return True
        return False

    def _can_block_attack(self, color: Color, attacker_coord: Coordinate):
        """Return whether the color can block an attack from the coordinate."""
        attacker = self.get_piece(attacker_coord)
        if isinstance(attacker, Knight):
            return False

        king_coord = self._get_king_coord(color)
        row_diff = attacker_coord.row_idx - king_coord.row_idx
        col_diff = attacker_coord.col_idx - king_coord.col_idx
        step_count = max(abs(row_diff), abs(col_diff))
        row_delta = row_diff // step_count
        col_delta = col_diff // step_count
        for step in range(1, step_count):
            curr_coord = Coordinate(
                king_coord.row_idx + step * row_delta,
                king_coord.col_idx + step * col_delta,
            )
            blocker_coords = self._get_blocker_coords(color, curr_coord)
            can_block_curr_coord = self._simulate_defense(
                color, curr_coord, blocker_coords
            )
            if can_block_curr_coord:
                return True

        return False

    def _can_capture_attack(self, color: Color, attacker_coord: Coordinate) -> bool:
        """Return whether the color can capture the attacker at the coordinate."""
        defender_coords = self._get_attacker_coords(color, attacker_coord)
        return self._simulate_defense(color, attacker_coord, defender_coords)

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
        if not is_two_back_same_color_pawn or two_back_piece.has_moved:
            return []

        return [two_back_coord]

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
        return self._get_straight_attacker_coords(color, coord, ORTHOGONAL_DIRECTIONS)

    def _get_diagonal_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate diagonally."""
        return self._get_straight_attacker_coords(color, coord, DIAGONAL_DIRECTIONS)

    def _get_straight_attacker_coords(
        self,
        color: Color,
        coord: Coordinate,
        directions: tuple[Direction],
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        given coordinate in a straight line in any of the given directions."""
        coords = []
        for direction in directions:
            curr_coord = Coordinate(
                coord.row_idx + direction.row_delta, coord.col_idx + direction.col_delta
            )
            while Board.is_in_bounds(curr_coord):
                piece = self.get_piece(curr_coord)
                if piece is not None:
                    can_piece_attack_square = (
                        isinstance(piece.move_strategy, StraightMoveStrategy)
                        and direction in piece.move_strategy.DIRECTIONS
                    )
                    if can_piece_attack_square and piece.color == color:
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
        res = self._get_pattern_piece_attacker_coords(color, coord, KnightMoveStrategy)
        return res

    def _get_king_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all kings of the color attacking the
        given coordinate."""
        return self._get_pattern_piece_attacker_coords(color, coord, KingMoveStrategy)

    def _get_pattern_piece_attacker_coords(
        self, color: Color, coord: Coordinate, move_strategy: PatternMoveStrategy
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color that can
        attack the given coordinate using any of the move patterns."""
        coords = []
        for move_pattern in move_strategy.MOVE_PATTERNS:
            curr_coord = Coordinate(
                coord.row_idx + move_pattern.row_delta,
                coord.col_idx + move_pattern.col_delta,
            )
            piece = self.get_piece(curr_coord)
            if piece is None:
                continue

            can_piece_attack_square = isinstance(piece.move_strategy, move_strategy)
            if can_piece_attack_square and piece.color == color:
                coords.append(curr_coord)
        return coords

    def _get_pawn_attacker_coords(
        self, color: Color, coord: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pawns of the color attacking the
        given coordinate."""
        coords = []
        pawn_row_delta = PawnMoveStrategy.get_row_delta(color)
        for col_delta in PawnMoveStrategy._CAPTURE_COL_DELTAS:
            curr_coord = Coordinate(
                coord.row_idx - pawn_row_delta, coord.col_idx + col_delta
            )
            piece = self.get_piece(curr_coord)
            is_same_color_pawn = isinstance(piece, Pawn) and piece.color == color
            if is_same_color_pawn:
                coords.append(curr_coord)
        return coords

    def _get_king_coord(self, color: Color) -> Coordinate:
        """Get the coordinate of the king of the color."""
        return (
            self._white_king_coord if color is Color.WHITE else self._black_king_coord
        )

    def _set_king_coords(self, color: Color, coord: Coordinate) -> None:
        """Set the coordinate of the king of the color."""
        if color is Color.WHITE:
            self._white_king_coord = coord
        else:
            self._black_king_coord = coord

    def _set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col_idx, piece_type in enumerate(piece_order):
            white_piece_coord = Coordinate(0, col_idx)
            black_piece_coord = Coordinate(BOARD_SIZE - 1, col_idx)
            white_pawn_coord = Coordinate(WHITE_PAWN_ROW_IDX, col_idx)
            black_pawn_coord = Coordinate(BLACK_PAWN_ROW_IDX, col_idx)
            self.set_piece(white_piece_coord, piece_type(Color.WHITE))
            self.set_piece(black_piece_coord, piece_type(Color.BLACK))
            self.set_piece(white_pawn_coord, Pawn(Color.WHITE))
            self.set_piece(black_pawn_coord, Pawn(Color.BLACK))
