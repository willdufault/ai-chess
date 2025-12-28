from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from utils.bit_utils import intersects, signed_shift
from utils.board_utils import is_diagonal, is_orthogonal

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


class MoveGenerator:
    @classmethod
    def calculate_attacker_squares_mask(
        cls, target_square_mask: int, color: Color, board: Board
    ) -> int:
        """Return a mask of all pieces of the color attacking the target square."""
        if color == Color.WHITE:
            pawn_transforms = PAWN_CAPTURE_DOWN_TRANSFORMS
            pawn_bitboard = board._white_pawn_bitboard
            knight_bitboard = board._white_knight_bitboard
            bishop_bitboard = board._white_bishop_bitboard
            rook_bitboard = board._white_rook_bitboard
            queen_bitboard = board._white_queen_bitboard
            king_bitboard = board._white_king_bitboard
        else:
            pawn_transforms = PAWN_CAPTURE_UP_TRANSFORMS
            pawn_bitboard = board._black_pawn_bitboard
            knight_bitboard = board._black_knight_bitboard
            bishop_bitboard = board._black_bishop_bitboard
            rook_bitboard = board._black_rook_bitboard
            queen_bitboard = board._black_queen_bitboard
            king_bitboard = board._black_king_bitboard

        attacker_squares_mask = 0

        if board.is_occupied(target_square_mask, color.opposite):
            attacker_squares_mask |= cls._calculate_pattern_attacker_squares_mask(
                target_square_mask, pawn_bitboard, pawn_transforms
            )

        attacker_squares_mask |= cls._calculate_pattern_attacker_squares_mask(
            target_square_mask, knight_bitboard, KNIGHT_TRANSFORMS
        )
        attacker_squares_mask |= cls._calculate_straight_attacker_squares_mask(
            target_square_mask,
            [bishop_bitboard, queen_bitboard],
            DIAGONAL_TRANSFORMS,
            board,
        )
        attacker_squares_mask |= cls._calculate_straight_attacker_squares_mask(
            target_square_mask,
            [rook_bitboard, queen_bitboard],
            ORTHOGONAL_TRANSFORMS,
            board,
        )
        attacker_squares_mask |= cls._calculate_pattern_attacker_squares_mask(
            target_square_mask, king_bitboard, KING_TRANSFORMS
        )
        return attacker_squares_mask

    @classmethod
    def calculate_blocker_squares(
        cls, target_square_mask: int, color: Color, board: Board
    ) -> int:
        """Return a bitboard of all non-king pieces of the color that can move to
        the empty target square."""
        if color == Color.WHITE:
            pawn_transforms = PAWN_MOVE_DOWN_TRANSFORMS
            pawn_bitboard = board._white_pawn_bitboard
            knight_bitboard = board._white_knight_bitboard
            bishop_bitboard = board._white_bishop_bitboard
            rook_bitboard = board._white_rook_bitboard
            queen_bitboard = board._white_queen_bitboard
        else:
            pawn_transforms = PAWN_MOVE_UP_TRANSFORMS
            pawn_bitboard = board._black_pawn_bitboard
            knight_bitboard = board._black_knight_bitboard
            bishop_bitboard = board._black_bishop_bitboard
            rook_bitboard = board._black_rook_bitboard
            queen_bitboard = board._black_queen_bitboard

        attacker_squares_mask = 0
        attacker_squares_mask |= cls._calculate_pattern_attacker_squares_mask(
            target_square_mask, pawn_bitboard, pawn_transforms
        )
        attacker_squares_mask |= cls._calculate_pattern_attacker_squares_mask(
            target_square_mask, knight_bitboard, KNIGHT_TRANSFORMS
        )
        attacker_squares_mask |= cls._calculate_straight_attacker_squares_mask(
            target_square_mask,
            [bishop_bitboard, queen_bitboard],
            DIAGONAL_TRANSFORMS,
            board,
        )
        attacker_squares_mask |= cls._calculate_straight_attacker_squares_mask(
            target_square_mask,
            [rook_bitboard, queen_bitboard],
            ORTHOGONAL_TRANSFORMS,
            board,
        )
        return attacker_squares_mask

    @staticmethod
    def calculate_escape_squares_mask(
        square_mask: int, color: Color, board: Board
    ) -> int:
        """Return a mask of all squares surrounding the given square that are not
        occupied by the color."""
        escape_squares_mask = 0
        for transform_mask, transform_shift in KING_TRANSFORMS:
            if intersects(square_mask, transform_mask):
                escape_square_mask = signed_shift(square_mask, transform_shift)
                if not board.is_occupied(escape_square_mask, color):
                    escape_squares_mask |= escape_square_mask
        return escape_squares_mask

    @classmethod
    def calculate_intermediate_squares_mask(
        cls, from_square_mask: int, to_square_mask: int
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

    @staticmethod
    def _calculate_pattern_attacker_squares_mask(
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

    @staticmethod
    def _calculate_straight_attacker_squares_mask(
        target_square_mask: int,
        piece_bitboards: list[int],
        piece_transforms: list[tuple[int, int]],
        board: Board,
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

                if board.is_occupied(piece_square_mask):
                    break
        return piece_attacker_squares_mask
