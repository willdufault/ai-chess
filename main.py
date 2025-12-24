from enums.color import Color
from models.board import Board, Coordinate
from models.move import Move
from models.move_validator import MoveValidator
from models.piece import Pawn


def main() -> None:
    b = Board()
    b.set_up_pieces()

    c1 = Coordinate(1, 0)
    c2 = Coordinate(2, 0)
    p1 = b.get_piece(c1)
    p2 = b.get_piece(c2)
    m = Move(c1, c2, p1, p2, Color.WHITE)
    v = MoveValidator.is_valid(m)
    if v:
        b.move(m)
        b.print(Color.WHITE)
    else:
        print(f'INVALID')


if __name__ == "__main__":
    main()
