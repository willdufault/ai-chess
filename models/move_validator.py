from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook
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
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)
        are_both_coordinates_in_bounds = is_coordinate_in_bounds(
            from_coordinate
        ) and is_coordinate_in_bounds(to_coordinate)
        if not are_both_coordinates_in_bounds:
            return False

        if move.from_piece is None or move.from_piece.color != move.color:
            return False

        if move.to_piece is not None and move.to_piece.color == move.color:
            return False

        return True

    @classmethod
    def is_legal_move(cls, move: Move) -> bool:
        match move.from_piece:
            case Pawn():
                return cls.is_legal_pawn_move(move)
            case Knight():
                return cls.is_legal_knight_move(move)
            case Bishop():
                return cls.is_legal_bishop_move(move)
            case Rook():
                return cls.is_legal_rook_move(move)
            case Queen():
                return cls.is_legal_queen_move(move)
            case King():
                return cls.is_legal_king_move(move)
            case _:
                raise ValueError(f"Invalid piece type: {move.from_piece}")

    @staticmethod
    def is_legal_pawn_move(move: Move) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)

        moving_forward_one = (
            from_coordinate.row_index + move.color.forward_row_delta
            == to_coordinate.row_index
        )
        if not moving_forward_one:
            return False

        is_same_column = from_coordinate.column_index == to_coordinate.column_index
        moving_to_empty_square = move.to_piece is None
        if is_same_column and moving_to_empty_square:
            return True

        is_adjacent_column = (
            abs(from_coordinate.column_index - to_coordinate.column_index) == 1
        )
        capturing_opponent_piece = (
            move.to_piece is not None and move.to_piece.color != move.color
        )
        if is_adjacent_column and capturing_opponent_piece:
            return True

        return False

    @staticmethod
    def is_legal_knight_move(move: Move) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)
        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        return (row_delta, column_delta) in VALID_KNIGHT_MOVE_PATTERNS

    @staticmethod
    def is_legal_bishop_move(move: Move) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)
        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        is_along_diagonal = abs(row_delta) == abs(column_delta)
        return is_along_diagonal

    @staticmethod
    def is_legal_rook_move(move: Move) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)
        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        is_orthogonal = (row_delta, column_delta).count(0) == 1
        return is_orthogonal

    @classmethod
    def is_legal_queen_move(cls, move: Move) -> bool:
        return cls.is_legal_bishop_move(move) or cls.is_legal_rook_move(move)

    @staticmethod
    def is_legal_king_move(move: Move) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)
        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        return (row_delta, column_delta) in VALID_KING_MOVE_PATTERNS
