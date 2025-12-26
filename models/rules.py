from enums.color import Color
from models.board import Board


class Rules:
    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        king_square = board._white_king_square if color is Color.WHITE else board._black_king_square
        return board.calculate_attacker_squares(color.opposite, king_square) != 0

    @classmethod
    def is_in_checkmate(cls, color: Color, board: Board) -> bool:
        if not cls.is_in_check(color, board):
            return False

        return False