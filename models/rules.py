from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_generator import MoveGenerator
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook
from utils.bit_utils import intersects
from utils.board_utils import enumerate_mask, is_diagonal, is_orthogonal

LEGAL_KNIGHT_MOVE_PATTERNS = [
    (1, 2),
    (-1, 2),
    (1, -2),
    (-1, -2),
    (2, 1),
    (-2, 1),
    (2, -1),
    (-2, -1),
]
LEGAL_KING_MOVE_PATTERNS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 1),
    (-1, 1),
    (1, -1),
    (-1, -1),
]


# TODO: cache check/checkmate/stalemate/cand_moves/legal_moves?
class Rules:
    @staticmethod
    def can_promote(move: Move) -> bool:
        moved_pawn = isinstance(move.from_piece, Pawn)
        return moved_pawn and Board.moving_to_final_row(move)

    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        king_square = (
            board._white_king_bitboard
            if color is Color.WHITE
            else board._black_king_bitboard
        )
        return (
            MoveGenerator.calculate_attacker_squares_mask(
                king_square, color.opposite, board
            )
            != 0
        )

    @classmethod
    def is_in_check_after_move(cls, move: Move, board: Board) -> bool:
        """Return whether the color is in check after the move."""
        board.make_move(move)
        is_in_check = cls.is_in_check(move.color, board)
        board.undo_move(move)
        return is_in_check

    @classmethod
    def is_legal_move(cls, move: Move, board: Board) -> bool:
        """Return whether the valid move is legal."""
        match move.from_piece:
            case Pawn():
                return cls.is_legal_pawn_move(move)
            case Knight():
                return cls.is_legal_knight_move(move)
            case Bishop():
                return cls.is_legal_bishop_move(move, board)
            case Rook():
                return cls.is_legal_rook_move(move, board)
            case Queen():
                return cls.is_legal_queen_move(move, board)
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
        return (row_delta, column_delta) in LEGAL_KNIGHT_MOVE_PATTERNS

    @staticmethod
    def is_legal_bishop_move(move: Move, board: Board) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)

        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        if not is_diagonal(row_delta, column_delta):
            return False

        intermediate_squares_mask = MoveGenerator.calculate_intermediate_squares_mask(
            move.from_square_mask, move.to_square_mask
        )
        board_mask = board.get_mask()
        if intersects(intermediate_squares_mask, board_mask):
            return False

        return True

    @staticmethod
    def is_legal_rook_move(move: Move, board: Board) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)

        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        if not is_orthogonal(row_delta, column_delta):
            return False

        intermediate_squares_mask = MoveGenerator.calculate_intermediate_squares_mask(
            move.from_square_mask, move.to_square_mask
        )
        board_mask = board.get_mask()
        if intersects(intermediate_squares_mask, board_mask):
            return False

        return True

    @classmethod
    def is_legal_queen_move(cls, move: Move, board: Board) -> bool:
        return cls.is_legal_bishop_move(move, board) or cls.is_legal_rook_move(
            move, board
        )

    @staticmethod
    def is_legal_king_move(move: Move) -> bool:
        from_coordinate = Coordinate.from_mask(move.from_square_mask)
        to_coordinate = Coordinate.from_mask(move.to_square_mask)
        row_delta = from_coordinate.row_index - to_coordinate.row_index
        column_delta = from_coordinate.column_index - to_coordinate.column_index
        return (row_delta, column_delta) in LEGAL_KING_MOVE_PATTERNS

    @staticmethod
    def generate_legal_moves(color: Color, board: Board) -> list[Move]:
        legal_moves = []
        candidate_moves = MoveGenerator.generate_candidate_moves(color, board)
        for move in candidate_moves:
            board.make_move(move)
            is_in_check = Rules.is_in_check(color, board)
            board.undo_move(move)
            if not is_in_check:
                legal_moves.append(move)
        return legal_moves

    # TODO: optimize gen_legal_moves and gen_cand_moves with generators
    @classmethod
    def is_in_checkmate(cls, color: Color, board: Board) -> bool:
        return (
            cls.is_in_check(color, board)
            and len(cls.generate_legal_moves(color, board)) == 0
        )

    @classmethod
    def is_in_stalemate(cls, color: Color, board: Board) -> bool:
        return (
            not cls.is_in_check(color, board)
            and len(cls.generate_legal_moves(color, board)) == 0
        )
