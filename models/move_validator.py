from models.move import Move
from utils.board_utils import is_coordinate_in_bounds

VALID_KNIGHT_MOVE_PATTERNS = [
    (1, 2),
    (-1, 2),
    (1, -2),
    (-1, -2),
    (2, 1),
    (-2, 1),
    (2, -1),
    (-2, -1),
]
VALID_KING_MOVE_PATTERNS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 1),
    (-1, 1),
    (1, -1),
    (-1, -1),
]


# TODO: mark necessary methods as private
class MoveValidator:
    @staticmethod
    def is_valid_move(move: Move) -> bool:
        are_coordinates_in_bounds = is_coordinate_in_bounds(
            move.from_coordinate
        ) and is_coordinate_in_bounds(move.to_coordinate)
        if not are_coordinates_in_bounds:
            return False

        if move.from_piece is None or move.from_piece.color != move.color:
            return False

        if move.to_piece is not None and move.to_piece.color == move.color:
            return False

        return True

    @staticmethod
    def is_valid_pawn_move(move: Move) -> bool:
        moving_forward_one = (
            move.from_coordinate.row_index + move.color.forward_row_delta
            == move.to_coordinate.row_index
        )
        if not moving_forward_one:
            return False

        is_same_column = (
            move.from_coordinate.column_index == move.to_coordinate.column_index
        )
        moving_to_empty_square = move.to_piece is None
        if is_same_column and moving_to_empty_square:
            return True

        is_adjacent_column = (
            abs(move.from_coordinate.column_index - move.to_coordinate.column_index)
            == 1
        )
        capturing_opponent_piece = (
            move.to_piece is not None and move.to_piece.color != move.color
        )
        if is_adjacent_column and capturing_opponent_piece:
            return True

        return False

    @staticmethod
    def is_valid_knight_move(move: Move) -> bool:
        row_delta = move.from_coordinate.row_index - move.to_coordinate.row_index
        column_delta = (
            move.from_coordinate.column_index - move.to_coordinate.column_index
        )
        return (row_delta, column_delta) in VALID_KNIGHT_MOVE_PATTERNS

    @staticmethod
    def is_valid_bishop_move(move: Move) -> bool:
        row_delta = move.from_coordinate.row_index - move.to_coordinate.row_index
        column_delta = (
            move.from_coordinate.column_index - move.to_coordinate.column_index
        )
        is_along_diagonal = abs(row_delta) == abs(column_delta)
        return is_along_diagonal

    @staticmethod
    def is_valid_rook_move(move: Move) -> bool:
        row_delta = move.from_coordinate.row_index - move.to_coordinate.row_index
        column_delta = (
            move.from_coordinate.column_index - move.to_coordinate.column_index
        )
        is_orthogonal = (row_delta, column_delta).count(0) == 1
        return is_orthogonal

    @classmethod
    def is_valid_queen_move(cls, move: Move) -> bool:
        return cls.is_valid_bishop_move(move) or cls.is_valid_rook_move(move)

    @staticmethod
    def is_valid_king_move(move: Move) -> bool:
        row_delta = move.from_coordinate.row_index - move.to_coordinate.row_index
        column_delta = (
            move.from_coordinate.column_index - move.to_coordinate.column_index
        )
        return (row_delta, column_delta) in VALID_KING_MOVE_PATTERNS
