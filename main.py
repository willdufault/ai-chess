from enums.color import Color
from models.board import Board, Coordinate
from models.move import Move
from models.move_validator import MoveValidator
from models.piece import Pawn
from utils.board_utils import print_bitboard


def main() -> None:
    b = Board()
    _1 = b.calculate_intermediate_squares(1,2)
    _2 = b.calculate_intermediate_squares(1<<51,1<<27)
    breakpoint()

if __name__ == "__main__":
    main()
