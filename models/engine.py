from enums import Color

from ..models.board import BOARD_SIZE, Board
from ..models.coordinate import Coordinate
from ..models.move import Move


# TODO: TBD WHICH FOLDER
class Engine:
    def __init__(self, board: Board) -> None:
        """
        material
        board control (# of squares)
        threats (attack enemy pieces, bonus if higher val)
        piece position (matrixes for score for each piece)
        king safety
        mobility (# of legal moves)
        cache evals based on depth
        """
        self._board = board

    def evaluate(self) -> int:
        """Evaluate the board and return a number (TODO) 0-100 representing which color
        is winning (low = black, high = white)."""
        return self._get_material_advantage()

    # TODO
    def order_moves(self, moves: list[Move]) -> list[Move]:
        print("engine.order_moves is not implemented")
        return moves

    # TODO: could make this an attr on board, could also cache for board hash
    def _get_material_advantage(self) -> int:
        """Return the sum of the values of all white pieces minus the sum of
        values of all black pieces."""
        total = 0
        for row_index in range(BOARD_SIZE):
            for column_index in range(BOARD_SIZE):
                curr_coord = Coordinate(row_index, column_index)
                piece = self._board.get_piece(curr_coord)
                if piece is not None:
                    value = piece.value if piece.color is Color.WHITE else -piece.value
                    total += value
        return total
