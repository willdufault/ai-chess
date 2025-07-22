from board import Board
from enums import Color


class Game:
    """Represents a chess game."""

    def __init__(self) -> None:
        self.board = Board()

    def move(
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
    ) -> None:
        pass


if __name__ == "__main__":
    from piece import Pawn
    g = Game()

    # TODO: PICK UP HERE
    # testing pawn move strategy, need to figure out import error

    g.board.squares[2][1] = Pawn(Color.BLACK)
    print(g.board)
