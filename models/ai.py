from enums.color import Color
from models.board import Board
from models.engine import Engine
from models.move import Move
from models.piece import Queen
from models.rules import Rules

_MAX_SCORE = 1_000_000
_MIN_SCORE = -1_000_000


# TODO: optimize as much as possible, THEN add multithreading (thread safe dict)
class Ai:
    def __init__(self, depth: int) -> None:
        self._depth = depth
        self._transposition_table = {}
        self._hits = 0
        self._total = 0

    def calculate_best_move(self, color: Color, board: Board) -> Move:
        moves = list(Rules.generate_legal_moves(color, board))
        scores = self._calculate_move_scores(moves, board)
        best_score = max(scores) if color == Color.WHITE else min(scores)
        best_index = scores.index(best_score)
        best_move = moves[best_index]
        print(f"hits:", self._hits)
        print(f"total:", self._total)
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

        self._total += 1
        board_hash = hash(board)
        if board_hash in self._transposition_table:
            cached_depth, cached_score = self._transposition_table[board_hash]
            if cached_depth >= depth:
                self._hits += 1
                return cached_score

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

        self._transposition_table[board_hash] = depth, best_score
        return best_score
