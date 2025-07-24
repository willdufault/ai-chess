from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from constants import KNIGHT_MOVE_PATTERNS
from enums import Color

if TYPE_CHECKING:
    from board import Board


class MoveStrategy(ABC):
    """Represents an abstract move strategy for a chess piece."""

    @abstractmethod
    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is legal."""
        pass

    def _is_blocked(
        self,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
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
            piece = board.get_piece(row_idx, col_idx)
            if piece is not None:
                return True

        return False


class PawnMoveStrategy(MoveStrategy):
    """Represents the move strategy for a pawn."""

    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is a legal for a pawn."""
        # NOTE: I have no plans to implement En Passant.
        if abs(from_col_idx - to_col_idx) > 1:
            return False

        to_piece = board.get_piece(to_row_idx, to_col_idx)
        is_capturing_vertically = from_col_idx == to_col_idx and to_piece is not None
        if is_capturing_vertically:
            return False

        is_moving_diagonally = from_col_idx != to_col_idx and to_piece is None
        if is_moving_diagonally:
            return False

        from_piece = board.get_piece(from_row_idx, from_col_idx)

        row_delta = 1 if color == Color.WHITE else -1
        is_moving_forward_two = (
            to_row_idx == from_row_idx + 2 * row_delta and from_col_idx == to_col_idx
        )
        if is_moving_forward_two:
            if from_piece.has_moved or self._is_blocked(
                from_row_idx, from_col_idx, to_row_idx, to_col_idx, board
            ):
                return False
        elif to_row_idx != from_row_idx + row_delta:
            return False

        return True


class KnightMoveStrategy(MoveStrategy):
    """Represents the move strategy for a knight."""

    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is legal for a knight."""
        row_delta = from_row_idx - to_row_idx
        col_delta = from_col_idx - to_col_idx
        return (row_delta, col_delta) in KNIGHT_MOVE_PATTERNS


class BishopMoveStrategy(MoveStrategy):
    """Represents the move strategy for a bishop."""

    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is legal for a bishop."""
        row_diff = abs(from_row_idx - to_row_idx)
        col_diff = abs(from_col_idx - to_col_idx)
        is_not_diagonal = row_diff != col_diff
        if is_not_diagonal:
            return False

        if self._is_blocked(from_row_idx, from_col_idx, to_row_idx, to_col_idx, board):
            return False

        return True


class RookMoveStrategy(MoveStrategy):
    """Represents the move strategy for a rook."""

    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is legal for a rook."""
        row_diff = abs(from_row_idx - to_row_idx)
        col_diff = abs(from_col_idx - to_col_idx)
        is_not_straight = row_diff != 0 and col_diff != 0
        if is_not_straight:
            return False

        if self._is_blocked(from_row_idx, from_col_idx, to_row_idx, to_col_idx, board):
            return False

        return True


class QueenMoveStrategy(MoveStrategy):
    """Represents the move strategy for a queen."""

    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is legal for a queen."""
        row_diff = abs(from_row_idx - to_row_idx)
        col_diff = abs(from_col_idx - to_col_idx)
        is_not_diagonal = row_diff != col_diff
        is_not_straight = row_diff != 0 and col_diff != 0
        if is_not_diagonal and is_not_straight:
            return False

        if self._is_blocked(from_row_idx, from_col_idx, to_row_idx, to_col_idx, board):
            return False

        return True


class KingMoveStrategy(MoveStrategy):
    """Represents the move strategy for a king."""

    def is_legal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        row_diff = abs(from_row_idx - to_row_idx)
        col_diff = abs(from_col_idx - to_col_idx)
        return row_diff <= 1 and col_diff <= 1
