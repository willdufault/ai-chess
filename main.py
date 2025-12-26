from enums.color import Color
from models.board import Board, Coordinate
from models.move import Move
from models.move_validator import MoveValidator
from models.piece import Pawn


def main() -> None:
    b = Board()
    b.set_up_pieces()
    breakpoint()


if __name__ == "__main__":
    main()
