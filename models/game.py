from enums import Color, GameMode

from .board import BOARD_SIZE, Board
from .coordinate import Coordinate
from .pieces import FirstMovePiece, Piece

MAX_DEPTH = 10


class Game:
    """Represents a chess game."""

    def __init__(self, board: Board) -> None:
        self._board = board
        self._game_mode = GameMode.TWO_PLAYER
        self._user_color = Color.WHITE
        self._depth = 0

    # TODO: PICK UP HERE, COORD REFACTOR

    def move(self, color: Color, from_coord: Coordinate, to_coord: Coordinate) -> bool:
        """Return whether the move was successful."""
        if not self._move_passes_basic_checks(color, from_coord, to_coord):
            return False

        from_piece = self._board.get_piece(from_coord)
        if not from_piece.move_strategy.is_valid_move(
            color,
            from_coord,
            to_coord,
            self._board,
        ):
            return False

        self._move_piece(from_coord, to_coord, from_piece)
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

        # TODO: Implement AI game loop.
        # TODO: Implement pawn promotion.
        if self._game_mode is GameMode.AI:
            raise NotImplementedError

        color = Color.WHITE
        winner = Color.WHITE
        while True:
            self._board.draw(color)

            is_in_check = self._board.is_in_check(color)
            if is_in_check and self._board.is_king_trapped(color):
                winner = Color.get_opposite_color(color)
                break

            print(f"\nIt's {'white' if color is Color.WHITE else 'black'}'s turn.")

            if is_in_check:
                print("You are in check.")

            # TODO: This can be cleaned up, weird structure break @ bottom
            while True:
                move_coords = input("Where would you like to move (rcrc)? ")
                if not self.is_valid_input(move_coords):
                    print("Invalid input.\n")
                    continue

                from_coord, to_coord = self._parse_input(move_coords)
                from_piece = self._board.get_piece(from_coord)
                to_piece = self._board.get_piece(to_coord)

                moved = self.move(color, from_coord, to_coord)
                if not moved:
                    print("Illegal move.\n")
                    continue

                if self._board.is_in_check(color):
                    # ! could fail, if that piece was blocking check but is now gone
                    self.move(color, to_coord, from_coord)
                    self._board._set_piece(to_coord, to_piece)

                    print("Illegal move. Your king would be in check.\n")
                    continue

                # todo: MOVED INTO BOARD, REFACTOR
                if isinstance(from_piece, FirstMovePiece):
                    from_piece.has_moved = True

                break

            color = Color.get_opposite_color(color)

        print(f"{'White' if winner is Color.WHITE else 'Black'} won by checkmate!")

    # DONE
    def is_valid_input(self, move_input: str) -> bool:
        """Return whether the user input is valid."""
        expected_len = 4

        if len(move_input) != expected_len:
            return False

        for char in move_input:
            if not char.isdigit():
                return False

            is_in_bounds = 0 <= int(char) < BOARD_SIZE

            if not is_in_bounds:
                return False

        return True

    # DONE
    def _parse_input(self, move_input: str) -> tuple[Coordinate, Coordinate]:
        """Return the from and to coordinates from the input. Assumes the input
        is valid."""
        from_row_idx, from_col_idx, to_row_idx, to_col_idx = tuple(map(int, move_input))
        from_coord = Coordinate(from_row_idx, from_col_idx)
        to_coord = Coordinate(to_row_idx, to_col_idx)
        return from_coord, to_coord

    # DONE
    def _prompt_user(self, options: list[str], message: str) -> str:
        """Prompt the user to choose from the options given a message."""
        choice = None

        while choice not in options:
            if choice is not None:
                print("Invalid choice.\n")

            choice = input(f"{message} ")

        return choice

    # DONE
    def _move_passes_basic_checks(
        self, color: Color, from_coord: Coordinate, to_coord: Coordinate
    ) -> bool:
        """Return whether the move passes basic legality checks."""
        are_coords_in_bounds = self._board.is_in_bounds(
            from_coord
        ) and self._board.is_in_bounds(to_coord)

        if not are_coords_in_bounds:
            return False

        from_piece = self._board.get_piece(from_coord)
        is_moving_wrong_piece = from_piece is None or from_piece.color != color

        if is_moving_wrong_piece:
            return False

        to_piece = self._board.get_piece(to_coord)
        is_to_same_color = to_piece is not None and to_piece.color == color

        if is_to_same_color:
            return False

        return True

    #! ENCAPSULATION?
    def _move_piece(
        self, from_coord: Coordinate, to_coord: Coordinate, from_piece: Piece
    ) -> None:
        """Move a piece. Assuming this is a legal move."""
        self._board._set_piece(from_coord, None)
        self._board._set_piece(to_coord, from_piece)
