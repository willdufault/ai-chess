from enums import Color, GameMode

from .ai import AI, MAX_DEPTH
from .board import BOARD_SIZE, Board
from .coordinate import Coordinate
from .move import Move
from .pieces import Bishop, FirstMovePiece, Knight, Pawn, Piece, Queen, Rook

MOVE_INPUT_LEN = 4


class Game:
    """Represents a chess game."""

    def __init__(self, board: Board) -> None:
        self._board = board
        self._game_mode = GameMode.TWO_PLAYER
        self._user_color = Color.WHITE
        self._depth = 0

    def make_move(
        self, color: Color, from_coord: Coordinate, to_coord: Coordinate
    ) -> bool:
        """Make a move and return whether it was successful."""
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

        to_piece = self._board.get_piece(to_coord)
        move = Move(from_coord, to_coord, from_piece, to_piece)
        self._board.make_move(move)
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

        turn_color = Color.WHITE
        winner = None
        while winner is None:
            self._board.draw(turn_color)

            print(f"\nIt's {str(turn_color).lower()}'s turn.")
            if self._board.is_in_check(turn_color):
                print(f"You are in check.")

            to_coord = self._handle_move(turn_color)
            self._handle_promotion(turn_color, to_coord)

            other_color = Color.get_other_color(turn_color)
            if self._board.is_in_checkmate(other_color):
                winner = turn_color
            turn_color = other_color

        self._board.draw(winner)
        print(f"{winner} won by checkmate!")

    def _handle_move(self, color: Color) -> Coordinate:
        """Get the move from the user input, validate it, then make the move and
        return the to coordinate."""
        is_legal_move = False
        while not is_legal_move:
            move_coords = input("Where would you like to move (rcrc)? ")
            if not self._is_valid_input(move_coords):
                print("Invalid input.\n")
                continue

            from_coord, to_coord = self._parse_input(move_coords)
            from_piece = self._board.get_piece(from_coord)
            from_piece_has_moved = (
                from_piece.has_moved
                if isinstance(from_piece, FirstMovePiece)
                else False
            )
            to_piece = self._board.get_piece(to_coord)
            is_legal_move = self.make_move(color, from_coord, to_coord)
            if not is_legal_move:
                print("Illegal move.\n")
                continue

            if self._board.is_in_check(color):
                self._board.undo_move(
                    from_coord, to_coord, to_piece, from_piece_has_moved
                )
                print("Illegal move. Your king would be in check.\n")
                continue

            is_legal_move = True
        return to_coord

    def _handle_promotion(self, color: Color, coord: Coordinate) -> None:
        """Get the new piece from the user input and promote the pawn at the coordinate."""
        last_row_idx = self._board.get_last_row(color)
        piece = self._board.get_piece(coord)
        is_promoting = coord.row_idx == last_row_idx and isinstance(piece, Pawn)
        if not is_promoting:
            return

        self._board.draw(color)
        print()

        new_piece_options = ("k", "b", "r", "q")
        new_piece_choice = self._prompt_user(
            new_piece_options,
            "What would you like to promote to? (k/b/r/q)",
        )
        match new_piece_choice:
            case "k":
                new_piece = Knight(color)
            case "b":
                new_piece = Bishop(color)
            case "r":
                new_piece = Rook(color)
            case "q":
                new_piece = Queen(color)

        self._promote(coord, new_piece)

    def _promote(self, coord: Coordinate, piece: Piece) -> None:
        """Place the piece at the coordinate."""
        self._board.set_piece(coord, piece)

    def _is_valid_input(self, move_input: str) -> bool:
        """Return whether the user input is valid."""
        if len(move_input) != MOVE_INPUT_LEN:
            return False

        for char in move_input:
            if not char.isdigit():
                return False

            is_in_bounds = 0 <= int(char) < BOARD_SIZE
            if not is_in_bounds:
                return False

        return True

    def _parse_input(self, move_input: str) -> tuple[Coordinate, Coordinate]:
        """Return the from and to coordinates from the input. Assumes the input
        is valid."""
        from_row_idx, from_col_idx, to_row_idx, to_col_idx = tuple(map(int, move_input))
        from_coord = Coordinate(from_row_idx, from_col_idx)
        to_coord = Coordinate(to_row_idx, to_col_idx)
        return from_coord, to_coord

    def _prompt_user(self, options: tuple[str], message: str) -> str:
        """Prompt the user to choose from the options given a message."""
        choice = None

        while choice not in options:
            if choice is not None:
                print("Invalid choice.\n")

            choice = input(f"{message} ")

        return choice

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
