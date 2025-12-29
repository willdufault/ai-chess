from enums.color import Color
from enums.game_mode import GameMode
from models.board import Board
from models.move import Move


class Game:
    # TODO: does this need to exist? all private vars = smell?
    def __init__(self, board: Board) -> None:
        self._board = board
        self._current_color = Color.WHITE
        self._mode = GameMode.VS_PLAYER
        self._ai_depth = 0
        self._player_color = Color.WHITE

    def make_move(self, move: Move) -> None:
        self._board.make_move(move)
