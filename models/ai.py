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
        # TODO REMOVE
        self.prune_count = 0
        self.total_count = 0

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
        """TODO
        get legal moves for color
        try them all with depth n-1
        if depth = 0, eval
        a-b pruning
        cache in engine at depth >= cur_depth
        !!! efficient board hashing !!! (test w/ diff strats?)
        """
        if depth == 0:
            return Engine.evaluate(self._board)

        # TODO TEMP
        self.total_count += 1

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
                    # TODO TEMP
                    self.prune_count += 1
                    break
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
                    # TODO TEMP
                    self.prune_count += 1
                    break
            return best_score
