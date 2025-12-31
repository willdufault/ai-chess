from constants.board_constants import BOARD_SIZE
from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.bit_utils import intersects
from utils.board_utils import calculate_mask

WHITE_PAWN_INITIAL_BITBOARD = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
)
WHITE_KNIGHT_INITIAL_BITBOARD = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
)
WHITE_BISHOP_INITIAL_BITBOARD = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
)
WHITE_ROOK_INITIAL_BITBOARD = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
)
WHITE_QUEEN_INITIAL_BITBOARD = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
)
WHITE_KING_INITIAL_BITBOARD = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
)

BLACK_PAWN_INITIAL_BITBOARD = (
    0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
)
BLACK_ROOK_INITIAL_BITBOARD = (
    0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
BLACK_KNIGHT_INITIAL_BITBOARD = (
    0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
BLACK_BISHOP_INITIAL_BITBOARD = (
    0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
BLACK_QUEEN_INITIAL_BITBOARD = (
    0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
BLACK_KING_INITIAL_BITBOARD = (
    0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)

FIRST_ROW_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111
)
LAST_ROW_MASK = (
    0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)


class Board:
    def __init__(self) -> None:
        self.size = BOARD_SIZE

        self._white_pawn_bitboard = 0
        self._white_knight_bitboard = 0
        self._white_bishop_bitboard = 0
        self._white_rook_bitboard = 0
        self._white_queen_bitboard = 0
        self._white_king_bitboard = 0

        self._black_pawn_bitboard = 0
        self._black_knight_bitboard = 0
        self._black_bishop_bitboard = 0
        self._black_rook_bitboard = 0
        self._black_queen_bitboard = 0
        self._black_king_bitboard = 0

    def set_up_pieces(self) -> None:
        self._white_pawn_bitboard = WHITE_PAWN_INITIAL_BITBOARD
        self._white_knight_bitboard = WHITE_KNIGHT_INITIAL_BITBOARD
        self._white_bishop_bitboard = WHITE_BISHOP_INITIAL_BITBOARD
        self._white_rook_bitboard = WHITE_ROOK_INITIAL_BITBOARD
        self._white_queen_bitboard = WHITE_QUEEN_INITIAL_BITBOARD
        self._white_king_bitboard = WHITE_KING_INITIAL_BITBOARD

        self._black_pawn_bitboard = BLACK_PAWN_INITIAL_BITBOARD
        self._black_rook_bitboard = BLACK_ROOK_INITIAL_BITBOARD
        self._black_knight_bitboard = BLACK_KNIGHT_INITIAL_BITBOARD
        self._black_bishop_bitboard = BLACK_BISHOP_INITIAL_BITBOARD
        self._black_queen_bitboard = BLACK_QUEEN_INITIAL_BITBOARD
        self._black_king_bitboard = BLACK_KING_INITIAL_BITBOARD

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        square_mask = calculate_mask(coordinate.row_index, coordinate.column_index)
        return self._get_piece(square_mask)

    def set_piece(self, piece: Piece | None, coordinate: Coordinate) -> None:
        square_mask = calculate_mask(coordinate.row_index, coordinate.column_index)
        return self._set_piece(piece, square_mask)

    def is_occupied(self, square_mask: int, color: Color | None = None) -> bool:
        """Return whether the square is occupied by the color. Checks both colors
        if not specified."""
        is_occupied_by_white = (
            intersects(self._white_pawn_bitboard, square_mask)
            or intersects(self._white_knight_bitboard, square_mask)
            or intersects(self._white_bishop_bitboard, square_mask)
            or intersects(self._white_rook_bitboard, square_mask)
            or intersects(self._white_queen_bitboard, square_mask)
            or intersects(self._white_king_bitboard, square_mask)
        )
        is_occupied_by_black = (
            intersects(self._black_pawn_bitboard, square_mask)
            or intersects(self._black_knight_bitboard, square_mask)
            or intersects(self._black_bishop_bitboard, square_mask)
            or intersects(self._black_rook_bitboard, square_mask)
            or intersects(self._black_queen_bitboard, square_mask)
            or intersects(self._black_king_bitboard, square_mask)
        )

        if color == Color.WHITE:
            return is_occupied_by_white

        if color == Color.BLACK:
            return is_occupied_by_black

        return is_occupied_by_white or is_occupied_by_black

    def make_move(self, move: Move) -> None:
        self._set_piece(None, move.from_square_mask)
        self._set_piece(move.from_piece, move.to_square_mask)

    def undo_move(self, move: Move) -> None:
        self._set_piece(move.from_piece, move.from_square_mask)
        self._set_piece(move.to_piece, move.to_square_mask)

    @staticmethod
    def moving_to_final_row(move: Move) -> bool:
        final_row_mask = LAST_ROW_MASK if move.color == Color.WHITE else FIRST_ROW_MASK
        return intersects(move.to_square_mask, final_row_mask)

    def _get_piece(self, square_mask: int) -> Piece | None:
        if intersects(self._white_pawn_bitboard, square_mask):
            return Pawn(Color.WHITE)
        elif intersects(self._white_knight_bitboard, square_mask):
            return Knight(Color.WHITE)
        elif intersects(self._white_bishop_bitboard, square_mask):
            return Bishop(Color.WHITE)
        elif intersects(self._white_rook_bitboard, square_mask):
            return Rook(Color.WHITE)
        elif intersects(self._white_queen_bitboard, square_mask):
            return Queen(Color.WHITE)
        elif intersects(self._white_king_bitboard, square_mask):
            return King(Color.WHITE)

        elif intersects(self._black_pawn_bitboard, square_mask):
            return Pawn(Color.BLACK)
        elif intersects(self._black_knight_bitboard, square_mask):
            return Knight(Color.BLACK)
        elif intersects(self._black_bishop_bitboard, square_mask):
            return Bishop(Color.BLACK)
        elif intersects(self._black_rook_bitboard, square_mask):
            return Rook(Color.BLACK)
        elif intersects(self._black_queen_bitboard, square_mask):
            return Queen(Color.BLACK)
        elif intersects(self._black_king_bitboard, square_mask):
            return King(Color.BLACK)

        return None

    def _set_piece(self, piece: Piece | None, square_mask: int) -> None:
        self._clear_square(square_mask)

        if piece is None:
            return

        match piece:
            case Pawn():
                if piece.color == Color.WHITE:
                    self._white_pawn_bitboard |= square_mask
                else:
                    self._black_pawn_bitboard |= square_mask
            case Knight():
                if piece.color == Color.WHITE:
                    self._white_knight_bitboard |= square_mask
                else:
                    self._black_knight_bitboard |= square_mask
            case Bishop():
                if piece.color == Color.WHITE:
                    self._white_bishop_bitboard |= square_mask
                else:
                    self._black_bishop_bitboard |= square_mask
            case Rook():
                if piece.color == Color.WHITE:
                    self._white_rook_bitboard |= square_mask
                else:
                    self._black_rook_bitboard |= square_mask
            case Queen():
                if piece.color == Color.WHITE:
                    self._white_queen_bitboard |= square_mask
                else:
                    self._black_queen_bitboard |= square_mask
            case King():
                if piece.color == Color.WHITE:
                    self._white_king_bitboard |= square_mask
                else:
                    self._black_king_bitboard |= square_mask
            case _:
                raise ValueError(f"Invalid piece type: {piece}")

    def _clear_square(self, square_mask: int) -> None:
        self._white_pawn_bitboard &= ~square_mask
        self._white_knight_bitboard &= ~square_mask
        self._white_bishop_bitboard &= ~square_mask
        self._white_rook_bitboard &= ~square_mask
        self._white_queen_bitboard &= ~square_mask
        self._white_king_bitboard &= ~square_mask

        self._black_pawn_bitboard &= ~square_mask
        self._black_knight_bitboard &= ~square_mask
        self._black_bishop_bitboard &= ~square_mask
        self._black_rook_bitboard &= ~square_mask
        self._black_queen_bitboard &= ~square_mask
        self._black_king_bitboard &= ~square_mask
        self._black_rook_bitboard &= ~square_mask
        self._black_queen_bitboard &= ~square_mask
        self._black_king_bitboard &= ~square_mask
