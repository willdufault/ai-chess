from models.move import Move
from utils.board_utils import is_coordinate_in_bounds


class MoveValidator:
    @staticmethod
    def is_valid(move: Move) -> bool:
        are_coordinates_in_bounds = is_coordinate_in_bounds(
            move.from_coordinate
        ) and is_coordinate_in_bounds(move.to_coordinate)
        if not are_coordinates_in_bounds:
            return False

        if move.from_piece is None or move.from_piece.color != move.color:
            return False

        if move.to_piece is not None and move.to_piece.color == move.color:
            return False

        return True
