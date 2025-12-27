from constants.board_constants import BOARD_SIZE
from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.board_utils import (
    calculate_mask,
    intersects,
    is_diagonal,
    is_orthogonal,
    signed_shift,
)

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

UP2_LEFT_MASK = signed_shift(UP_LEFT_MASK, DOWN_SHIFT)
UP2_RIGHT_MASK = signed_shift(UP_RIGHT_MASK, DOWN_SHIFT)
DOWN2_LEFT_MASK = DOWN_LEFT_MASK & signed_shift(DOWN_LEFT_MASK, UP_SHIFT)
DOWN2_RIGHT_MASK = DOWN_RIGHT_MASK & signed_shift(DOWN_RIGHT_MASK, UP_SHIFT)
LEFT2_UP_MASK = UP_LEFT_MASK & signed_shift(UP_LEFT_MASK, RIGHT_SHIFT)
LEFT2_DOWN_MASK = DOWN_LEFT_MASK & signed_shift(DOWN_LEFT_MASK, RIGHT_SHIFT)
RIGHT2_UP_MASK = UP_RIGHT_MASK & signed_shift(UP_RIGHT_MASK, LEFT_SHIFT)
RIGHT2_DOWN_MASK = DOWN_RIGHT_MASK & signed_shift(DOWN_RIGHT_MASK, LEFT_SHIFT)

UP2_LEFT_SHIFT = 15
UP2_RIGHT_SHIFT = 17
DOWN2_LEFT_SHIFT = -17
DOWN2_RIGHT_SHIFT = -15
LEFT2_UP_SHIFT = 6
LEFT2_DOWN_SHIFT = -10
RIGHT2_UP_SHIFT = 10
KNIGHT_RIGHT2_DOWN_SHIFT = -6

