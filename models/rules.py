from enums.color import Color
from models.board import Board
from utils.board_utils import calculate_mask


class Rules:
    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        king_square = (
            board._white_king_square
            if color is Color.WHITE
            else board._black_king_square
        )
        return board.calculate_attacker_squares(color.opposite, king_square) != 0

    @classmethod
    def is_in_checkmate(cls, color: Color, board: Board) -> bool:
        if not cls.is_in_check(color, board):
            return False

        king_square = (
            board._white_king_square
            if color == Color.WHITE
            else board._black_king_square
        )
        attacker_squares = board.calculate_attacker_squares(color.opposite, king_square)
        is_impossible_to_block = attacker_squares.bit_count() > 1
        if is_impossible_to_block:
            return True

        for attacker_shift in range(board.size**2):
            attacker_square = 1 << attacker_shift
            if attacker_squares & attacker_square != 0:
                intermediate_squares = board.calculate_intermediate_squares(
                    king_square, attacker_square
                )
                candidate_squares = intermediate_squares | attacker_square
                for candidate_shift in range(board.size**2):
                    candidate_square = 1 << candidate_shift
                    if candidate_square & candidate_squares != 0:
                        defender_squares = board.calculate_attacker_squares(
                            color, candidate_square
                        )
                        # 1. sim move
                        # 2. check check
                        # 3. no check? no mate

        # for each attacker:
        # - for each square in [attacker_sq + interm_sq]:
        # - - check block + not in check
        return True
