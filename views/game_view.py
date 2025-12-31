from constants.ai_constants import MAX_AI_DEPTH
from enums.color import Color
from enums.game_mode import GameMode
from enums.promotion_piece import PromotionPiece


class GameView:
    @classmethod
    def prompt_game_mode(cls) -> GameMode:
        message = "Choose a game mode: (1) player vs. player, or (2) player vs. AI."
        choices = ["1", "2"]
        choice = cls._prompt_choice(message, choices)
        return GameMode.VS_PLAYER if choice == "1" else GameMode.VS_AI

    @classmethod
    def prompt_ai_depth(cls) -> int:
        message = f"Choose an AI depth from 0 to {MAX_AI_DEPTH} (higher = smarter but slower)."
        choices = list(map(str, range(MAX_AI_DEPTH + 1)))
        return int(cls._prompt_choice(message, choices))

    @classmethod
    def prompt_player_color(cls) -> Color:
        message = f"Choose your color: (1) white, or (2) black."
        choices = ["1", "2"]
        choice = cls._prompt_choice(message, choices)
        return Color.WHITE if choice == "1" else Color.BLACK

    @staticmethod
    def prompt_move() -> str:
        return input(
            'Enter a move in the format "rcrc" (row/column → row/column). ',
        )

    @classmethod
    def prompt_promotion(cls) -> PromotionPiece:
        message = f"Choose a piece to promote to: (1) Knight, (2) Bishop, (3) Rook, or (4) Queen."
        choices = ["1", "2", "3", "4"]
        choice = cls._prompt_choice(message, choices)
        match choice:
            case "1":
                return PromotionPiece.KNIGHT
            case "2":
                return PromotionPiece.BISHOP
            case "3":
                return PromotionPiece.ROOK
            case "4":
                return PromotionPiece.QUEEN
            case _:
                raise ValueError(f"Invalid promotion piece: {choice}")

    @staticmethod
    def _prompt_choice(message: str, choices: list[str]) -> str:
        while True:
            choice = input(
                message + " ",
            )
            if choice not in choices:
                print("Invalid choice.")
                continue
            break
        return choice
