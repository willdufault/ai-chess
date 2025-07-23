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
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        pass

    # * some helper that takes in delta x + y and can be used to check blocking
    # * pieces along horiz, vert, diag, use in bishop, rook, queen
    def _is_blocked(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        raise NotImplementedError


class PawnMoveStrategy(MoveStrategy):
    """Represents the move strategy for a pawn."""

    def is_legal_move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        """Return whether the move is a legal Pawn move."""

        # TODO: En Passant requires move history.

        if abs(from_column_index - to_column_index) > 1:
            return False

        to_piece = board.get_piece(to_row_index, to_column_index)
        if from_column_index == to_column_index and to_piece is not None:
            return False

        if from_column_index != to_column_index and to_piece is None:
            return False

        from_piece = board.get_piece(from_row_index, from_column_index)
        row_delta = 1 if color == Color.WHITE else -1
        if (
            to_row_index == from_row_index + 2 * row_delta
            and from_column_index == to_column_index
        ):
            adjacent_piece = board.get_piece(
                from_row_index + row_delta, from_column_index
            )
            if from_piece.has_moved or adjacent_piece is not None:
                return False
        elif to_row_index != from_row_index + row_delta:
            return False

        from_piece.has_moved = True
        return True


class KnightMoveStrategy(MoveStrategy):
    """Represents the move strategy for a knight."""

    def is_legal_move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        raise NotImplementedError


class BishopMoveStrategy(MoveStrategy):
    """Represents the move strategy for a bishop."""

    def is_legal_move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        raise NotImplementedError


class RookMoveStrategy(MoveStrategy):
    """Represents the move strategy for a rook."""

    def is_legal_move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        raise NotImplementedError


class QueenMoveStrategy(MoveStrategy):
    """Represents the move strategy for a queen."""

    def is_legal_move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        raise NotImplementedError


class KingMoveStrategy(MoveStrategy):
    """Represents the move strategy for a king."""

    def is_legal_move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
        board: Board,
    ) -> bool:
        raise NotImplementedError
