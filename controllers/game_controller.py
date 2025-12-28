from enums.game_mode import GameMode
from models.game import Game
from views.game_view import GameView


class GameController:
    def __init__(self, game: Game) -> None:
        self._game = game

    def configure(self) -> None:
        self._game.game_mode = GameView.prompt_game_mode()
        if self._game.game_mode == GameMode.PLAYER_VS_AI:
            self._game.ai_depth = GameView.prompt_ai_depth()
            self._game.player_color = GameView.prompt_player_color()

    def play(self) -> None:
        if self._game.game_mode == GameMode.PLAYER_VS_PLAYER:
            self._game.play_player_vs_player()
        else:
            self._game.play_player_vs_ai()
