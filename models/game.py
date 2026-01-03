from enums.color import Color
from enums.game_status import GameStatus
from models.board import Board
from models.move import Move


class Game:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._current_color = Color.WHITE
        self.status = GameStatus.ACTIVE

    def make_move(self, move: Move) -> None:
        self._board.make_move(move)
