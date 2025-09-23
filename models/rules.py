from models.board import Board
from models.move_generator import MoveGenerator


class Rules:
    @staticmethod
    def is_in_check(board: Board) -> bool:
        return len(MoveGenerator.(board)) > 0
        




    @staticmethod
    def is_in_checkmate(board: Board) -> bool: ...
