from enums.game_mode import GameMode
from models.game import Game
from models.move import Move
from models.move_parser import MoveParser
from models.move_validator import MoveValidator
from models.rules import Rules
from utils.board_utils import calculate_mask
from views.board_view import BoardView
from views.game_view import GameView


class GameController:
    def __init__(self, game: Game) -> None:
        self._game = game

    def configure(self) -> None:
        self._game._mode = GameView.prompt_game_mode()
        if self._game._mode == GameMode.VS_AI:
            self._game._ai_depth = GameView.prompt_ai_depth()
            self._game._player_color = GameView.prompt_player_color()

    def play(self) -> None:
        while True:
            BoardView.print(self._game._current_color, self._game._board)

            if (
                self._game._mode == GameMode.VS_PLAYER
                or self._game._current_color == self._game._player_color
            ):
                self._take_player_turn()
            else:
                self._take_ai_turn()

            if Rules.is_in_checkmate(
                self._game._current_color.opposite, self._game._board
            ):
                break

            self._game._current_color = self._game._current_color.opposite

        BoardView.print(self._game._current_color, self._game._board)
        print(f"🎉 {self._game._current_color} wins by checkmate!")

    def _take_player_turn(self) -> None:
        if Rules.is_in_check(self._game._current_color, self._game._board):
            print("You are in check.")

        while True:
            move_input = GameView.prompt_move()
            move_tuple = MoveParser.parse_input(move_input)

            if move_tuple is None:
                print("Invalid format.")
                continue

            from_row_index, from_column_index, to_row_index, to_column_index = (
                move_tuple
            )
            from_square_mask = calculate_mask(from_row_index, from_column_index)
            to_square_mask = calculate_mask(to_row_index, to_column_index)
            from_piece = self._game._board._get_piece(from_square_mask)
            to_piece = self._game._board._get_piece(to_square_mask)
            move = Move(
                from_square_mask,
                to_square_mask,
                from_piece,
                to_piece,
                self._game._current_color,
            )

            if not MoveValidator.is_valid_move(move):
                print("Invalid move.")
                continue

            if not Rules.is_legal_move(move, self._game._board):
                print("Illegal move.")
                continue

            if Rules.is_in_check_after_move(move, self._game._board):
                print("Illegal move. You would be in check.")
                continue

            break

        self._game.make_move(move)

        # TODO: promotion + AI always queens?

    def _take_ai_turn(self) -> None:
        # ai get best move
        # make move
        pass
