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


class Board:
    def __init__(self) -> None:
        self.size = BOARD_SIZE

        self.white_pawn_bitboard = 0
        self.white_knight_bitboard = 0
        self.white_bishop_bitboard = 0
        self.white_rook_bitboard = 0
        self.white_queen_bitboard = 0
        self.white_king_bitboard = 0

        self.black_pawn_bitboard = 0
        self.black_knight_bitboard = 0
        self.black_bishop_bitboard = 0
        self.black_rook_bitboard = 0
        self.black_queen_bitboard = 0
        self.black_king_bitboard = 0

    def set_up_pieces(self) -> None:
        self.white_pawn_bitboard = WHITE_PAWN_INITIAL_BITBOARD
        self.white_knight_bitboard = WHITE_KNIGHT_INITIAL_BITBOARD
        self.white_bishop_bitboard = WHITE_BISHOP_INITIAL_BITBOARD
        self.white_rook_bitboard = WHITE_ROOK_INITIAL_BITBOARD
        self.white_queen_bitboard = WHITE_QUEEN_INITIAL_BITBOARD
        self.white_king_bitboard = WHITE_KING_INITIAL_BITBOARD

        self.black_pawn_bitboard = BLACK_PAWN_INITIAL_BITBOARD
        self.black_rook_bitboard = BLACK_ROOK_INITIAL_BITBOARD
        self.black_knight_bitboard = BLACK_KNIGHT_INITIAL_BITBOARD
        self.black_bishop_bitboard = BLACK_BISHOP_INITIAL_BITBOARD
        self.black_queen_bitboard = BLACK_QUEEN_INITIAL_BITBOARD
        self.black_king_bitboard = BLACK_KING_INITIAL_BITBOARD

    def print(self, color: Color) -> None:
        # Flip board based on team.
        if color == Color.WHITE:
            row_indexes = reversed(range(self.size))
            column_indexes = range(self.size)
        else:
            row_indexes = range(self.size)
            # Must be a list to not exhaust the iterator.
            column_indexes = list(reversed(range(self.size)))

        for row_index in row_indexes:
            for column_index in column_indexes:
                square_mask = calculate_mask(row_index, column_index)

                if intersects(self.white_pawn_bitboard, square_mask):
                    print("♙", end=" ")
                elif intersects(self.white_knight_bitboard, square_mask):
                    print("♘", end=" ")
                elif intersects(self.white_bishop_bitboard, square_mask):
                    print("♗", end=" ")
                elif intersects(self.white_rook_bitboard, square_mask):
                    print("♖", end=" ")
                elif intersects(self.white_queen_bitboard, square_mask):
                    print("♕", end=" ")
                elif intersects(self.white_king_bitboard, square_mask):
                    print("♔", end=" ")

                elif intersects(self.black_pawn_bitboard, square_mask):
                    print("♟", end=" ")
                elif intersects(self.black_knight_bitboard, square_mask):
                    print("♞", end=" ")
                elif intersects(self.black_bishop_bitboard, square_mask):
                    print("♝", end=" ")
                elif intersects(self.black_rook_bitboard, square_mask):
                    print("♜", end=" ")
                elif intersects(self.black_queen_bitboard, square_mask):
                    print("♛", end=" ")
                elif intersects(self.black_king_bitboard, square_mask):
                    print("♚", end=" ")
                else:
                    print(".", end=" ")
            print()

    def get_piece(
        self,
        coordinate: Coordinate | None = None,
        square_mask: int | None = None,
    ) -> Piece | None:
        if coordinate is None and square_mask is None:
            raise ValueError("Must provide either coordinate or square_mask.")

        if coordinate is not None and square_mask is not None:
            raise ValueError(
                "Must provide exactly one of either coordinate or square_mask."
            )

        if coordinate is not None:
            square_mask = calculate_mask(coordinate.row_index, coordinate.column_index)

        assert square_mask is not None

        if intersects(self.white_pawn_bitboard, square_mask):
            return Pawn(Color.WHITE)
        elif intersects(self.white_knight_bitboard, square_mask):
            return Knight(Color.WHITE)
        elif intersects(self.white_bishop_bitboard, square_mask):
            return Bishop(Color.WHITE)
        elif intersects(self.white_rook_bitboard, square_mask):
            return Rook(Color.WHITE)
        elif intersects(self.white_queen_bitboard, square_mask):
            return Queen(Color.WHITE)
        elif intersects(self.white_king_bitboard, square_mask):
            return King(Color.WHITE)

        elif intersects(self.black_pawn_bitboard, square_mask):
            return Pawn(Color.BLACK)
        elif intersects(self.black_knight_bitboard, square_mask):
            return Knight(Color.BLACK)
        elif intersects(self.black_bishop_bitboard, square_mask):
            return Bishop(Color.BLACK)
        elif intersects(self.black_rook_bitboard, square_mask):
            return Rook(Color.BLACK)
        elif intersects(self.black_queen_bitboard, square_mask):
            return Queen(Color.BLACK)
        elif intersects(self.black_king_bitboard, square_mask):
            return King(Color.BLACK)

        return None

    def set_piece(
        self,
        piece: Piece | None,
        coordinate: Coordinate | None = None,
        square_mask: int | None = None,
    ) -> None:
        if coordinate is None and square_mask is None:
            raise ValueError("Must provide either coordinate or square_mask.")

        if coordinate is not None and square_mask is not None:
            raise ValueError(
                "Must provide exactly one of either coordinate or square_mask."
            )

        if coordinate is not None:
            square_mask = calculate_mask(coordinate.row_index, coordinate.column_index)

        assert square_mask is not None

        self._clear_square(square_mask)

        if piece is None:
            return

        match piece:
            case Pawn():
                if piece.color == Color.WHITE:
                    self.white_pawn_bitboard |= square_mask
                else:
                    self.black_pawn_bitboard |= square_mask
            case Knight():
                if piece.color == Color.WHITE:
                    self.white_knight_bitboard |= square_mask
                else:
                    self.black_knight_bitboard |= square_mask
            case Bishop():
                if piece.color == Color.WHITE:
                    self.white_bishop_bitboard |= square_mask
                else:
                    self.black_bishop_bitboard |= square_mask
            case Rook():
                if piece.color == Color.WHITE:
                    self.white_rook_bitboard |= square_mask
                else:
                    self.black_rook_bitboard |= square_mask
            case Queen():
                if piece.color == Color.WHITE:
                    self.white_queen_bitboard |= square_mask
                else:
                    self.black_queen_bitboard |= square_mask
            case King():
                if piece.color == Color.WHITE:
                    self.white_king_bitboard |= square_mask
                else:
                    self.black_king_bitboard |= square_mask
            case _:
                raise ValueError(f"Invalid piece type: {piece}")

    def is_occupied(self, square_mask: int, color: Color | None = None) -> bool:
        """Return whether the square is occupied by the color. Checks both colors
        if not specified."""
        is_occupied_by_white = (
            intersects(self.white_pawn_bitboard, square_mask)
            or intersects(self.white_knight_bitboard, square_mask)
            or intersects(self.white_bishop_bitboard, square_mask)
            or intersects(self.white_rook_bitboard, square_mask)
            or intersects(self.white_queen_bitboard, square_mask)
            or intersects(self.white_king_bitboard, square_mask)
        )
        is_occupied_by_black = (
            intersects(self.black_pawn_bitboard, square_mask)
            or intersects(self.black_knight_bitboard, square_mask)
            or intersects(self.black_bishop_bitboard, square_mask)
            or intersects(self.black_rook_bitboard, square_mask)
            or intersects(self.black_queen_bitboard, square_mask)
            or intersects(self.black_king_bitboard, square_mask)
        )

        if color == Color.WHITE:
            return is_occupied_by_white

        if color == Color.BLACK:
            return is_occupied_by_black

        return is_occupied_by_white or is_occupied_by_black

    def make_move(self, move: Move) -> None:
        self.set_piece(None, square_mask=move.from_square_mask)
        self.set_piece(move.from_piece, square_mask=move.to_square_mask)

    def undo_move(self, move: Move) -> None:
        self.set_piece(move.from_piece, square_mask=move.from_square_mask)
        self.set_piece(move.to_piece, square_mask=move.to_square_mask)

    def _clear_square(self, square_mask: int) -> None:
        self.white_pawn_bitboard &= ~square_mask
        self.white_knight_bitboard &= ~square_mask
        self.white_bishop_bitboard &= ~square_mask
        self.white_rook_bitboard &= ~square_mask
        self.white_queen_bitboard &= ~square_mask
        self.white_king_bitboard &= ~square_mask

        self.black_pawn_bitboard &= ~square_mask
        self.black_knight_bitboard &= ~square_mask
        self.black_bishop_bitboard &= ~square_mask
        self.black_rook_bitboard &= ~square_mask
        self.black_queen_bitboard &= ~square_mask
        self.black_king_bitboard &= ~square_mask
