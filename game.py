from board import Board
from enums import Color, GameMode
from pieces import Piece

MAX_DEPTH = 10


class Game:
    """Represents a chess game."""

    def __init__(self, board: Board) -> None:
        self._board = board
        self._game_mode = GameMode.TWO_PLAYER
        self._user_color = Color.WHITE
        self._depth = 0

    def move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
    ) -> bool:
        """Return whether the move was made."""
        if not self._move_passes_basic_checks(
            color, from_row_idx, from_col_idx, to_row_idx, to_col_idx
        ):
            return False

        from_piece = self._board.get_piece(from_row_idx, from_col_idx)
        if not from_piece.move_strategy.is_legal_move(
            color,
            from_row_idx,
            from_col_idx,
            to_row_idx,
            to_col_idx,
            self._board,
        ):
            return False

        self._move_piece(from_row_idx, from_col_idx, to_row_idx, to_col_idx, from_piece)

        if from_piece.tracks_first_move:
            from_piece.has_moved = True

        return True

    def configure(self) -> None:
        """Prompt the user to configure the game."""
        game_mode_options = ("1", "2")
        game_mode_choice = self._prompt_user(
            game_mode_options,
            "Would you like to play 2-player (1) or against our AI (2)?",
        )
        self._game_mode = (
            GameMode.TWO_PLAYER if game_mode_choice == "1" else GameMode.AI
        )

        if self._game_mode == GameMode.TWO_PLAYER:
            return

        user_color_options = ("w", "b")
        user_color_choice = self._prompt_user(
            user_color_options, 'Would you like to play as white ("w") or black ("b")?'
        )
        self._user_color = Color.WHITE if user_color_choice == "w" else Color.BLACK

        depth_options = tuple(map(str, range(0, MAX_DEPTH + 1)))
        depth_choice = self._prompt_user(
            depth_options,
            f"What would you like the AI depth to be (0-{MAX_DEPTH}, higher is smarter but slower)?",
        )
        self._depth = int(depth_choice)

    def play(self) -> None:
        breakpoint()
        pass

    def _prompt_user(self, options: list[str], message: str) -> str:
        """Prompt the user to choose from the options given a message."""
        choice = None
        while choice not in options:
            if choice is not None:
                print("Invalid choice.\n")

            choice = input(f"{message} ")
        return choice

    def _move_passes_basic_checks(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
    ) -> bool:
        """Return whether the move passes basic legality checks."""
        is_from_in_bounds = self._board.is_in_bounds(from_row_idx, from_col_idx)
        is_to_in_bounds = self._board.is_in_bounds(to_row_idx, to_col_idx)
        if not (is_from_in_bounds and is_to_in_bounds):
            return False

        from_piece = self._board.get_piece(from_row_idx, from_col_idx)
        is_moving_wrong_piece = from_piece is None or from_piece.color != color
        if is_moving_wrong_piece:
            return False

        to_piece = self._board.get_piece(to_row_idx, to_col_idx)
        is_to_same_color = to_piece is not None and to_piece.color == color
        if is_to_same_color:
            return False

        return True

    def _move_piece(
        self,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        from_piece: Piece,
    ) -> None:
        """Move a piece. Assuming this is a legal move."""
        self._board.set_piece(from_row_idx, from_col_idx, None)
        self._board.set_piece(to_row_idx, to_col_idx, from_piece)


if __name__ == "__main__":
    from pieces import Pawn

    g = Game(Board())
    cw = Color.WHITE
    cb = Color.BLACK

    g._board.set_piece(1, 4, None)
    print(g._board)
    breakpoint()
