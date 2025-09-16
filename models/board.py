from enums.piece import Piece
from models.coordinate import Coordinate
from models.move import Move

_BOARD_SIZE = 8

_WHITE_PAWN_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
)
_WHITE_KNIGHT_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
)
_WHITE_BISHOP_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
)
_WHITE_ROOK_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
)
_WHITE_QUEEN_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
)
_WHITE_KING_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
)

_BLACK_PAWN_INITIAL_MASK = (
    0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
)
_BLACK_KNIGHT_INITIAL_MASK = (
    0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
_BLACK_BISHOP_INITIAL_MASK = (
    0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
_BLACK_ROOK_INITIAL_MASK = (
    0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
_BLACK_QUEEN_INITIAL_MASK = (
    0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)
_BLACK_KING_INITIAL_MASK = (
    0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
)

_WHITE_KING_INITIAL_OFFSET = 4
_BLACK_KING_INITIAL_OFFSET = 60


class Board:
    SIZE = _BOARD_SIZE

    def __init__(self) -> None:
        self._white_pawn_mask = 0
        self._white_knight_mask = 0
        self._white_bishop_mask = 0
        self._white_rook_mask = 0
        self._white_queen_mask = 0
        self._white_king_mask = 0

        self._black_pawn_mask = 0
        self._black_knight_mask = 0
        self._black_bishop_mask = 0
        self._black_rook_mask = 0
        self._black_queen_mask = 0
        self._black_king_mask = 0

        self._white_king_offset = -1
        self._black_king_offset = -1

    def set_up_pieces(self) -> None:
        self._white_pawn_mask = _WHITE_PAWN_INITIAL_MASK
        self._white_knight_mask = _WHITE_KNIGHT_INITIAL_MASK
        self._white_bishop_mask = _WHITE_BISHOP_INITIAL_MASK
        self._white_rook_mask = _WHITE_ROOK_INITIAL_MASK
        self._white_queen_mask = _WHITE_QUEEN_INITIAL_MASK
        self._white_king_mask = _WHITE_KING_INITIAL_MASK

        self._black_pawn_mask = _BLACK_PAWN_INITIAL_MASK
        self._black_knight_mask = _BLACK_KNIGHT_INITIAL_MASK
        self._black_bishop_mask = _BLACK_BISHOP_INITIAL_MASK
        self._black_rook_mask = _BLACK_ROOK_INITIAL_MASK
        self._black_queen_mask = _BLACK_QUEEN_INITIAL_MASK
        self._black_king_mask = _BLACK_KING_INITIAL_MASK

        self._white_king_offset = _WHITE_KING_INITIAL_OFFSET
        self._black_king_offset = _BLACK_KING_INITIAL_OFFSET

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        mask = self._get_mask_from_coordinate(coordinate)

        if self._white_pawn_mask & mask:
            return Piece.WHITE_PAWN
        if self._white_knight_mask & mask:
            return Piece.WHITE_KNIGHT
        if self._white_bishop_mask & mask:
            return Piece.WHITE_BISHOP
        if self._white_rook_mask & mask:
            return Piece.WHITE_ROOK
        if self._white_queen_mask & mask:
            return Piece.WHITE_QUEEN
        if self._white_king_mask & mask:
            return Piece.WHITE_KING

        if self._black_pawn_mask & mask:
            return Piece.BLACK_PAWN
        if self._black_knight_mask & mask:
            return Piece.BLACK_KNIGHT
        if self._black_bishop_mask & mask:
            return Piece.BLACK_BISHOP
        if self._black_rook_mask & mask:
            return Piece.BLACK_ROOK
        if self._black_queen_mask & mask:
            return Piece.BLACK_QUEEN
        if self._black_king_mask & mask:
            return Piece.BLACK_KING

        return None

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        mask = self._get_mask_from_coordinate(coordinate)
        self._clear_bit_from_piece_masks(mask)

        if piece is None:
            return

        if piece is Piece.WHITE_PAWN:
            self._white_pawn_mask |= mask
        elif piece is Piece.WHITE_KNIGHT:
            self._white_knight_mask |= mask
        elif piece is Piece.WHITE_BISHOP:
            self._white_bishop_mask |= mask
        elif piece is Piece.WHITE_ROOK:
            self._white_rook_mask |= mask
        elif piece is Piece.WHITE_QUEEN:
            self._white_queen_mask |= mask
        elif piece is Piece.WHITE_KING:
            self._white_king_mask |= mask

        elif piece is Piece.BLACK_PAWN:
            self._black_pawn_mask |= mask
        elif piece is Piece.BLACK_KNIGHT:
            self._black_knight_mask |= mask
        elif piece is Piece.BLACK_BISHOP:
            self._black_bishop_mask |= mask
        elif piece is Piece.BLACK_ROOK:
            self._black_rook_mask |= mask
        elif piece is Piece.BLACK_QUEEN:
            self._black_queen_mask |= mask
        elif piece is Piece.BLACK_KING:
            self._black_king_mask |= mask

    def make_move(self, move: Move) -> None:
        piece = self.get_piece(move.from_coordinate)
        self.set_piece(move.from_coordinate, None)
        self.set_piece(move.to_coordinate, piece)

        to_offset = self._get_offset_from_coordinate(move.to_coordinate)

        if piece is Piece.WHITE_KING:
            self._white_king_offset = to_offset
        elif piece is Piece.BLACK_KING:
            self._black_king_offset = to_offset

    def undo_move(self, move: Move) -> None:
        raise NotImplementedError

    def _get_offset_from_coordinate(self, coordinate: Coordinate) -> int:
        return self.SIZE * coordinate.row_index + coordinate.column_index

    def _get_mask_from_coordinate(self, coordinate: Coordinate) -> int:
        return 1 << self._get_offset_from_coordinate(coordinate)

    def _clear_bit_from_piece_masks(self, mask: int) -> None:
        self._white_pawn_mask &= ~mask
        self._white_knight_mask &= ~mask
        self._white_bishop_mask &= ~mask
        self._white_rook_mask &= ~mask
        self._white_queen_mask &= ~mask
        self._white_king_mask &= ~mask

        self._black_pawn_mask &= ~mask
        self._black_knight_mask &= ~mask
        self._black_bishop_mask &= ~mask
        self._black_rook_mask &= ~mask
        self._black_queen_mask &= ~mask
        self._black_king_mask &= ~mask
