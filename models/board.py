from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
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
    SIZE = BOARD_SIZE

    def __init__(self) -> None:
        self._white_pawn_mask = 0
        self._white_knight_mask = 0
        self._white_bishop_mask = 0
        self._white_rook_mask = 0
        self._white_queen_mask = 0
        self._white_king_mask = 0
        self._white_pieces_mask = 0

        self._black_pawn_mask = 0
        self._black_knight_mask = 0
        self._black_bishop_mask = 0
        self._black_rook_mask = 0
        self._black_queen_mask = 0
        self._black_king_mask = 0
        self._black_pieces_mask = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False
        return self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)

    @property
    def state(self) -> tuple[int, ...]:
        return (
            self._white_pawn_mask,
            self._white_knight_mask,
            self._white_bishop_mask,
            self._white_rook_mask,
            self._white_queen_mask,
            self._white_king_mask,
            self._black_pawn_mask,
            self._black_knight_mask,
            self._black_bishop_mask,
            self._black_rook_mask,
            self._black_queen_mask,
            self._black_king_mask,
        )

    def generate_white_pawn_moves(self) -> list[Move]:
        moves = []
        for offset in range(_BOARD_LEN - BOARD_SIZE):
            from_mask = 1 << offset
            is_white_pawn = from_mask & self._white_pawn_mask
            if not is_white_pawn:
                continue

            to_mask = from_mask << BOARD_SIZE
            if self._is_square_occupied(to_mask):
                continue

            from_coordinate = self._get_coordinate_from_mask(from_mask)
            to_coordinate = self._get_coordinate_from_mask(to_mask)
            move = Move(Color.WHITE, from_coordinate, to_coordinate)
            moves.append(move)
        return moves

    def generate_black_pawn_moves(self) -> list[Move]:
        moves = []
        for offset in range(BOARD_SIZE, _BOARD_LEN):
            from_mask = 1 << offset
            is_black_pawn = from_mask & self._white_pawn_mask
            if not is_black_pawn:
                continue

            to_mask = from_mask >> BOARD_SIZE
            if self._is_square_occupied(to_mask):
                continue

            from_coordinate = self._get_coordinate_from_mask(from_mask)
            to_coordinate = self._get_coordinate_from_mask(to_mask)
            move = Move(Color.WHITE, from_coordinate, to_coordinate)
            moves.append(move)
        return moves

    def set_up_pieces(self) -> None:
        self._white_pawn_mask = _WHITE_PAWN_INITIAL_MASK
        self._white_knight_mask = _WHITE_KNIGHT_INITIAL_MASK
        self._white_bishop_mask = _WHITE_BISHOP_INITIAL_MASK
        self._white_rook_mask = _WHITE_ROOK_INITIAL_MASK
        self._white_queen_mask = _WHITE_QUEEN_INITIAL_MASK
        self._white_king_mask = _WHITE_KING_INITIAL_MASK
        self._white_pieces_mask = _WHITE_PIECES_INITIAL_MASK

        self._black_pawn_mask = _BLACK_PAWN_INITIAL_MASK
        self._black_knight_mask = _BLACK_KNIGHT_INITIAL_MASK
        self._black_bishop_mask = _BLACK_BISHOP_INITIAL_MASK
        self._black_rook_mask = _BLACK_ROOK_INITIAL_MASK
        self._black_queen_mask = _BLACK_QUEEN_INITIAL_MASK
        self._black_king_mask = _BLACK_KING_INITIAL_MASK
        self._black_pieces_mask = _BLACK_PIECES_INITIAL_MASK

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        mask = self._get_mask_from_coordinate(coordinate)

        if self._white_pawn_mask & mask > 0:
            return Pawn(Color.WHITE)
        if self._white_knight_mask & mask > 0:
            return Knight(Color.WHITE)
        if self._white_bishop_mask & mask > 0:
            return Bishop(Color.WHITE)
        if self._white_rook_mask & mask > 0:
            return Rook(Color.WHITE)
        if self._white_queen_mask & mask > 0:
            return Queen(Color.WHITE)
        if self._white_king_mask & mask > 0:
            return King(Color.WHITE)

        if self._black_pawn_mask & mask > 0:
            return Pawn(Color.BLACK)
        if self._black_knight_mask & mask > 0:
            return Knight(Color.BLACK)
        if self._black_bishop_mask & mask > 0:
            return Bishop(Color.BLACK)
        if self._black_rook_mask & mask > 0:
            return Rook(Color.BLACK)
        if self._black_queen_mask & mask > 0:
            return Queen(Color.BLACK)
        if self._black_king_mask & mask > 0:
            return King(Color.BLACK)

        return None

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        mask = self._get_mask_from_coordinate(coordinate)
        self._clear_bit(mask)

        if piece is None:
            return

        match piece:
            case Pawn(Color.WHITE):
                self._white_pawn_mask |= mask
            case Knight(Color.WHITE):
                self._white_knight_mask |= mask
            case Bishop(Color.WHITE):
                self._white_bishop_mask |= mask
            case Rook(Color.WHITE):
                self._white_rook_mask |= mask
            case Queen(Color.WHITE):
                self._white_queen_mask |= mask
            case King(Color.WHITE):
                self._white_king_mask |= mask

            case Pawn(Color.BLACK):
                self._black_pawn_mask |= mask
            case Knight(Color.BLACK):
                self._black_knight_mask |= mask
            case Bishop(Color.BLACK):
                self._black_bishop_mask |= mask
            case Rook(Color.BLACK):
                self._black_rook_mask |= mask
            case Queen(Color.BLACK):
                self._black_queen_mask |= mask
            case King(Color.BLACK):
                self._black_king_mask |= mask

        if piece.color is Color.WHITE:
            self._white_pieces_mask |= mask
        else:
            self._black_pieces_mask |= mask

    def make_move(self, move: Move) -> None:
        piece = self.get_piece(move.from_coordinate)
        self.set_piece(move.from_coordinate, None)
        self.set_piece(move.to_coordinate, piece)

    def _get_mask_from_coordinate(self, coordinate: Coordinate) -> int:
        return 1 << (self.SIZE * coordinate.row_index + coordinate.column_index)

    def _get_coordinate_from_mask(self, mask: int) -> Coordinate:
        row_index, column_index = divmod(mask.bit_length() - 1, BOARD_SIZE)
        return Coordinate(row_index, column_index)

    def _clear_bit(self, mask: int) -> None:
        self._white_pawn_mask &= ~mask
        self._white_knight_mask &= ~mask
        self._white_bishop_mask &= ~mask
        self._white_rook_mask &= ~mask
        self._white_queen_mask &= ~mask
        self._white_king_mask &= ~mask
        self._white_pieces_mask &= ~mask

        self._black_pawn_mask &= ~mask
        self._black_knight_mask &= ~mask
        self._black_bishop_mask &= ~mask
        self._black_rook_mask &= ~mask
        self._black_queen_mask &= ~mask
        self._black_king_mask &= ~mask
        self._black_pieces_mask &= ~mask

    def _is_square_occupied(self, mask: int) -> bool:
        return mask & self._white_pieces_mask > 0 or mask & self._black_pieces_mask > 0
