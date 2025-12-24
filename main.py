from models.board import Board, Coordinate


def main() -> None:
    b = Board()
    b.set_up_pieces()
    b.move(Coordinate(1, 0), Coordinate(2, 0))
    b.print()


if __name__ == "__main__":
    main()
