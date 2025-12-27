from enums.color import Color
from models.board import Board, Coordinate
from models.move import Move
from models.move_validator import MoveValidator
from models.piece import Pawn
from utils.board_utils import print_bitboard


def main() -> None:
    b = Board()
    b.set_up_pieces()
    b.print(Color.BLACK)

if __name__ == "__main__":
    main()
