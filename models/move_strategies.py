from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from enums.color import Color
from models.coordinate import Coordinate
from models.direction import Direction
from models.move import Move
from utils.board_utils import is_coordinate_in_bounds

if TYPE_CHECKING:
    from models.board import Board

_ORTHOGONAL_DIRECTIONS = (
    Direction(0, 1),
    Direction(0, -1),
    Direction(1, 0),
    Direction(-1, 0),
)
_DIAGONAL_DIRECTIONS = (
    Direction(1, 1),
    Direction(1, -1),
    Direction(-1, 1),
    Direction(-1, -1),
)


class MoveStrategy(ABC):
    # TODO: this should probably take in a move instead of color + coordinates
    @classmethod
    @abstractmethod
    def is_move_valid(
        cls,
        move: Move,
        board: Board,
    ) -> bool: ...

    @classmethod
    @abstractmethod
    def get_attacker_coordinates(
        cls, color: Color, target_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]: ...

    @classmethod
    @abstractmethod
    def get_candidate_moves(
        cls,
        color: Color,
        from_coordinate: Coordinate,
        board: Board,
    ) -> list[Move]: ...


class StraightMoveStrategy(MoveStrategy, ABC):
    """Represents an abstract move strategy for a chess piece that moves in
    straight lines."""

    # Abstract class variable must be implemented.
    _DIRECTIONS: tuple[Direction, ...] = ()

    @classmethod
    def is_move_valid(
        cls,
        move: Move,
        board: Board,
    ) -> bool:
        """Return whether the move is valid for a piece that moves in straight lines."""
        row_delta = move.to_coordinate.row_index - move.from_coordinate.row_index
        column_delta = (
            move.to_coordinate.column_index - move.from_coordinate.column_index
        )
        if row_delta != 0:
            column_delta /= abs(row_delta)
            row_delta /= abs(row_delta)
        elif column_delta != 0:
            row_delta /= abs(column_delta)
            column_delta /= abs(column_delta)

        are_whole_numbers = row_delta.is_integer() and column_delta.is_integer()
        if not are_whole_numbers:
            return False

        row_delta = int(row_delta)
        column_delta = int(column_delta)
        is_valid_direction = Direction(row_delta, column_delta) in cls._DIRECTIONS
        if not is_valid_direction:
            return False

        is_path_clear = not board.is_path_blocked(
            move.from_coordinate, move.to_coordinate
        )
        return is_path_clear

    @classmethod
    def get_attacker_coordinates(
        cls, color: Color, target_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        target coordinate in a straight line."""

        attacker_coordinates = []
        for direction in cls._DIRECTIONS:
            current_coordinate = Coordinate(
                target_coordinate.row_index + direction.row_delta,
                target_coordinate.column_index + direction.column_delta,
            )
            while is_coordinate_in_bounds(current_coordinate):
                if board.is_occupied(current_coordinate):
                    current_piece = board.get_piece(current_coordinate)
                    assert current_piece is not None
                    can_current_piece_attack_target = (
                        isinstance(current_piece.MOVE_STRATEGY, cls)
                        and direction in cls._DIRECTIONS
                    )
                    if can_current_piece_attack_target and current_piece.color == color:
                        attacker_coordinates.append(current_coordinate)

                    break

                current_coordinate = Coordinate(
                    current_coordinate.row_index + direction.row_delta,
                    current_coordinate.column_index + direction.column_delta,
                )
        return attacker_coordinates

    @classmethod
    def get_candidate_moves(
        cls, color: Color, from_coordinate: Coordinate, board: Board
    ) -> list[Move]:
        """Return a list of candidate moves from the from coordinate moving in a
        straight line without accounting for discovered check."""
        if not is_coordinate_in_bounds(from_coordinate):
            return []

        candidate_moves = []
        from_piece = board.get_piece(from_coordinate)
        for direction in cls._DIRECTIONS:
            row_delta = direction.row_delta
            column_delta = direction.column_delta
            to_coordinate = Coordinate(
                from_coordinate.row_index + row_delta,
                from_coordinate.column_index + column_delta,
            )
            while is_coordinate_in_bounds(to_coordinate):
                to_piece = board.get_piece(to_coordinate)
                current_move = Move(
                    color, from_coordinate, to_coordinate, from_piece, to_piece
                )
                if board.is_occupied(to_coordinate):
                    assert to_piece is not None
                    if to_piece.color != color:
                        candidate_moves.append(current_move)
                    break

                candidate_moves.append(current_move)
                to_coordinate = Coordinate(
                    to_coordinate.row_index + row_delta,
                    to_coordinate.column_index + column_delta,
                )
        return candidate_moves


class PatternMoveStrategy(MoveStrategy, ABC):
    """Represents an abstract move strategy for a chess piece that moves in a
    specific pattern."""

    # Abstract class variable must be implemented.
    _MOVE_PATTERNS: tuple[Direction, ...] = ()

    @classmethod
    def is_move_valid(
        cls,
        move: Move,
        board: Board,
    ) -> bool:
        """Return whether the move is valid for a piece that moves in a specific pattern."""
        row_delta = move.to_coordinate.row_index - move.from_coordinate.row_index
        column_delta = (
            move.to_coordinate.column_index - move.from_coordinate.column_index
        )
        move_pattern = Direction(row_delta, column_delta)
        is_valid_move_pattern = move_pattern in cls._MOVE_PATTERNS
        return is_valid_move_pattern

    @classmethod
    def get_attacker_coordinates(
        cls, color: Color, target_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color attacking the
        target coordinate in a specific pattern."""
        attacker_coordinates = []
        for move_pattern in cls._MOVE_PATTERNS:
            current_coordinate = Coordinate(
                target_coordinate.row_index + move_pattern.row_delta,
                target_coordinate.column_index + move_pattern.column_delta,
            )
            if not is_coordinate_in_bounds(current_coordinate):
                continue

            if not board.is_occupied(current_coordinate):
                continue

            current_piece = board.get_piece(current_coordinate)
            assert current_piece is not None
            can_current_piece_attack_target = isinstance(
                current_piece.MOVE_STRATEGY, cls
            )
            if can_current_piece_attack_target and current_piece.color == color:
                attacker_coordinates.append(current_coordinate)
        return attacker_coordinates

    @classmethod
    def get_candidate_moves(
        cls, color: Color, from_coordinate: Coordinate, board: Board
    ) -> list[Move]:
        """Return a list of candidate moves from the from coordinate moving in a
        specific pattern without accounting for discovered check."""
        if not is_coordinate_in_bounds(from_coordinate):
            return []

        candidate_moves = []
        from_piece = board.get_piece(from_coordinate)
        for direction in cls._MOVE_PATTERNS:
            row_delta = direction.row_delta
            column_delta = direction.column_delta
            to_coordinate = Coordinate(
                from_coordinate.row_index + row_delta,
                from_coordinate.column_index + column_delta,
            )
            if not is_coordinate_in_bounds(to_coordinate):
                continue

            to_piece = board.get_piece(to_coordinate)
            if board.is_occupied(to_coordinate):
                assert to_piece is not None
                if to_piece.color == color:
                    continue

            current_move = Move(
                color, from_coordinate, to_coordinate, from_piece, to_piece
            )
            candidate_moves.append(current_move)
        return candidate_moves


class PawnMoveStrategy(MoveStrategy):
    _SINGLE_MOVE_ROW_DELTA = 1
    _DOUBLE_MOVE_ROW_DELTA = 2
    _MOVE_COLUMN_DELTA = 0
    _CAPTURE_COLUMN_DELTAS = (-1, 1)

    @classmethod
    def get_forward_row_delta(cls, color: Color) -> int:
        """Return the forward row delta for pawns of the color."""
        return (
            cls._SINGLE_MOVE_ROW_DELTA
            if color is Color.WHITE
            else -cls._SINGLE_MOVE_ROW_DELTA
        )

    @classmethod
    def is_move_valid(cls, move: Move, board: Board) -> bool:
        """Return whether the move is valid for a pawn."""

        # TODO: Implement En Passant.

        column_delta = (
            move.to_coordinate.column_index - move.from_coordinate.column_index
        )
        is_same_column = column_delta == cls._MOVE_COLUMN_DELTA
        if is_same_column:
            return cls._is_forward_move_valid(move, board)

        is_adjacent_column = column_delta in cls._CAPTURE_COLUMN_DELTAS
        if is_adjacent_column:
            return cls._is_capture_valid(move)

        return False

    @classmethod
    def get_attacker_coordinates(
        cls, color: Color, target_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pawns of the color attacking the
        given coordinate."""
        attacker_coordinates = []
        forward_row_delta = cls.get_forward_row_delta(color)
        for column_delta in cls._CAPTURE_COLUMN_DELTAS:
            current_coordinate = Coordinate(
                target_coordinate.row_index - forward_row_delta,
                target_coordinate.column_index + column_delta,
            )
            if not is_coordinate_in_bounds(current_coordinate):
                continue

            if not board.is_occupied(current_coordinate):
                continue

            current_piece = board.get_piece(current_coordinate)
            assert current_piece is not None
            is_current_piece_same_color_pawn = (
                isinstance(current_piece.MOVE_STRATEGY, cls)
                and current_piece.color == color
            )
            if is_current_piece_same_color_pawn:
                attacker_coordinates.append(current_coordinate)
        return attacker_coordinates

    @classmethod
    def get_blocker_coordinate(
        cls, color: Color, target_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return the coordinate of the pawn of the color that can block the
        empty target coordinate.

        NOTE: Even though there can be at most one blocking pawn, this method
        returns a list for consistency with other similar methods."""
        forward_row_delta = cls.get_forward_row_delta(color)
        one_back_coordinate = Coordinate(
            target_coordinate.row_index - forward_row_delta,
            target_coordinate.column_index,
        )
        if not is_coordinate_in_bounds(one_back_coordinate):
            return []

        if board.is_occupied(one_back_coordinate):
            return cls._get_one_back_blocker_coordinate(
                color, one_back_coordinate, board
            )

        two_back_coordinate = Coordinate(
            target_coordinate.row_index - 2 * forward_row_delta,
            target_coordinate.column_index,
        )
        if not is_coordinate_in_bounds(two_back_coordinate):
            return []

        if board.is_occupied(two_back_coordinate):
            return cls._get_two_back_blocker_coordinate(
                color, two_back_coordinate, board
            )

        return []

    @classmethod
    def get_candidate_moves(
        cls, color: Color, from_coordinate: Coordinate, board: Board
    ) -> list[Move]:
        """Return a list of candidate moves for a pawn at the from coordinate
        without accounting for discovered check."""
        if not is_coordinate_in_bounds(from_coordinate):
            return []

        candidate_forward_moves = cls._get_candidate_forward_moves(
            color, from_coordinate, board
        )
        candidate_captures = cls._get_candidate_captures(color, from_coordinate, board)
        return candidate_forward_moves + candidate_captures

    @classmethod
    def _get_candidate_forward_moves(
        cls, color: Color, from_coordinate: Coordinate, board: Board
    ) -> list[Move]:
        """Return a list of candidate forward moves for a pawn at the from
        coordinate without accounting for discovered check."""
        candidate_forward_moves = []
        from_piece = board.get_piece(from_coordinate)
        forward_row_delta = cls.get_forward_row_delta(color)

        # TODO: REFACTOR, CLEAN UP
        # forward one
        forward_one_coordinate = Coordinate(
            from_coordinate.row_index + forward_row_delta,
            from_coordinate.column_index,
        )
        if not is_coordinate_in_bounds(forward_one_coordinate):
            return []

        if board.is_occupied(forward_one_coordinate):
            return []

        forward_one_piece = board.get_piece(forward_one_coordinate)
        forward_one_move = Move(
            color,
            from_coordinate,
            forward_one_coordinate,
            from_piece,
            forward_one_piece,
        )
        candidate_forward_moves.append(forward_one_move)

        # forward two
        # TODO: fix pyright warning
        assert from_piece is not None
        if not from_piece.has_moved:  # pyright: ignore[reportAttributeAccessIssue]
            forward_two_coordinate = Coordinate(
                from_coordinate.row_index
                + cls._DOUBLE_MOVE_ROW_DELTA * forward_row_delta,
                from_coordinate.column_index,
            )
            if not is_coordinate_in_bounds(forward_two_coordinate):
                return candidate_forward_moves

            if board.is_occupied(forward_two_coordinate):
                return candidate_forward_moves

            forward_two_piece = board.get_piece(forward_two_coordinate)
            forward_two_move = Move(
                color,
                from_coordinate,
                forward_two_coordinate,
                from_piece,
                forward_two_piece,
            )
            candidate_forward_moves.append(forward_two_move)

        return candidate_forward_moves

    @classmethod
    def _get_candidate_captures(
        cls, color: Color, from_coordinate: Coordinate, board: Board
    ) -> list[Move]:
        """Return a list of candidate captures for a pawn at the from coordinate
        without accounting for discovered check."""
        candidate_captures = []
        from_piece = board.get_piece(from_coordinate)
        forward_row_delta = cls.get_forward_row_delta(color)
        for column_delta in cls._CAPTURE_COLUMN_DELTAS:
            capture_coordinate = Coordinate(
                from_coordinate.row_index + forward_row_delta,
                from_coordinate.column_index + column_delta,
            )
            if not is_coordinate_in_bounds(capture_coordinate):
                continue

            if not board.is_occupied(capture_coordinate):
                continue

            capture_piece = board.get_piece(capture_coordinate)
            assert capture_piece is not None
            is_capturing_same_color = capture_piece.color == color
            if is_capturing_same_color:
                continue

            capture_move = Move(
                color,
                from_coordinate,
                capture_coordinate,
                from_piece,
                capture_piece,
            )
            candidate_captures.append(capture_move)
        return candidate_captures

    @classmethod
    def _get_one_back_blocker_coordinate(
        cls, color: Color, one_back_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return the coordinate of the pawn of the color that can block the
        empty target coordinate one square forward."""
        one_back_piece = board.get_piece(one_back_coordinate)
        assert one_back_piece is not None
        is_one_back_piece_same_color_pawn = (
            isinstance(one_back_piece.MOVE_STRATEGY, cls)
            and one_back_piece.color == color
        )
        if not is_one_back_piece_same_color_pawn:
            return []

        return [one_back_coordinate]

    @classmethod
    def _get_two_back_blocker_coordinate(
        cls, color: Color, two_back_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return the coordinate of the pawn of the color that can block the
        empty target coordinate two squares forward."""
        two_back_piece = board.get_piece(two_back_coordinate)
        assert two_back_piece is not None
        is_two_back_piece_same_color_pawn = (
            isinstance(two_back_piece.MOVE_STRATEGY, cls)
            and two_back_piece.color == color
        )
        # TODO: fix pyright warning
        if (
            not is_two_back_piece_same_color_pawn
            or two_back_piece.has_moved  # pyright: ignore[reportAttributeAccessIssue]
        ):
            return []

        return [two_back_coordinate]

    @classmethod
    def _is_forward_move_valid(cls, move: Move, board: Board):
        """Return whether the forward move is valid."""
        forward_row_delta = cls.get_forward_row_delta(move.color)
        forward_one_coordinate = Coordinate(
            move.from_coordinate.row_index + forward_row_delta,
            move.from_coordinate.column_index,
        )
        is_forward_one_occupied = board.is_occupied(forward_one_coordinate)
        if is_forward_one_occupied:
            return False

        row_delta = move.to_coordinate.row_index - move.from_coordinate.row_index
        is_single_move = row_delta == forward_row_delta
        if is_single_move:
            return True

        is_double_move = row_delta == cls._DOUBLE_MOVE_ROW_DELTA * forward_row_delta
        if is_double_move:
            return cls._is_double_move_valid(move)

        return False

    @staticmethod
    def _is_double_move_valid(move: Move) -> bool:
        """Return whether the double move is valid."""
        assert move.from_piece is not None
        # TODO: fix pyright attribute warning
        if move.from_piece.has_moved:  # pyright: ignore[reportAttributeAccessIssue]
            return False
        return move.to_piece is None

    @classmethod
    def _is_capture_valid(cls, move: Move):
        """Return whether the capture is valid."""
        row_delta = move.to_coordinate.row_index - move.from_coordinate.row_index
        forward_row_delta = cls.get_forward_row_delta(move.color)
        is_moving_forward_one = row_delta == forward_row_delta
        if not is_moving_forward_one:
            return False

        is_capturing_opponent = (
            move.to_piece is not None and move.to_piece.color != move.color
        )
        return is_capturing_opponent


class KnightMoveStrategy(PatternMoveStrategy):
    _MOVE_PATTERNS = (
        Direction(1, 2),
        Direction(1, -2),
        Direction(2, 1),
        Direction(2, -1),
        Direction(-1, 2),
        Direction(-1, -2),
        Direction(-2, 1),
        Direction(-2, -1),
    )


class BishopMoveStrategy(StraightMoveStrategy):
    _DIRECTIONS = _DIAGONAL_DIRECTIONS


class RookMoveStrategy(StraightMoveStrategy):
    _DIRECTIONS = _ORTHOGONAL_DIRECTIONS


class QueenMoveStrategy(StraightMoveStrategy):
    _DIRECTIONS = _ORTHOGONAL_DIRECTIONS + _DIAGONAL_DIRECTIONS


class KingMoveStrategy(PatternMoveStrategy):
    _MOVE_PATTERNS = (
        Direction(0, 1),
        Direction(0, -1),
        Direction(1, 0),
        Direction(1, 1),
        Direction(1, -1),
        Direction(-1, 0),
        Direction(-1, 1),
        Direction(-1, -1),
    )

    # TODO: rename to get_valid_moves?
    @classmethod
    def get_potential_escape_coordinates(
        cls, king_coordinate: Coordinate, board: Board
    ) -> list[Coordinate]:
        """Return a list of all coordinates adjacent to the king coordinate that
        are either empty or occupied by a piece of the opposite color."""
        escape_coordinates = []
        king_piece = board.get_piece(king_coordinate)
        assert king_piece is not None
        king_color = king_piece.color
        for move_pattern in cls._MOVE_PATTERNS:
            current_coordinate = Coordinate(
                king_coordinate.row_index + move_pattern.row_delta,
                king_coordinate.column_index + move_pattern.column_delta,
            )
            if not is_coordinate_in_bounds(current_coordinate):
                continue

            if board.is_occupied(current_coordinate):
                current_piece = board.get_piece(current_coordinate)
                assert current_piece is not None
                if current_piece.color == king_color:
                    continue

            escape_coordinates.append(current_coordinate)
        return escape_coordinates
