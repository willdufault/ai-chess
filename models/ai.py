from math import inf

from enums import Color

from .board import Board
from .engine import Engine
from .move import Move

MAX_DEPTH = 10


class AI:
    def __init__(self, color: Color, depth: int, board: Board, engine: Engine) -> None:
        self._color = color
        self._board = board
        self._depth = depth
        self._engine = engine

    def get_best_move(self, color: Color) -> Move:
        """Get the best move for the given color."""
        moves = self._board.get_legal_moves()
        # TODO: order moves here? special order in board?
        scores = self._get_move_scores(moves)
        best_score = max(scores) if color is Color.WHITE else min(scores)
        best_score_index = scores.index(best_score)
        best_move = moves[best_score_index]
        return best_move

    def _get_move_scores(self, moves: list[Move]) -> list[int]:
        """Return a list of scores for each move."""
        scores = []
        for move in moves:
            self._board.make_move(move)
            other_color = Color.get_other_color(self._color)
            scores.append(self._minimax(other_color, self._depth))
            self._board.undo_move(move)
        return scores

    def _minimax(self, color: Color, depth: int) -> Move:
        """TODO
        get legal moves for color
        try them all with depth n-1
        if depth = 0, eval
        a-b pruning
        cache in engine at depth >= cur_depth
        """

        if depth == 0:
            return self._engine.evaluate(self._board)

        best_score = -inf if color is Color.WHITE else inf
        other_color = Color.get_other_color(color)
        moves = self._board.get_legal_moves(color)  # TODO: Order moves?
        for move in moves:
            self._board.make_move(move)
            curr_score = self._minimax(other_color, depth - 1)
            self._board.undo_move(move)
            if color is Color.WHITE:
                best_score = max(best_score, curr_score)
            else:
                best_score = min(best_score, curr_score)
        return best_score
