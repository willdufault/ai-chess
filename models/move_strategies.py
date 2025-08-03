from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from enums import Color

if TYPE_CHECKING:
    from .board import Board

ORTHOGONAL_DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIAGONAL_DIRECTIONS = ((1, 1), (-1, 1), (-1, -1), (1, -1))


class MoveStrategy(ABC):
    """Represents an abstract move strategy for a chess piece."""

    @abstractmethod
    def is_valid_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is valid."""
        pass


class StraightMoveStrategy(MoveStrategy, ABC):
    """Represents an abstract move strategy for a chess piece that moves in
    straight lines."""

    _DIRECTIONS = ()

    def is_valid_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is valid for a piece that moves in straight lines."""
        row_delta = to_row_idx - from_row_idx
        col_delta = to_col_idx - from_col_idx

        if row_delta != 0:
            col_delta /= abs(row_delta)
            row_delta /= abs(row_delta)
        elif col_delta != 0:
            row_delta /= abs(col_delta)
            col_delta /= abs(col_delta)

        is_valid_direction = (row_delta, col_delta) in self._DIRECTIONS

        if not is_valid_direction:
            return False

        is_path_clear = not board.is_blocked(
            from_row_idx, from_col_idx, to_row_idx, to_col_idx
        )

        return is_path_clear


class PawnMoveStrategy(MoveStrategy):
    """Represents the move strategy for a pawn."""

    _DOUBLE_MOVE_ROW_DELTA = 2
    _MOVE_COL_DELTA = 0
    _CAPTURE_COL_DELTAS = (-1, 1)

    @staticmethod
    def get_row_direction(color: Color) -> int:
        """Return the pawn row delta for the color."""
        return 1 if color is Color.WHITE else -1

    def is_valid_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is valid for a pawn."""

        # TODO: Implement En Passant.

        col_delta = to_col_idx - from_col_idx
        is_same_col = col_delta == self._MOVE_COL_DELTA
        is_adjacent_col = col_delta in self._CAPTURE_COL_DELTAS

        if is_same_col:
            return self._is_valid_forward_move(
                color, from_row_idx, from_col_idx, to_row_idx, board
            )

        if is_adjacent_col:
            return self._is_valid_capture(
                color, from_row_idx, to_row_idx, to_col_idx, board
            )

        return False

    def _is_valid_forward_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        board: Board,
    ):
        """Return whether the forward move is valid."""
        row_direction = PawnMoveStrategy.get_row_direction(color)
        is_forward_one_occupied = board.is_occupied(
            from_row_idx + row_direction, from_col_idx
        )

        if is_forward_one_occupied:
            return False

        row_delta = to_row_idx - from_row_idx
        is_single_move = row_delta == row_direction
        is_double_move = row_delta == self._DOUBLE_MOVE_ROW_DELTA * row_direction

        if is_single_move:
            return True

        if is_double_move:
            return self._is_valid_double_move(
                from_row_idx, from_col_idx, row_direction, board
            )

        return False

    def _is_valid_double_move(
        self, from_row_idx: int, from_col_idx: int, row_direction: int, board: Board
    ) -> bool:
        """Return whether the double move is valid."""
        from_piece = board.get_piece(from_row_idx, from_col_idx)

        if from_piece.has_moved:
            return False

        is_forward_two_empty = not board.is_occupied(
            from_row_idx + self._DOUBLE_MOVE_ROW_DELTA * row_direction, from_col_idx
        )

        return is_forward_two_empty

    def _is_valid_capture(
        self,
        color: Color,
        from_row_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ):
        """Return whether the capture is valid."""
        row_delta = to_row_idx - from_row_idx
        row_direction = PawnMoveStrategy.get_row_direction(color)
        is_moving_forward_one = row_delta == row_direction

        if not is_moving_forward_one:
            return False

        to_piece = board.get_piece(to_row_idx, to_col_idx)
        is_capturing_opponent = to_piece is not None and to_piece.color != color

        return is_capturing_opponent


class KnightMoveStrategy(MoveStrategy):
    """Represents the move strategy for a knight."""

    MOVE_PATTERNS = [
        (1, 2),
        (1, -2),
        (2, 1),
        (2, -1),
        (-1, 2),
        (-1, -2),
        (-2, 1),
        (-2, -1),
    ]

    def is_valid_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is valid for a knight."""
        row_delta = to_row_idx - from_row_idx
        col_delta = to_col_idx - from_col_idx
        is_valid_move_pattern = (row_delta, col_delta) in self.MOVE_PATTERNS
        return is_valid_move_pattern


class BishopMoveStrategy(StraightMoveStrategy):
    """Represents the move strategy for a bishop."""

    _DIRECTIONS = DIAGONAL_DIRECTIONS


class RookMoveStrategy(StraightMoveStrategy):
    """Represents the move strategy for a rook."""

    _DIRECTIONS = ORTHOGONAL_DIRECTIONS


class QueenMoveStrategy(StraightMoveStrategy):
    """Represents the move strategy for a queen."""

    _DIRECTIONS = ORTHOGONAL_DIRECTIONS + DIAGONAL_DIRECTIONS


class KingMoveStrategy(MoveStrategy):
    """Represents the move strategy for a king."""

    MOVE_PATTERNS = [
        (1, 0),
        (1, 1),
        (1, -1),
        (0, 1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (-1, -1),
    ]

    def is_valid_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        row_delta = to_row_idx - from_row_idx
        col_delta = to_col_idx - from_col_idx
        return (row_delta, col_delta) in self.MOVE_PATTERNS
