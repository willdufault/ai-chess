from enums.color import Color
from models.board import Board
from models.engine import Engine
from models.move import Move
from models.rules import Rules

_MAX_SCORE = 1_000_000
_MIN_SCORE = -1_000_000


class AI:
    def __init__(self, depth: int) -> None:
        self._depth = depth
        self._transposition_table = {}

    def calculate_best_move(self, color: Color, board: Board) -> Move:
        moves = Rules.generate_legal_moves(color, board)
        scores = self._calculate_move_scores(moves, board)
        best_score = max(scores) if color == Color.WHITE else min(scores)
        best_index = scores.index(best_score)
        best_move = moves[best_index]
        return best_move

    def _calculate_move_scores(self, moves: list[Move], board: Board) -> list[int]:
        scores = []
        for move in moves:
            board.make_move(move)
            scores.append(
                self._minimax(
                    move.color.opposite, self._depth - 1, _MIN_SCORE, _MAX_SCORE, board
                )
            )
            board.undo_move(move)
        return scores

    def _minimax(
        self, color: Color, depth: int, alpha: int, beta: int, board: Board
    ) -> int:
        if depth == 0:
            # TODO: cache this?
            return Engine.evaluate(board)

        # TODO: impl
        # board_hash = 0
        # if board_hash in self._transposition_table:
        #     cached_depth, cached_score = self._transposition_table[board_hash]
        #     if cached_depth >= depth:
        #         return cached_score

        # TODO: store legal moves (everything, really) in transposition table
        moves = Rules.generate_legal_moves(color, board)
        best_score = _MIN_SCORE if color == Color.WHITE else _MAX_SCORE
        for move in moves:
            board.make_move(move)
            # TODO: add AI PROMO -> Queen
            current_score = self._minimax(color.opposite, depth - 1, alpha, beta, board)
            board.undo_move(move)

            if color == Color.WHITE:
                best_score = max(best_score, current_score)
                alpha = max(alpha, best_score)
                if best_score >= beta:
                    break
            else:
                best_score = min(best_score, current_score)
                beta = min(beta, best_score)
                if best_score <= alpha:
                    break

        # self._transposition_table[board_hash] = (depth, best_score)
        return best_score
