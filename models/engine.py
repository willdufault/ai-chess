from .board import Board
from .move import Move


class Engine:
    def __init__(self) -> None:
        """
        material
        board control (# of squares)
        threats (attack enemy pieces, bonus if higher val)
        piece position (matrixes for score for each piece)
        king safety
        mobility (# of legal moves)

        """
        pass

    def evaluate(board: Board) -> int:
        """Evaluate the board and return a number 0-100 representing which color
        is winning (low = black, high = white)."""
        return 50

    def order_moves(moves: list[Move]) -> list[Move]:
        pass
