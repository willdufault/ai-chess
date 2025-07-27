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

        # TODO: PICK UP HERE, IMPLEMENT THIS FLOW + TEST
        # TODO: IN MIDDLE OF REFACTOR, NEED TO FINISH BOARD + GAME (THIS WAS EXTENSION OF BOARD)

        row_direction = self.get_row_direction(color)
        row_delta = to_row_idx - from_row_idx

        if row_delta not in (row_direction, 2 * row_direction):
            return False

        col_delta = to_col_idx - from_col_idx

        if abs(col_delta) > 1:
            return False

        is_adjacent_column = col_delta in (-1, 1)

        if col_delta == 0:
            is_piece_forward_one = board.is_occupied(
                from_row_idx + row_direction, from_col_idx
            )

            if is_piece_forward_one:
                return False

            is_piece_forward_two = board.is_occupied(
                from_row_idx + 2 * row_direction, from_col_idx
            )
            from_piece = board.get_piece(from_row_idx, from_col_idx)

            if (
                row_delta == 2 * row_direction
                and from_piece.has_moved
                or is_piece_forward_two
            ):
                return False
        elif is_adjacent_column:
            if row_delta > 1:
                return False

            to_piece = board.get_piece(to_row_idx, to_col_idx)

            if to_piece is None or to_piece.color == color:
                return False
        else:
            return False

        return True

        """
        if col delta is 0
            if piece at row + 1
                return false

            if row delta is 2 and piece at to
                return false
            
        elif col delta in 1, -1
            if no piece at to or piece on same team
                return false
        
        else:
            return false
        
        return true
        
        """

        return True

    @staticmethod
    def get_row_direction(color: Color) -> int:
        """Return the pawn row delta for the color."""
        return 1 if color is Color.WHITE else -1

    def _is_valid_forward_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
    ) -> bool:
        """Return whether the move is a valid forward move."""
        row_delta = to_row_idx - from_row_idx
        col_delta = to_col_idx - from_col_idx
        row_direction = self.get_row_direction(color)
        is_valid_row_delta = row_delta in (row_direction, 2 * row_direction)
        return is_valid_row_delta and col_delta == 0

    def _is_valid_diagonal_move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
    ) -> bool:
        """Return whether the move is a valid diagonal move."""
        row_delta = to_row_idx - from_row_idx
        col_delta = to_col_idx - from_col_idx
        row_direction = self.get_row_direction(color)
        is_valid_col_delta = col_delta in (-1, 1)
        return is_valid_col_delta and row_delta == row_direction


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
