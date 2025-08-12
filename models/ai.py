from enums import Color

from .board import Board
from .coordinate import Coordinate
from .engine import Engine

MAX_DEPTH = 10


class AI:
    def __init__(self, color: Color, depth: int, board: Board, engine: Engine) -> None:
        self._color = color
        self._board = board
        self._depth = depth
        self._engine = engine

    def move(self) -> tuple[Coordinate, Coordinate]:
        pass

    def _minimax(self, color: Color, depth: int) -> int:
        """
        get legal moves for color
        try them all with depth n-1
        if depth = 0, eval
        a-b pruning
        cache in engine at depth >= cur_depth
        """
        pass

        if depth == 0:
            return self._engine.evaluate(self._board)

        legal_moves = self._board.get_legal_moves(color)
        legal_moves = self._engine.order_moves(legal_moves)
