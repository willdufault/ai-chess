from models.board import Board
from models.move import Move


class MoveValidator:
    """Handles move validation checking."""

    @staticmethod
    def is_move_valid(move: Move, board: Board) -> bool:
        """Return whether the move is valid, ignoring discovered check."""
        if not MoveValidator._does_move_pass_basic_checks(move, board):
            return False

        assert move.from_piece is not None
        return move.from_piece.move_strategy.is_valid_move(move, board)

    @staticmethod
    def _does_move_pass_basic_checks(move: Move, board: Board) -> bool:
        """Return whether the move passes basic validity checks."""
        are_coords_in_bounds = Board.is_coordinate_in_bounds(
            move.from_coordinate
        ) and board.is_coordinate_in_bounds(move.to_coordinate)
        if not are_coords_in_bounds:
            return False

        is_moving_wrong_piece = (
            move.from_piece is None or move.from_piece.color != move.color
        )
        if is_moving_wrong_piece:
            return False

        is_capturing_same_color = (
            move.to_piece is not None and move.to_piece.color == move.color
        )
        if is_capturing_same_color:
            return False

        return True
