import random

from constants.board_constants import BOARD_LEN, BOARD_SIZE
from constants.piece_constants import PIECE_TYPE_COUNT
from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.bit_utils import get_shift, intersects
from utils.board_utils import enumerate_mask, get_mask

# fmt: off
_WHITE_PAWN_INITIAL_BITBOARD = 0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
_WHITE_KNIGHT_INITIAL_BITBOARD = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
_WHITE_BISHOP_INITIAL_BITBOARD = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
_WHITE_ROOK_INITIAL_BITBOARD = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
_WHITE_QUEEN_INITIAL_BITBOARD = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
_WHITE_KING_INITIAL_BITBOARD = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000

_BLACK_PAWN_INITIAL_BITBOARD = 0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
_BLACK_ROOK_INITIAL_BITBOARD = 0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
_BLACK_KNIGHT_INITIAL_BITBOARD = 0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
_BLACK_BISHOP_INITIAL_BITBOARD = 0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
_BLACK_QUEEN_INITIAL_BITBOARD = 0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
_BLACK_KING_INITIAL_BITBOARD = 0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000

_FIRST_ROW_MASK = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111
_LAST_ROW_MASK = 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000
# fmt: on

_WHITE_PAWN = Pawn(Color.WHITE)
_WHITE_KNIGHT = Knight(Color.WHITE)
_WHITE_BISHOP = Bishop(Color.WHITE)
_WHITE_ROOK = Rook(Color.WHITE)
_WHITE_QUEEN = Queen(Color.WHITE)
_WHITE_KING = King(Color.WHITE)

_BLACK_PAWN = Pawn(Color.BLACK)
_BLACK_KNIGHT = Knight(Color.BLACK)
_BLACK_BISHOP = Bishop(Color.BLACK)
_BLACK_ROOK = Rook(Color.BLACK)
_BLACK_QUEEN = Queen(Color.BLACK)
_BLACK_KING = King(Color.BLACK)

_ZOBRIST_INDEX_WHITE_PAWN = 0
_ZOBRIST_INDEX_WHITE_KNIGHT = 1
_ZOBRIST_INDEX_WHITE_BISHOP = 2
_ZOBRIST_INDEX_WHITE_ROOK = 3
_ZOBRIST_INDEX_WHITE_QUEEN = 4
_ZOBRIST_INDEX_WHITE_KING = 5

_ZOBRIST_INDEX_BLACK_PAWN = 6
_ZOBRIST_INDEX_BLACK_KNIGHT = 7
_ZOBRIST_INDEX_BLACK_BISHOP = 8
_ZOBRIST_INDEX_BLACK_ROOK = 9
_ZOBRIST_INDEX_BLACK_QUEEN = 10
_ZOBRIST_INDEX_BLACK_KING = 11

_ZOBRIST_HASH_BITS = 64


