from constants.board_constants import BOARD_SIZE
from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.board_utils import calculate_mask, signed_shift

UP_MASK = 0b00000000_11111111_11111111_11111111_11111111_11111111_11111111_11111111
DOWN_MASK = 0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_00000000
LEFT_MASK = 0b11111110_11111110_11111110_11111110_11111110_11111110_11111110_11111110
RIGHT_MASK = 0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_01111111

UP_LEFT_MASK = UP_MASK & LEFT_MASK
UP_RIGHT_MASK = UP_MASK & RIGHT_MASK
DOWN_LEFT_MASK = DOWN_MASK & LEFT_MASK
DOWN_RIGHT_MASK = DOWN_MASK & RIGHT_MASK

UP_SHIFT = 8
DOWN_SHIFT = -8
LEFT_SHIFT = -1
RIGHT_SHIFT = 1

UP_LEFT_SHIFT = 7
UP_RIGHT_SHIFT = 9
DOWN_LEFT_SHIFT = -9
DOWN_RIGHT_SHIFT = -7

KNIGHT_UP2_LEFT_MASK = signed_shift(UP_LEFT_MASK, DOWN_SHIFT)
KNIGHT_UP2_RIGHT_MASK = signed_shift(UP_RIGHT_MASK, DOWN_SHIFT)
KNIGHT_DOWN2_LEFT_MASK = DOWN_LEFT_MASK & signed_shift(DOWN_LEFT_MASK, UP_SHIFT)
KNIGHT_DOWN2_RIGHT_MASK = DOWN_RIGHT_MASK & signed_shift(DOWN_RIGHT_MASK, UP_SHIFT)
KNIGHT_LEFT2_UP_MASK = UP_LEFT_MASK & signed_shift(UP_LEFT_MASK, RIGHT_SHIFT)
KNIGHT_LEFT2_DOWN_MASK = DOWN_LEFT_MASK & signed_shift(DOWN_LEFT_MASK, RIGHT_SHIFT)
KNIGHT_RIGHT2_UP_MASK = UP_RIGHT_MASK & signed_shift(UP_RIGHT_MASK, LEFT_SHIFT)
KNIGHT_RIGHT2_DOWN_MASK = DOWN_RIGHT_MASK & signed_shift(DOWN_RIGHT_MASK, LEFT_SHIFT)

KNIGHT_UP2_LEFT_SHIFT = 15
KNIGHT_UP2_RIGHT_SHIFT = 17
KNIGHT_DOWN2_LEFT_SHIFT = -17
KNIGHT_DOWN2_RIGHT_SHIFT = -15
KNIGHT_LEFT2_UP_SHIFT = 6
KNIGHT_LEFT2_DOWN_SHIFT = -10
KNIGHT_RIGHT2_UP_SHIFT = 10
KNIGHT_RIGHT2_DOWN_SHIFT = -6

PAWN_UP_TRANSFORMS = [(UP_LEFT_MASK, UP_LEFT_SHIFT), (UP_RIGHT_MASK, UP_RIGHT_SHIFT)]
PAWN_DOWN_TRANSFORMS = [
    (DOWN_LEFT_MASK, DOWN_LEFT_SHIFT),
    (DOWN_RIGHT_MASK, DOWN_RIGHT_SHIFT),
]
HORIZONTAL_TRANSFORMS = [
    (UP_MASK, UP_SHIFT),
    (DOWN_MASK, DOWN_SHIFT),
    (LEFT_MASK, LEFT_SHIFT),
    (RIGHT_MASK, RIGHT_SHIFT),
]
DIAGONAL_TRANSFORMS = [
    (UP_LEFT_MASK, UP_LEFT_SHIFT),
    (UP_RIGHT_MASK, UP_RIGHT_SHIFT),
    (DOWN_LEFT_MASK, DOWN_LEFT_SHIFT),
    (DOWN_RIGHT_MASK, DOWN_RIGHT_SHIFT),
]
KNIGHT_TRANSFORMS = [
    (KNIGHT_UP2_LEFT_MASK, KNIGHT_UP2_LEFT_SHIFT),
    (KNIGHT_UP2_RIGHT_MASK, KNIGHT_UP2_RIGHT_SHIFT),
    (KNIGHT_DOWN2_LEFT_MASK, KNIGHT_DOWN2_LEFT_SHIFT),
    (KNIGHT_DOWN2_RIGHT_MASK, KNIGHT_DOWN2_RIGHT_SHIFT),
    (KNIGHT_LEFT2_UP_MASK, KNIGHT_LEFT2_UP_SHIFT),
    (KNIGHT_LEFT2_DOWN_MASK, KNIGHT_LEFT2_DOWN_SHIFT),
    (KNIGHT_RIGHT2_UP_MASK, KNIGHT_RIGHT2_UP_SHIFT),
    (KNIGHT_RIGHT2_DOWN_MASK, KNIGHT_RIGHT2_DOWN_SHIFT),
]


