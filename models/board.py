from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

_BOARD_SIZE = 8
_BOARD_LEN = 64

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
_WHITE_PIECES_INITIAL_MASK = (
    0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_11111111
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
_BLACK_PIECES_INITIAL_MASK = (
    0b11111111_11111111_00000000_00000000_00000000_00000000_00000000_00000000
)


class Board:
    SIZE = _BOARD_SIZE
    LEN = _BOARD_LEN

    def __init__(self) -> None:
        self.white_pawn_mask = 0
        self.white_knight_mask = 0
        self.white_bishop_mask = 0
        self.white_rook_mask = 0
        self.white_queen_mask = 0
        self.white_king_mask = 0
        self.white_pieces_mask = 0

        self.black_pawn_mask = 0
        self.black_knight_mask = 0
        self.black_bishop_mask = 0
        self.black_rook_mask = 0
        self.black_queen_mask = 0
        self.black_king_mask = 0
        self.black_pieces_mask = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False
        return self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)

    @property
    def state(self) -> tuple[int, ...]:
        return (
            self.white_pawn_mask,
            self.white_knight_mask,
            self.white_bishop_mask,
            self.white_rook_mask,
            self.white_queen_mask,
            self.white_king_mask,
            self.black_pawn_mask,
            self.black_knight_mask,
            self.black_bishop_mask,
            self.black_rook_mask,
            self.black_queen_mask,
            self.black_king_mask,
        )

    def set_up_pieces(self) -> None:
        self.white_pawn_mask = _WHITE_PAWN_INITIAL_MASK
        self.white_knight_mask = _WHITE_KNIGHT_INITIAL_MASK
        self.white_bishop_mask = _WHITE_BISHOP_INITIAL_MASK
        self.white_rook_mask = _WHITE_ROOK_INITIAL_MASK
        self.white_queen_mask = _WHITE_QUEEN_INITIAL_MASK
        self.white_king_mask = _WHITE_KING_INITIAL_MASK
        self.white_pieces_mask = _WHITE_PIECES_INITIAL_MASK

        self.black_pawn_mask = _BLACK_PAWN_INITIAL_MASK
        self.black_knight_mask = _BLACK_KNIGHT_INITIAL_MASK
        self.black_bishop_mask = _BLACK_BISHOP_INITIAL_MASK
        self.black_rook_mask = _BLACK_ROOK_INITIAL_MASK
        self.black_queen_mask = _BLACK_QUEEN_INITIAL_MASK
        self.black_king_mask = _BLACK_KING_INITIAL_MASK
        self.black_pieces_mask = _BLACK_PIECES_INITIAL_MASK

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        mask = self._get_mask_from_coordinate(coordinate)

        if self.white_pawn_mask & mask > 0:
            return Pawn(Color.WHITE)
        if self.white_knight_mask & mask > 0:
            return Knight(Color.WHITE)
        if self.white_bishop_mask & mask > 0:
            return Bishop(Color.WHITE)
        if self.white_rook_mask & mask > 0:
            return Rook(Color.WHITE)
        if self.white_queen_mask & mask > 0:
            return Queen(Color.WHITE)
        if self.white_king_mask & mask > 0:
            return King(Color.WHITE)

        if self.black_pawn_mask & mask > 0:
            return Pawn(Color.BLACK)
        if self.black_knight_mask & mask > 0:
            return Knight(Color.BLACK)
        if self.black_bishop_mask & mask > 0:
            return Bishop(Color.BLACK)
        if self.black_rook_mask & mask > 0:
            return Rook(Color.BLACK)
        if self.black_queen_mask & mask > 0:
            return Queen(Color.BLACK)
        if self.black_king_mask & mask > 0:
            return King(Color.BLACK)

        return None

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        mask = self._get_mask_from_coordinate(coordinate)
        self._clear_bit(mask)

        if piece is None:
            return

        match piece:
            case Pawn(Color.WHITE):
                self.white_pawn_mask |= mask
            case Knight(Color.WHITE):
                self.white_knight_mask |= mask
            case Bishop(Color.WHITE):
                self.white_bishop_mask |= mask
            case Rook(Color.WHITE):
                self.white_rook_mask |= mask
            case Queen(Color.WHITE):
                self.white_queen_mask |= mask
            case King(Color.WHITE):
                self.white_king_mask |= mask

            case Pawn(Color.BLACK):
                self.black_pawn_mask |= mask
            case Knight(Color.BLACK):
                self.black_knight_mask |= mask
            case Bishop(Color.BLACK):
                self.black_bishop_mask |= mask
            case Rook(Color.BLACK):
                self.black_rook_mask |= mask
            case Queen(Color.BLACK):
                self.black_queen_mask |= mask
            case King(Color.BLACK):
                self.black_king_mask |= mask

        if piece.color is Color.WHITE:
            self.white_pieces_mask |= mask
        else:
            self.black_pieces_mask |= mask

    def make_move(self, move: Move) -> None:
        piece = self.get_piece(move.from_coordinate)
        self.set_piece(move.from_coordinate, None)
        self.set_piece(move.to_coordinate, piece)

    def get_coordinate_from_mask(self, mask: int) -> Coordinate:
        row_index, column_index = divmod(mask.bit_length() - 1, _BOARD_SIZE)
        return Coordinate(row_index, column_index)

    def is_white_piece_on_square(self, mask: int) -> bool:
        return mask & self.white_pieces_mask > 0

    def is_black_piece_on_square(self, mask: int) -> bool:
        return mask & self.black_pieces_mask > 0

    def is_square_occupied(self, mask: int) -> bool:
        return self.is_white_piece_on_square(mask) or self.is_black_piece_on_square(
            mask
        )

    def _get_mask_from_coordinate(self, coordinate: Coordinate) -> int:
        return 1 << (self.SIZE * coordinate.row_index + coordinate.column_index)

    def _clear_bit(self, mask: int) -> None:
        self.white_pawn_mask &= ~mask
        self.white_knight_mask &= ~mask
        self.white_bishop_mask &= ~mask
        self.white_rook_mask &= ~mask
        self.white_queen_mask &= ~mask
        self.white_king_mask &= ~mask
        self.white_pieces_mask &= ~mask

        self.black_pawn_mask &= ~mask
        self.black_knight_mask &= ~mask
        self.black_bishop_mask &= ~mask
        self.black_rook_mask &= ~mask
        self.black_queen_mask &= ~mask
        self.black_king_mask &= ~mask
        self.black_pieces_mask &= ~mask
