from models.board import Board
from utils.board_utils import signed_shift

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


class Rules:
    @staticmethod
    def is_white_in_check(board: Board) -> bool:
        # TODO: clean up, make relative to board size
        # TODO: after, check if all info makes sense in this fcn
        # pawn
        if board._white_king_square & UP_LEFT_MASK != 0:
            up_left_square = board._white_king_square << UP_LEFT_SHIFT
            if board._black_pawn_squares & up_left_square:
                return True
        if board._white_king_square & UP_RIGHT_MASK != 0:
            up_right_square = board._white_king_square << UP_RIGHT_SHIFT
            if board._black_pawn_squares & up_right_square:
                return True

        # knight
        for mask, shift in KNIGHT_TRANSFORMS:
            if board._white_king_square & mask != 0:
                knight_square = signed_shift(board._white_king_square, shift)
                if board._black_knight_squares & knight_square:
                    return True

        # bishop & queen
        for mask, shift in DIAGONAL_TRANSFORMS:
            diagonal_square = board._white_king_square
            while diagonal_square & mask != 0:
                diagonal_square = signed_shift(diagonal_square, shift)
                if (
                    diagonal_square & board._black_bishop_squares
                    or diagonal_square & board._black_queen_squares
                ):
                    return True

                if board.is_occupied(diagonal_square):
                    break

        # rook & queen
        for mask, shift in HORIZONTAL_TRANSFORMS:
            horizontal_square = board._white_king_square
            while horizontal_square & mask != 0:
                horizontal_square = signed_shift(horizontal_square, shift)
                if (
                    horizontal_square & board._black_rook_squares
                    or horizontal_square & board._black_queen_squares
                ):
                    return True

                if board.is_occupied(horizontal_square):
                    break

        return False