class Board:
    def __init__(self) -> None:
        self.size = BOARD_SIZE

        self._white_pawn_squares = 0
        self._white_rook_squares = 0
        self._white_knight_squares = 0
        self._white_bishop_squares = 0
        self._white_queen_squares = 0
        self._white_king_square = 0

        self._black_pawn_squares = 0
        self._black_rook_squares = 0
        self._black_knight_squares = 0
        self._black_bishop_squares = 0
        self._black_queen_squares = 0
        self._black_king_square = 0

    def set_up_pieces(self) -> None:
        self._white_pawn_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
        )
        self._white_rook_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
        )
        self._white_knight_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
        )
        self._white_bishop_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
        )
        self._white_queen_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
        )
        self._white_king_square = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
        )

        self._black_pawn_squares = (
            0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_rook_squares = (
            0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_knight_squares = (
            0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_bishop_squares = (
            0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_queen_squares = (
            0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_king_square = (
            0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )

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
                square = calculate_mask(row_index, column_index)

                if (self._white_pawn_squares & square) != 0:
                    print("♙", end=" ")
                elif (self._white_knight_squares & square) != 0:
                    print("♘", end=" ")
                elif (self._white_bishop_squares & square) != 0:
                    print("♗", end=" ")
                elif (self._white_rook_squares & square) != 0:
                    print("♖", end=" ")
                elif (self._white_queen_squares & square) != 0:
                    print("♕", end=" ")
                elif self._white_king_square & square != 0:
                    print("♔", end=" ")

                elif (self._black_pawn_squares & square) != 0:
                    print("♟", end=" ")
                elif (self._black_knight_squares & square) != 0:
                    print("♞", end=" ")
                elif (self._black_bishop_squares & square) != 0:
                    print("♝", end=" ")
                elif (self._black_rook_squares & square) != 0:
                    print("♜", end=" ")
                elif (self._black_queen_squares & square) != 0:
                    print("♛", end=" ")
                elif self._black_king_square & square != 0:
                    print("♚", end=" ")
                else:
                    print(".", end=" ")
            print()

    # TODO: reuse get/set piece here?
    def move(self, move: Move) -> None:
        from_square = calculate_mask(
            move.from_coordinate.row_index, move.from_coordinate.column_index
        )
        to_square = calculate_mask(
            move.to_coordinate.row_index, move.to_coordinate.column_index
        )

        if self._white_pawn_squares & from_square != 0:
            self._white_pawn_squares ^= from_square
            self._white_pawn_squares |= to_square
        elif self._white_knight_squares & from_square != 0:
            self._white_knight_squares ^= from_square
            self._white_knight_squares |= to_square
        elif self._white_bishop_squares & from_square != 0:
            self._white_bishop_squares ^= from_square
            self._white_bishop_squares |= to_square
        elif self._white_rook_squares & from_square != 0:
            self._white_rook_squares ^= from_square
            self._white_rook_squares |= to_square
        elif self._white_queen_squares & from_square != 0:
            self._white_queen_squares ^= from_square
            self._white_queen_squares |= to_square
        elif self._white_king_square == from_square:
            self._white_king_square ^= from_square
            self._white_king_square |= to_square

        elif self._black_pawn_squares & from_square != 0:
            self._black_pawn_squares ^= from_square
            self._black_pawn_squares |= to_square
        elif self._black_knight_squares & from_square != 0:
            self._black_knight_squares ^= from_square
            self._black_knight_squares |= to_square
        elif self._black_bishop_squares & from_square != 0:
            self._black_bishop_squares ^= from_square
            self._black_bishop_squares |= to_square
        elif self._black_rook_squares & from_square != 0:
            self._black_rook_squares ^= from_square
            self._black_rook_squares |= to_square
        elif self._black_queen_squares & from_square != 0:
            self._black_queen_squares ^= from_square
            self._black_queen_squares |= to_square
        elif self._black_king_square == from_square:
            self._black_king_square ^= from_square
            self._black_king_square |= to_square

    def get_piece_from_coordinate(self, coordinate: Coordinate) -> Piece | None:
        square = calculate_mask(coordinate.row_index, coordinate.column_index)
        return self.get_piece_from_square(square)

    def get_piece_from_square(self, square: int) -> Piece | None:
        if self._white_pawn_squares & square != 0:
            return Pawn(Color.WHITE)
        elif self._white_knight_squares & square != 0:
            return Knight(Color.WHITE)
        elif self._white_bishop_squares & square != 0:
            return Bishop(Color.WHITE)
        elif self._white_rook_squares & square != 0:
            return Rook(Color.WHITE)
        elif self._white_queen_squares & square != 0:
            return Queen(Color.WHITE)
        elif self._white_king_square & square != 0:
            return King(Color.WHITE)

        elif self._black_pawn_squares & square != 0:
            return Pawn(Color.BLACK)
        elif self._black_knight_squares & square != 0:
            return Knight(Color.BLACK)
        elif self._black_bishop_squares & square != 0:
            return Bishop(Color.BLACK)
        elif self._black_rook_squares & square != 0:
            return Rook(Color.BLACK)
        elif self._black_queen_squares & square != 0:
            return Queen(Color.BLACK)
        elif self._black_king_square & square != 0:
            return King(Color.BLACK)

        return None

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        mask = calculate_mask(coordinate.row_index, coordinate.column_index)

        self._white_pawn_squares &= ~mask
        self._white_knight_squares &= ~mask
        self._white_bishop_squares &= ~mask
        self._white_rook_squares &= ~mask
        self._white_queen_squares &= ~mask
        self._white_king_square &= ~mask

        self._black_pawn_squares &= ~mask
        self._black_knight_squares &= ~mask
        self._black_bishop_squares &= ~mask
        self._black_rook_squares &= ~mask
        self._black_queen_squares &= ~mask
        self._black_king_square &= ~mask

        if piece is None:
            return

        match piece:
            case Pawn():
                if piece.color == Color.WHITE:
                    self._white_pawn_squares |= mask
                else:
                    self._black_pawn_squares |= mask
            case Knight():
                if piece.color == Color.WHITE:
                    self._white_knight_squares |= mask
                else:
                    self._black_knight_squares |= mask
            case Bishop():
                if piece.color == Color.WHITE:
                    self._white_bishop_squares |= mask
                else:
                    self._black_bishop_squares |= mask
            case Rook():
                if piece.color == Color.WHITE:
                    self._white_rook_squares |= mask
                else:
                    self._black_rook_squares |= mask
            case Queen():
                if piece.color == Color.WHITE:
                    self._white_queen_squares |= mask
                else:
                    self._black_queen_squares |= mask
            case King():
                if piece.color == Color.WHITE:
                    self._white_king_square |= mask
                else:
                    self._black_king_square |= mask
            case _:
                raise ValueError(f"Invalid piece type {piece}.")

    def is_occupied(self, square: int) -> bool:
        return (
            self._white_pawn_squares & square != 0
            or self._white_knight_squares & square != 0
            or self._white_bishop_squares & square != 0
            or self._white_rook_squares & square != 0
            or self._white_queen_squares & square != 0
            or self._white_king_square & square != 0
            or self._black_pawn_squares & square != 0
            or self._black_knight_squares & square != 0
            or self._black_bishop_squares & square != 0
            or self._black_rook_squares & square != 0
            or self._black_queen_squares & square != 0
            or self._black_king_square & square != 0
        )

    def calculate_attacker_squares(self, color: Color, target_square: int) -> int:
        """Return a bitboard of all non-king pieces of the color attacking the target
        square."""
        if color == Color.WHITE:
            pawn_transforms = PAWN_DOWN_TRANSFORMS
            pawn_squares = self._white_pawn_squares
            knight_squares = self._white_knight_squares
            bishop_squares = self._white_bishop_squares
            rook_squares = self._white_rook_squares
            queen_squares = self._white_queen_squares
        else:
            pawn_transforms = PAWN_UP_TRANSFORMS
            pawn_squares = self._black_pawn_squares
            knight_squares = self._black_knight_squares
            bishop_squares = self._black_bishop_squares
            rook_squares = self._black_rook_squares
            queen_squares = self._black_queen_squares

        attacker_squares = 0

        for mask, shift in pawn_transforms:
            if target_square & mask != 0:
                pawn_square = signed_shift(target_square, shift)
                if pawn_squares & pawn_square:
                    attacker_squares |= pawn_square

        for mask, shift in KNIGHT_TRANSFORMS:
            if target_square & mask != 0:
                knight_square = signed_shift(target_square, shift)
                if knight_squares & knight_square:
                    attacker_squares |= knight_square

        for mask, shift in DIAGONAL_TRANSFORMS:
            diagonal_square = target_square
            while diagonal_square & mask != 0:
                diagonal_square = signed_shift(diagonal_square, shift)
                if (
                    bishop_squares & diagonal_square != 0
                    or queen_squares & diagonal_square != 0
                ):
                    attacker_squares |= diagonal_square

                if self.is_occupied(diagonal_square):
                    break

        for mask, shift in HORIZONTAL_TRANSFORMS:
            horizontal_square = target_square
            while horizontal_square & mask != 0:
                horizontal_square = signed_shift(horizontal_square, shift)
                if (
                    rook_squares & horizontal_square != 0
                    or queen_squares & horizontal_square != 0
                ):
                    attacker_squares |= horizontal_square

                if self.is_occupied(horizontal_square):
                    break

        return attacker_squares

    def calculate_intermediate_squares(self, from_square: int, to_square: int) -> int:
        """Return a bitboard of all squares between two squares. Return 0 if the
        two squares aren't in a straight line."""
        from_row_index, from_column_index = divmod(from_square.bit_length(), self.size)
        to_row_index, to_column_index = divmod(to_square.bit_length(), self.size)
        row_delta = to_row_index - from_row_index
        column_delta = to_column_index - from_column_index

        # TODO: dupe logic with move_validator
        is_horizontal = 0 in (row_delta, column_delta)
        is_along_diagonal = abs(row_delta) == abs(column_delta)
        if not (is_horizontal or is_along_diagonal):
            return 0

        row_step = row_delta // abs(row_delta) if row_delta != 0 else 0
        column_step = column_delta // abs(column_delta) if column_delta != 0 else 0
        if row_step == 0:
            row_shift = 0
        if row_step == 1:
            row_shift = UP_SHIFT
        elif row_step == -1:
            row_shift = DOWN_SHIFT
        if column_step == 0:
            column_shift = 0
        elif column_step == 1:
            column_shift = RIGHT_SHIFT
        elif column_step == -1:
            column_shift = LEFT_SHIFT

        intermediate_squares = 0
        intermediate_square = signed_shift(
            signed_shift(from_square, row_shift), column_shift
        )
        while intermediate_square != to_square:
            intermediate_squares |= intermediate_square
            intermediate_square = signed_shift(
                signed_shift(intermediate_square, row_shift), column_shift
            )
        return intermediate_squares
