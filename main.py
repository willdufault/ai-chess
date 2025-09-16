from enums.color import Color
from models.board import Board
from views.board_view import BoardView


def main() -> None:
    print("hello world")
    board = Board()
    board.set_up_pieces()
    breakpoint()


if __name__ == "__main__":
    main()
