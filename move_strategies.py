from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

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

    # TODO: some helper that takes in delta x + y and can be used to check blocking
    # TODO: pieces along horiz, vert, diag, use in bishop, rook, queen
    def _is_blocked(
        self,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether there is a piece between the from and to coordinates. Assumes horizontal,
        vertical, or diagonal movement."""
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

        # TODO: En Passant requires move history.

        if abs(from_col_idx - to_col_idx) > 1:
            return False

        to_piece = board.get_piece(to_row_idx, to_col_idx)
        if from_col_idx == to_col_idx and to_piece is not None:
            return False

        if from_col_idx != to_col_idx and to_piece is None:
            return False

        from_piece = board.get_piece(from_row_idx, from_col_idx)
        row_delta = 1 if color == Color.WHITE else -1
        if to_row_idx == from_row_idx + 2 * row_delta and from_col_idx == to_col_idx:
            if from_piece.has_moved or self._is_blocked(
                from_row_idx, from_col_idx, to_row_idx, to_col_idx, board
            ):
                return False
        elif to_row_idx != from_row_idx + row_delta:
            return False

        from_piece.has_moved = True
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
        row_diff = abs(from_row_idx - to_row_idx)
        col_diff = abs(from_col_idx - to_col_idx)
        diffs = (row_diff, col_diff)
        return 1 in diffs and 2 in diffs


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
        if row_diff != col_diff:
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
        if row_diff != 0 and col_diff != 0:
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
        if row_diff != col_diff and row_diff != 0 and col_diff != 0:
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
