from collections import defaultdict

from enums.color import Color
from models.board import Board
from models.engine import Engine
from models.move import Move
from models.piece import Queen
from models.rules import Rules

_MAX_SCORE = 1_000_000
_MIN_SCORE = -1_000_000


class Bot:
    def __init__(self, depth: int) -> None:
        self._depth = depth
        self._cache = {}

    def calculate_best_move(self, color: Color, board: Board) -> Move:
        moves = list(Rules.generate_legal_moves(color, board))
        scores = self._calculate_move_scores(moves, board)
        best_score = max(scores) if color == Color.WHITE else min(scores)
        best_index = scores.index(best_score)
        best_move = moves[best_index]
        return best_move

    def _calculate_move_scores(self, moves: list[Move], board: Board) -> list[int]:
        scores = []
        for move in moves:
            board.make_move(move)
            score = self._minimax(
                move.color.opposite, self._depth - 1, _MIN_SCORE, _MAX_SCORE, board
            )
            board.undo_move(move)
            scores.append(score)
        return scores

    def _minimax(
        self, color: Color, depth: int, alpha: float, beta: float, board: Board
    ) -> float:
        if depth == 0:
            return Engine.evaluate(board)

        if Rules.is_in_checkmate(color, board):
            return _MIN_SCORE if color == Color.WHITE else _MAX_SCORE
        elif Rules.is_in_stalemate(color, board):
            return 0

        board_hash = hash(board)
        if board_hash in self._cache:
            cached_depth, cached_score = self._cache[board_hash]
            if cached_depth >= depth:
                return cached_score
        else:
            self._cache[board_hash] = (
                depth,
                _MIN_SCORE if color == Color.WHITE else _MAX_SCORE,
            )

        moves = Rules.generate_legal_moves(color, board)
        best_score = _MIN_SCORE if color == Color.WHITE else _MAX_SCORE
        for move in moves:
            board.make_move(move)
            if Rules.can_promote(move):
                board._set_piece(Queen(move.color), move.to_square_mask)
            current_score = self._minimax(color.opposite, depth - 1, alpha, beta, board)
            board.undo_move(move)

            if color == Color.WHITE:
                best_score = max(best_score, current_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, current_score)
                beta = min(beta, best_score)

            if alpha >= beta:
                break

        self._cache[board_hash] = depth, best_score
        return best_score

    # Sorting moves didn't improve performance due to lazy loading tradeoff.
    def _sort_moves(self, moves: list[Move]) -> list[Move]:
        """Return the moves in LVA-MVV order."""
        return sorted(moves, key=self._compare_move)

    def _compare_move(self, move: Move) -> tuple[int, int]:
        from_piece_value = getattr(move.from_piece, "VALUE", 0)
        to_piece_value = getattr(move.to_piece, "VALUE", 0)
        return from_piece_value, -to_piece_value
