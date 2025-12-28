from constants.ai_constants import MAX_AI_DEPTH
from enums.color import Color
from enums.game_mode import GameMode


class GameView:
    @classmethod
    def prompt_game_mode(cls) -> GameMode:
        message = "Choose a game mode: (1) player vs. player, or (2) player vs. AI."
        choices = [1, 2]
        choice = cls._prompt_choice(message, choices)
        return GameMode.PLAYER_VS_PLAYER if choice == 1 else GameMode.PLAYER_VS_AI

    @classmethod
    def prompt_ai_depth(cls) -> int:
        message = f"Choose an AI depth from 0 to {MAX_AI_DEPTH} (higher = smarter but slower)."
        choices = list(range(MAX_AI_DEPTH + 1))
        return cls._prompt_choice(message, choices)

    @classmethod
    def prompt_player_color(cls) -> Color:
        message = f"Choose a color to play as: (1) white, or (2) black."
        choices = [1, 2]
        choice = cls._prompt_choice(message, choices)
        return Color.WHITE if choice == 1 else Color.BLACK

    @staticmethod
    def _prompt_choice(message: str, choices: list[int]) -> int:
        while True:
            choice = input(
                message + " ",
            )
            if choice not in choices:
                print("Invalid choice.")
                continue
            break
        return choice
