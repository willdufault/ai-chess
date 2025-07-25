from board import BOARD_SIZE, Board
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
        """Return whether the move was successful."""
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
            user_color_options, "Would you like to play as white (w) or black (b)?"
        )
        self._user_color = Color.WHITE if user_color_choice == "w" else Color.BLACK

        depth_options = tuple(map(str, range(0, MAX_DEPTH + 1)))
        depth_choice = self._prompt_user(
            depth_options,
            f"What would you like the AI depth to be (0-{MAX_DEPTH}, higher is smarter but slower)?",
        )
        self._depth = int(depth_choice)

    def play(self) -> None:
        """Play a game of chess."""

        # TODO:
        if self._game_mode is GameMode.AI:
            raise NotImplementedError

        color_turn = Color.WHITE
        other_color = Color.BLACK
        while True:
            self._board.draw(color_turn)
            print(f"\nIt's {'white' if color_turn == Color.WHITE else 'black'}'s turn.")

            if self._board.is_king_under_attack(color_turn):
                print("You are in check.")

            # TODO: This can be cleaned up, weird structure break @ bottom
            while True:
                move_coords = input("Where would you like to move (rcrc)? ")
                if not self.is_valid_input(move_coords):
                    print("Invalid input.\n")
                    continue

                from_row_idx, from_col_idx, to_row_idx, to_col_idx = self._parse_input(
                    move_coords
                )
                to_piece = self._board.get_piece(to_row_idx, to_col_idx)

                moved = self.move(
                    color_turn, from_row_idx, from_col_idx, to_row_idx, to_col_idx
                )
                if not moved:
                    print("Illegal move.\n")
                    continue

                if self._board.is_king_under_attack(color_turn):
                    self.move(
                        color_turn, to_row_idx, to_col_idx, from_row_idx, from_col_idx
                    )
                    self._board.set_piece(to_row_idx, to_col_idx, to_piece)

                    print("Illegal move. Your king would be in check.\n")
                    continue

                break

            if self._board.is_king_under_attack(
                other_color
            ) and self._board.is_king_trapped(other_color):
                break

            color_turn, other_color = other_color, color_turn

            # print board
            # print if under check
            # prompt coords
            # check valid
            # check legal move
            # move piece
            # if under check, move back
            # check for mate

        print(f"{'White' if color_turn is Color.WHITE else 'Black'} won by checkmate!")
        """
        color_turn = white
        while true
            color move
            check win, exit
            color = other color
        return winner
        """

    def is_valid_input(self, move_coords: str) -> bool:
        """Return whether the input is valid."""
        idx_cnt = 4
        if len(move_coords) != idx_cnt:
            return False

        for char in move_coords:
            if not char.isdigit():
                return False

            idx = int(char)
            if idx < 0 or BOARD_SIZE <= idx:
                return False

        return True

    def _parse_input(self, move_coords: str) -> tuple[int, int, int, int]:
        """Return the from and to coordinates from the input."""
        from_row_idx, from_col_idx, to_row_idx, to_col_idx = tuple(
            map(int, move_coords)
        )
        return from_row_idx, from_col_idx, to_row_idx, to_col_idx

    def _prompt_user(self, options: tuple[str], message: str) -> str:
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
    g = Game(Board())
    cw = Color.WHITE
    cb = Color.BLACK

    g._board.draw(cw)
    g._board.draw(cb)
    breakpoint()
