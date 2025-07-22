from abc import ABC, abstractmethod

from enums import Color


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
    ) -> bool:
        pass

    def __passes_basic_move_checks(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
    ) -> bool:
        """Return whether the move passes basic legality checks."""
        #! board import error
        # if not (
        #     board.is_in_bounds(from_row_index, from_column_index)
        #     and board.is_in_bounds(to_row_index, to_column_index)
        # ):
        #     return False

        # from_piece = board.get_piece(from_row_index, from_column_index)
        # if from_piece is None or from_piece.color != color:
        #     return False

        # to_piece = board.get_piece(to_row_index, to_column_index)
        # if to_piece is not None and to_piece.color == color:
        #     return False

        return True

    # * some helper that takes in delta x + y and can be used to check blocking
    # * pieces along horiz, vert, diag, use in bishop, rook, queen
    def __is_blocked(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
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
    ) -> bool:
        if not self.__passes_basic_move_checks():
            return False

        # TODO: en passant

        #! board import error
        # row_delta = 1 if color == Color.WHITE else -1
        # if to_row_index != from_row_index + row_delta:
        #     return False

        # if abs(from_column_index - to_column_index) > 1:
        #     return False

        # to_piece = board.get_piece(to_row_index, to_column_index)
        # if from_column_index == to_column_index and to_piece is not None:
        #     return False

        # if from_column_index != to_column_index and to_piece is None:
        #     return False

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
    ) -> bool:
        raise NotImplementedError
