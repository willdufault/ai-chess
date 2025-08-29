from enums.color import Color
from enums.game_mode import GameMode
from models.ai import MAX_DEPTH
from models.pieces import Bishop, Knight, Queen, Rook


class GameView:
    """Handles prompting the user for game-related inputs."""

    @classmethod
    def prompt_game_mode(cls) -> GameMode:
        """Prompt the user for the game mode and return it."""
        game_mode_options = ("2p", "ai")
        game_mode_choice = cls._prompt_choice(
            game_mode_options,
            "Would you like to play 2-player or against our AI? (2p/ai)",
        )
        game_mode = GameMode.TWO_PLAYER if game_mode_choice == "2p" else GameMode.AI
        return game_mode

    @classmethod
    def prompt_player_color(cls) -> Color:
        """Prompt the user for the player color and return it."""
        player_color_options = ("w", "b")
        player_color_choice = cls._prompt_choice(
            player_color_options, "Would you like to play as white or black? (w/b)"
        )
        player_color = Color.WHITE if player_color_choice == "w" else Color.BLACK
        return player_color

    @classmethod
    def prompt_ai_depth(cls) -> int:
        """Prompt the user for the AI depth and return it."""
        ai_depth_options = tuple(map(str, range(MAX_DEPTH + 1)))
        ai_depth_choice = cls._prompt_choice(
            ai_depth_options,
            f"What would you like the AI depth to be? (0-{MAX_DEPTH}, higher is smarter but slower)",
        )
        ai_depth = int(ai_depth_choice)
        return ai_depth

    @staticmethod
    def prompt_move_coordinates() -> str:
        """Prompt the user for from and to coordinates for a move."""
        move_coords = input("Where would you like to move (rcrc)? ")
        return move_coords

    @classmethod
    def prompt_promotion(cls) -> type[Knight | Bishop | Rook | Queen]:
        """Prompt the user for the piece type to promote their pawn to."""
        new_piece_options = ("k", "b", "r", "q")
        new_piece_choice = cls._prompt_choice(
            new_piece_options,
            "What would you like to promote to? (k/b/r/q)",
        )
        match new_piece_choice:
            case "k":
                return Knight
            case "b":
                return Bishop
            case "r":
                return Rook
            case "q":
                return Queen
            case _:
                raise ValueError

    @staticmethod
    def show_turn_status(current_color: Color, is_in_check: bool) -> None:
        """Print the color whose turn it is and whether they are in check."""
        print(f"It's {str(current_color).lower()}'s turn.")
        if is_in_check:
            print(f"You are in check.")

    @staticmethod
    def show_invalid_input() -> None:
        """Tell the user the previous input is invalid."""
        print("Invalid input.")

    @staticmethod
    def show_illegal_move(is_in_check: bool | None = None) -> None:
        """Tell the user the previous move is illegal. Optionally, display
        whether the move would reveal a discovered check on their own king."""
        if is_in_check is None:
            is_in_check = False

        if is_in_check:
            print("Illegal move. Your king would be in check.")
        else:
            print("Illegal move.")

    @staticmethod
    def show_winner_message(winner_color: Color) -> None:
        """Tell the user which color won the game."""
        # TODO: add another arg for how won happen, enum
        print(f"{winner_color} won by checkmate!")

    @staticmethod
    def _prompt_choice(options: tuple[str, ...], message: str) -> str:
        """Prompt the user to choose from the options given a message."""
        choice = None
        while choice not in options:
            if choice is not None:
                print("Invalid choice.")
            choice = input(f"{message} ")
        return choice