class Board:
    SIZE = BOARD_SIZE
    LEN = BOARD_LEN
    _ZOBRIST_MATRIX = [
        [random.getrandbits(_ZOBRIST_HASH_BITS) for _ in range(PIECE_TYPE_COUNT)]
        for _ in range(BOARD_LEN)
    ]

    def __init__(self) -> None:
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

    def __hash__(self) -> int:
        return self._calculate_zobrist_hash()

    def set_up_pieces(self) -> None:
        self._white_pawn_bitboard = _WHITE_PAWN_INITIAL_BITBOARD
        self._white_knight_bitboard = _WHITE_KNIGHT_INITIAL_BITBOARD
        self._white_bishop_bitboard = _WHITE_BISHOP_INITIAL_BITBOARD
        self._white_rook_bitboard = _WHITE_ROOK_INITIAL_BITBOARD
        self._white_queen_bitboard = _WHITE_QUEEN_INITIAL_BITBOARD
        self._white_king_bitboard = _WHITE_KING_INITIAL_BITBOARD

        self._black_pawn_bitboard = _BLACK_PAWN_INITIAL_BITBOARD
        self._black_rook_bitboard = _BLACK_ROOK_INITIAL_BITBOARD
        self._black_knight_bitboard = _BLACK_KNIGHT_INITIAL_BITBOARD
        self._black_bishop_bitboard = _BLACK_BISHOP_INITIAL_BITBOARD
        self._black_queen_bitboard = _BLACK_QUEEN_INITIAL_BITBOARD
        self._black_king_bitboard = _BLACK_KING_INITIAL_BITBOARD

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        square_mask = get_mask(coordinate.row_index, coordinate.column_index)
        return self._get_piece(square_mask)

    def set_piece(self, piece: Piece | None, coordinate: Coordinate) -> None:
        square_mask = get_mask(coordinate.row_index, coordinate.column_index)
        return self._set_piece(piece, square_mask)

    def is_occupied(self, square_mask: int, color: Color | None = None) -> bool:
        """Return whether the square is occupied by the color. Check both colors
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

    def get_mask(self, color: Color | None = None):
        """Return a mask with all pieces of the color. Check both colors if not
        specified."""
        white_mask = (
            self._white_pawn_bitboard
            | self._white_knight_bitboard
            | self._white_bishop_bitboard
            | self._white_rook_bitboard
            | self._white_queen_bitboard
            | self._white_king_bitboard
        )
        black_mask = (
            self._black_pawn_bitboard
            | self._black_knight_bitboard
            | self._black_bishop_bitboard
            | self._black_rook_bitboard
            | self._black_queen_bitboard
            | self._black_king_bitboard
        )

        if color == Color.WHITE:
            return white_mask
        elif color == Color.BLACK:
            return black_mask
        else:
            return white_mask | black_mask

    def make_move(self, move: Move) -> None:
        self._set_piece(None, move.from_square_mask)
        self._set_piece(move.from_piece, move.to_square_mask)

    def undo_move(self, move: Move) -> None:
        self._set_piece(move.from_piece, move.from_square_mask)
        self._set_piece(move.to_piece, move.to_square_mask)

    @staticmethod
    def moving_to_final_row(move: Move) -> bool:
        final_row_mask = (
            _LAST_ROW_MASK if move.color == Color.WHITE else _FIRST_ROW_MASK
        )
        return intersects(move.to_square_mask, final_row_mask)

    def _get_piece(self, square_mask: int) -> Piece | None:
        if intersects(self._white_pawn_bitboard, square_mask):
            return _WHITE_PAWN
        elif intersects(self._white_knight_bitboard, square_mask):
            return _WHITE_KNIGHT
        elif intersects(self._white_bishop_bitboard, square_mask):
            return _WHITE_BISHOP
        elif intersects(self._white_rook_bitboard, square_mask):
            return _WHITE_ROOK
        elif intersects(self._white_queen_bitboard, square_mask):
            return _WHITE_QUEEN
        elif intersects(self._white_king_bitboard, square_mask):
            return _WHITE_KING

        elif intersects(self._black_pawn_bitboard, square_mask):
            return _BLACK_PAWN
        elif intersects(self._black_knight_bitboard, square_mask):
            return _BLACK_KNIGHT
        elif intersects(self._black_bishop_bitboard, square_mask):
            return _BLACK_BISHOP
        elif intersects(self._black_rook_bitboard, square_mask):
            return _BLACK_ROOK
        elif intersects(self._black_queen_bitboard, square_mask):
            return _BLACK_QUEEN
        elif intersects(self._black_king_bitboard, square_mask):
            return _BLACK_KING

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
        self._black_king_bitboard &= ~square_mask

    def _calculate_zobrist_hash(self) -> int:
        value = 0
        for square_mask in enumerate_mask(self.get_mask()):
            shift = get_shift(square_mask)

            if intersects(square_mask, self._white_pawn_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_WHITE_PAWN]
            elif intersects(square_mask, self._white_knight_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_WHITE_KNIGHT]
            elif intersects(square_mask, self._white_bishop_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_WHITE_BISHOP]
            elif intersects(square_mask, self._white_rook_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_WHITE_ROOK]
            elif intersects(square_mask, self._white_queen_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_WHITE_QUEEN]
            elif intersects(square_mask, self._white_king_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_WHITE_KING]

            elif intersects(square_mask, self._black_pawn_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_BLACK_PAWN]
            elif intersects(square_mask, self._black_knight_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_BLACK_KNIGHT]
            elif intersects(square_mask, self._black_bishop_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_BLACK_BISHOP]
            elif intersects(square_mask, self._black_rook_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_BLACK_ROOK]
            elif intersects(square_mask, self._black_queen_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_BLACK_QUEEN]
            elif intersects(square_mask, self._black_king_bitboard):
                value ^= self._ZOBRIST_MATRIX[shift][_ZOBRIST_INDEX_BLACK_KING]
        return value
