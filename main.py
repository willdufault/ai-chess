from enums.color import Color
from models.board import Board


def main() -> None:
    b = Board()
    b.set_up_pieces()
    b.print(Color.WHITE)

if __name__ == "__main__":
    main()
