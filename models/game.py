from enums.color import Color
from enums.game_mode import GameMode
from models.board import Board


class Game:
    # TODO: builder?
    def __init__(self, board: Board) -> None:
        self._board = board
        self._game_mode = GameMode.PLAYER_VS_PLAYER
        self._ai_depth = 0
        self._player_color = Color.WHITE
        self._current_color = Color.WHITE
        # TODO: track first move against ai

    def _play_player_vs_player(self) -> None:
        # 1.1 print board
        # 1.2 tell if in check
        # 2. prompt move
        # 3.1 valid move?
        # 3.2 legal move?
        # 3.3 in check?
        # 3.4 in mate? print board + exit
        # 4. switch team, repeat
        pass

    def _play_player_vs_ai(self) -> None:
        # 1.1 print board
        # 1.2 tell if in check
        # 2. prompt move
        # 3.1 valid move?
        # 3.2 legal move?
        # 3.3 in check?
        # 3.4 in mate? print board + exit
        # 4. switch team, repeat
        pass
