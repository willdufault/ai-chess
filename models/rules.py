from enums.color import Color
from models.board import Board
from models.move_generator import MoveGenerator


class Rules:
    @staticmethod
    def is_in_check(board: Board, color: Color) -> bool:
        king_mask = (
            board.white_king_mask if color is Color.WHITE else board.black_king_mask
        )
        king_coordinate = board.get_coordinate_from_mask(king_mask)
        return (
            len(
                MoveGenerator.get_attacker_coordinates(
                    board, color.opposite, king_coordinate
                )
            )
            > 0
        )

    @staticmethod
    def is_in_checkmate(board: Board) -> bool: ...
