from enums.color import Color
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


class Rules:
    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        if color == Color.WHITE:
            king_square = board._white_king_square
            pawn_transforms = PAWN_UP_TRANSFORMS
            opponent_pawn_squares = board._black_pawn_squares
            opponent_knight_squares = board._black_knight_squares
            opponent_bishop_squares = board._black_bishop_squares
            opponent_rook_squares = board._black_rook_squares
            opponent_queen_squares = board._black_queen_squares
        else:
            king_square = board._black_king_square
            pawn_transforms = PAWN_DOWN_TRANSFORMS
            opponent_pawn_squares = board._white_pawn_squares
            opponent_knight_squares = board._white_knight_squares
            opponent_bishop_squares = board._white_bishop_squares
            opponent_rook_squares = board._white_rook_squares
            opponent_queen_squares = board._white_queen_squares

        for mask, shift in pawn_transforms:
            if king_square & mask != 0:
                pawn_square = signed_shift(king_square, shift)
                if opponent_pawn_squares & pawn_square:
                    return True

        for mask, shift in KNIGHT_TRANSFORMS:
            if king_square & mask != 0:
                knight_square = signed_shift(king_square, shift)
                if opponent_knight_squares & knight_square:
                    return True

        is_under_diagonal_attack = cls._is_under_straight_attack(
            board,
            king_square,
            [opponent_bishop_squares, opponent_queen_squares],
            DIAGONAL_TRANSFORMS,
        )
        if is_under_diagonal_attack:
            return True

        is_under_horizontal_attack = cls._is_under_straight_attack(
            board,
            king_square,
            [opponent_rook_squares, opponent_queen_squares],
            HORIZONTAL_TRANSFORMS,
        )
        if is_under_horizontal_attack:
            return True

        return False

    @staticmethod
    def _is_under_straight_attack(
        board: Board,
        king_square: int,
        attacker_squares: list[int],
        transforms: list[tuple[int, int]],
    ) -> bool:
        for mask, shift in transforms:
            current_square = king_square
            while current_square & mask != 0:
                current_square = signed_shift(current_square, shift)
                if any(
                    [
                        current_square & attacker_square != 0
                        for attacker_square in attacker_squares
                    ]
                ):
                    return True

                if board.is_occupied(current_square):
                    break

        return False