PAWN_CAPTURE_UP_TRANSFORMS = [
    (UP_LEFT_MASK, UP_LEFT_SHIFT),
    (UP_RIGHT_MASK, UP_RIGHT_SHIFT),
]
PAWN_CAPTURE_DOWN_TRANSFORMS = [
    (DOWN_LEFT_MASK, DOWN_LEFT_SHIFT),
    (DOWN_RIGHT_MASK, DOWN_RIGHT_SHIFT),
]
PAWN_MOVE_UP_TRANSFORMS = [(UP_MASK, UP_SHIFT)]
PAWN_MOVE_DOWN_TRANSFORMS = [(DOWN_MASK, DOWN_SHIFT)]
ORTHOGONAL_TRANSFORMS = [
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
    (UP2_LEFT_MASK, UP2_LEFT_SHIFT),
    (UP2_RIGHT_MASK, UP2_RIGHT_SHIFT),
    (DOWN2_LEFT_MASK, DOWN2_LEFT_SHIFT),
    (DOWN2_RIGHT_MASK, DOWN2_RIGHT_SHIFT),
    (LEFT2_UP_MASK, LEFT2_UP_SHIFT),
    (LEFT2_DOWN_MASK, LEFT2_DOWN_SHIFT),
    (RIGHT2_UP_MASK, RIGHT2_UP_SHIFT),
    (RIGHT2_DOWN_MASK, KNIGHT_RIGHT2_DOWN_SHIFT),
]
KING_TRANSFORMS = [
    (UP_MASK, UP_SHIFT),
    (DOWN_MASK, DOWN_SHIFT),
    (LEFT_MASK, LEFT_SHIFT),
    (RIGHT_MASK, RIGHT_SHIFT),
    (UP_LEFT_MASK, UP_LEFT_SHIFT),
    (UP_RIGHT_MASK, UP_RIGHT_SHIFT),
    (DOWN_LEFT_MASK, DOWN_LEFT_SHIFT),
    (DOWN_RIGHT_MASK, DOWN_RIGHT_SHIFT),
]


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

                if intersects(self._white_pawn_bitboard, square_mask):
                    print("♙", end=" ")
                elif intersects(self._white_knight_bitboard, square_mask):
                    print("♘", end=" ")
                elif intersects(self._white_bishop_bitboard, square_mask):
                    print("♗", end=" ")
                elif intersects(self._white_rook_bitboard, square_mask):
                    print("♖", end=" ")
                elif intersects(self._white_queen_bitboard, square_mask):
                    print("♕", end=" ")
                elif intersects(self._white_king_bitboard, square_mask):
                    print("♔", end=" ")

                elif intersects(self._black_pawn_bitboard, square_mask):
                    print("♟", end=" ")
                elif intersects(self._black_knight_bitboard, square_mask):
                    print("♞", end=" ")
                elif intersects(self._black_bishop_bitboard, square_mask):
                    print("♝", end=" ")
                elif intersects(self._black_rook_bitboard, square_mask):
                    print("♜", end=" ")
                elif intersects(self._black_queen_bitboard, square_mask):
                    print("♛", end=" ")
                elif intersects(self._black_king_bitboard, square_mask):
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
        self.set_piece(None, square_mask=move.from_square_mask)
        self.set_piece(move.from_piece, square_mask=move.to_square_mask)

    def undo_move(self, move: Move) -> None:
        self.set_piece(move.from_piece, square_mask=move.from_square_mask)
        self.set_piece(move.to_piece, square_mask=move.to_square_mask)

    def calculate_attacker_squares_mask(
        self, target_square_mask: int, color: Color
    ) -> int:
        """Return a mask of all pieces of the color attacking the target square."""
        if color == Color.WHITE:
            pawn_transforms = PAWN_CAPTURE_DOWN_TRANSFORMS
            pawn_bitboard = self._white_pawn_bitboard
            knight_bitboard = self._white_knight_bitboard
            bishop_bitboard = self._white_bishop_bitboard
            rook_bitboard = self._white_rook_bitboard
            queen_bitboard = self._white_queen_bitboard
            king_bitboard = self._white_king_bitboard
        else:
            pawn_transforms = PAWN_CAPTURE_UP_TRANSFORMS
            pawn_bitboard = self._black_pawn_bitboard
            knight_bitboard = self._black_knight_bitboard
            bishop_bitboard = self._black_bishop_bitboard
            rook_bitboard = self._black_rook_bitboard
            queen_bitboard = self._black_queen_bitboard
            king_bitboard = self._black_king_bitboard

        attacker_squares_mask = 0

        if self.is_occupied(target_square_mask, color.opposite):
            attacker_squares_mask |= self._calculate_pattern_attacker_squares_mask(
                target_square_mask, pawn_bitboard, pawn_transforms
            )

        attacker_squares_mask |= self._calculate_pattern_attacker_squares_mask(
            target_square_mask, knight_bitboard, KNIGHT_TRANSFORMS
        )
        attacker_squares_mask |= self._calculate_straight_attacker_squares_mask(
            target_square_mask, [bishop_bitboard, queen_bitboard], DIAGONAL_TRANSFORMS
        )
        attacker_squares_mask |= self._calculate_straight_attacker_squares_mask(
            target_square_mask, [rook_bitboard, queen_bitboard], ORTHOGONAL_TRANSFORMS
        )
        attacker_squares_mask |= self._calculate_pattern_attacker_squares_mask(
            target_square_mask, king_bitboard, KING_TRANSFORMS
        )
        return attacker_squares_mask

    def calculate_blocker_squares(self, target_square_mask: int, color: Color) -> int:
        """Return a bitboard of all non-king pieces of the color that can move to
        the empty target square."""
        if color == Color.WHITE:
            pawn_transforms = PAWN_MOVE_DOWN_TRANSFORMS
            pawn_bitboard = self._white_pawn_bitboard
            knight_bitboard = self._white_knight_bitboard
            bishop_bitboard = self._white_bishop_bitboard
            rook_bitboard = self._white_rook_bitboard
            queen_bitboard = self._white_queen_bitboard
        else:
            pawn_transforms = PAWN_MOVE_UP_TRANSFORMS
            pawn_bitboard = self._black_pawn_bitboard
            knight_bitboard = self._black_knight_bitboard
            bishop_bitboard = self._black_bishop_bitboard
            rook_bitboard = self._black_rook_bitboard
            queen_bitboard = self._black_queen_bitboard

        attacker_squares_mask = 0
        attacker_squares_mask |= self._calculate_pattern_attacker_squares_mask(
            target_square_mask, pawn_bitboard, pawn_transforms
        )
        attacker_squares_mask |= self._calculate_pattern_attacker_squares_mask(
            target_square_mask, knight_bitboard, KNIGHT_TRANSFORMS
        )
        attacker_squares_mask |= self._calculate_straight_attacker_squares_mask(
            target_square_mask, [bishop_bitboard, queen_bitboard], DIAGONAL_TRANSFORMS
        )
        attacker_squares_mask |= self._calculate_straight_attacker_squares_mask(
            target_square_mask, [rook_bitboard, queen_bitboard], ORTHOGONAL_TRANSFORMS
        )
        return attacker_squares_mask

    def calculate_escape_squares_mask(self, square_mask: int, color: Color) -> int:
        """Return a mask of all squares surrounding the given square that are not
        occupied by the color."""
        escape_squares_mask = 0
        for transform_mask, transform_shift in KING_TRANSFORMS:
            if intersects(square_mask, transform_mask):
                escape_square_mask = signed_shift(square_mask, transform_shift)
                if not self.is_occupied(escape_square_mask, color):
                    escape_squares_mask |= escape_square_mask
        return escape_squares_mask

    def calculate_intermediate_squares_mask(
        self, from_square_mask: int, to_square_mask: int
    ) -> int:
        """Return a mask of all squares between two squares in a orthogonal or diagonal
        line."""
        from_coordinate = Coordinate.from_mask(from_square_mask)
        to_coordinate = Coordinate.from_mask(to_square_mask)
        row_delta = to_coordinate.row_index - from_coordinate.row_index
        column_delta = to_coordinate.column_index - from_coordinate.column_index

        if not (
            is_orthogonal(row_delta, column_delta)
            or is_diagonal(row_delta, column_delta)
        ):
            return 0

        if row_delta == 0:
            row_shift = 0
        elif row_delta > 0:
            row_shift = UP_SHIFT
        elif row_delta < 0:
            row_shift = DOWN_SHIFT

        if column_delta == 0:
            column_shift = 0
        elif column_delta > 0:
            column_shift = RIGHT_SHIFT
        elif column_delta < 0:
            column_shift = LEFT_SHIFT

        intermediate_squares_mask = 0
        intermediate_square_mask = signed_shift(
            signed_shift(from_square_mask, row_shift), column_shift
        )
        while intermediate_square_mask != to_square_mask:
            intermediate_squares_mask |= intermediate_square_mask
            intermediate_square_mask = signed_shift(
                signed_shift(intermediate_square_mask, row_shift), column_shift
            )
        return intermediate_squares_mask

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

    def _calculate_pattern_attacker_squares_mask(
        self,
        target_square_mask: int,
        piece_bitboard: int,
        piece_transforms: list[tuple[int, int]],
    ) -> int:
        piece_attacker_squares_mask = 0
        for transform_mask, transform_shift in piece_transforms:
            if intersects(target_square_mask, transform_mask):
                piece_square_mask = signed_shift(target_square_mask, transform_shift)
                if intersects(piece_bitboard, piece_square_mask):
                    piece_attacker_squares_mask |= piece_square_mask
        return piece_attacker_squares_mask

    def _calculate_straight_attacker_squares_mask(
        self,
        target_square_mask: int,
        piece_bitboards: list[int],
        piece_transforms: list[tuple[int, int]],
    ) -> int:
        piece_attacker_squares_mask = 0
        for transform_mask, transform_shift in piece_transforms:
            piece_square_mask = target_square_mask
            while intersects(piece_square_mask, transform_mask):
                piece_square_mask = signed_shift(piece_square_mask, transform_shift)
                if any(
                    [
                        intersects(piece_bitboard, piece_square_mask)
                        for piece_bitboard in piece_bitboards
                    ]
                ):
                    piece_attacker_squares_mask |= piece_square_mask

                if self.is_occupied(piece_square_mask):
                    break
        return piece_attacker_squares_mask
