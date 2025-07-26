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


class PawnMoveStrategy(MoveStrategy):
    """Represents the move strategy for a pawn."""

    # TODO: need move col deltas?
    move_col_deltas = (0,)
    attack_col_deltas = (-1, 1)
    row_deltas = (1, 2)

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

        # TODO: Implement En Passant.

        if not self._is_legal_col_delta(to_col_idx, from_col_idx):
            return False
        
        # TODO: PICK UP HERE, IMPLEMENT THIS FLOW + TEST
        # TODO: IN MIDDLE OF REFACTOR, NEED TO FINISH BOARD + GAME (THIS WAS EXTENSION OF BOARD)

        """
        if col delta not in -1, 0, 1
            return false

        if row delta not in 1, 2
            return false

        if col delta is 0
            if piece at row + 1
                return false

            if row delta is 2 and piece at to
                return false
            
        elif col delta in 1, -1
            if row delta not 1
                return false

            if no piece at to
                return false            
        
        return true
        
        """

        if self.is_vertical_capture(from_col_idx, to_row_idx, to_col_idx):
            return False

        if self.is_diagonal_move(from_col_idx, to_row_idx, to_col_idx):
            return False

        # row_delta = self.get_row_delta(color)
        # is_moving_forward_two = (
        #     to_row_idx == from_row_idx + 2 * row_delta and from_col_idx == to_col_idx
        # )
        # is_moving_forward_one = to_row_idx == from_row_idx + row_delta

        # if is_moving_forward_two:
        #     if not self._is_legal_move_forward_two(
        #         from_row_idx, from_col_idx, to_row_idx, to_col_idx, board
        #     ):
        #         return False
        # elif not is_moving_forward_one:
        #     return False

        return True

    @staticmethod
    def get_row_delta(color: Color) -> int:
        """Return the pawn row delta for the color."""
        return 1 if color is Color.WHITE else -1

    def _is_legal_col_delta(self, from_col_idx: int, to_col_idx: int) -> bool:
        """Return whether the column delta is legal."""
        col_delta = to_col_idx - from_col_idx
        legal_col_deltas = self.move_col_deltas + self.attack_col_deltas
        return col_delta in legal_col_deltas

    def _is_legal_row_delta(self, )

    def is_vertical_capture(
        self,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move attempts to capture a piece vertically."""
        to_piece = board.get_piece(to_row_idx, to_col_idx)
        return from_col_idx == to_col_idx and to_piece is not None

    def is_diagonal_move(
        self,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move attempts to move diagonally."""
        to_piece = board.get_piece(to_row_idx, to_col_idx)
        return from_col_idx != to_col_idx and to_piece is None

    def _is_legal_forward_move(
        self,
        color: int,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        board: Board,
    ) -> bool:
        """Return whether the move is a legal forward move."""
        row_delta = self.get_row_delta(color)
        from_piece = board.get_piece(from_row_idx, from_col_idx)
        is_forward_two_move = (
            to_row_idx == from_row_idx + 2 * row_delta and from_col_idx == to_col_idx
        )
        can_move_forward_two = from_piece.has_moved and not board.is_blocked(
            from_row_idx, from_col_idx, to_row_idx, to_col_idx
        )

        if is_forward_two_move:
            if not can_move_forward_two:
                return False

        is_moving_forward_one = to_row_idx == from_row_idx + row_delta

        if not is_moving_forward_one:
            return False

        return True


class KnightMoveStrategy(MoveStrategy):
    """Represents the move strategy for a knight."""

    move_patterns = [
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
    ]

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
        row_delta = to_row_idx - from_row_idx
        col_delta = to_col_idx - from_col_idx
        return (row_delta, col_delta) in self.move_patterns


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

        if board.is_blocked(from_row_idx, from_col_idx, to_row_idx, to_col_idx):
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

        if board.is_blocked(from_row_idx, from_col_idx, to_row_idx, to_col_idx):
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

        if board.is_blocked(from_row_idx, from_col_idx, to_row_idx, to_col_idx):
            return False

        return True


class KingMoveStrategy(MoveStrategy):
    """Represents the move strategy for a king."""

    move_patterns = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    ]

    def is_legal_move(
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
        return (row_delta, col_delta) in self.move_patterns
