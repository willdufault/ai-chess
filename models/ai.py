from enums.color import Color
from models.board import Board
from models.engine import Engine
from models.move import Move
from models.rules import Rules

_MAX_SCORE = 1_000_000
_MIN_SCORE = -1_000_000


# TODO: TBD WHICH FOLDER
class AI:
    def __init__(
        self,
        color: Color,
        depth: int,
        board: Board,
    ) -> None:
        self._color = color
        self._depth = depth
        self._board = board
        self._cache = {}  # TODO better name

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Color) -> None:
        self._color = color

    @property
    def depth(self) -> int:
        return self._depth

    @depth.setter
    def depth(self, depth: int) -> None:
        self._depth = depth

    def get_best_move(self, color: Color) -> Move:
        """Get the best move for the color."""
        moves = Rules.get_legal_moves(color, self._board)
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
            scores.append(
                self._minimax(self._color.opposite, self._depth, _MIN_SCORE, _MAX_SCORE)
            )
            self._board.undo_move(move)
        return scores

    def _minimax(self, color: Color, depth: int, alpha: int, beta: int) -> int:
        if depth == 0:
            return Engine.evaluate(self._board)

        board_key = self._board.to_key()
        if board_key in self._cache:
            cached_depth, cached_score = self._cache[board_key]
            if cached_depth >= depth:
                return cached_score

        moves = Rules.get_legal_moves(color, self._board)
        if color is Color.WHITE:
            best_score = _MIN_SCORE
            for move in moves:
                self._board.make_move(move)
                current_score = self._minimax(color.opposite, depth - 1, alpha, beta)
                self._board.undo_move(move)
                best_score = max(best_score, current_score)
                alpha = max(alpha, best_score)
                if best_score >= beta:
                    break
            self._cache[board_key] = (depth, best_score)
            return best_score
        else:
            best_score = _MAX_SCORE
            for move in moves:
                self._board.make_move(move)
                current_score = self._minimax(color.opposite, depth - 1, alpha, beta)
                self._board.undo_move(move)
                best_score = min(best_score, current_score)
                beta = min(beta, best_score)
                if best_score <= alpha:
                    break
            self._cache[board_key] = (depth, best_score)
            return best_score
