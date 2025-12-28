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
        self._game._game_mode = GameView.prompt_game_mode()
        if self._game._game_mode == GameMode.PLAYER_VS_AI:
            self._game._ai_depth = GameView.prompt_ai_depth()
            self._game._player_color = GameView.prompt_player_color()

    def play(self) -> None:
        if self._game._game_mode == GameMode.PLAYER_VS_PLAYER:
            self._play_player_vs_player()
        else:
            self._play_player_vs_ai()

    def _play_player_vs_player(self) -> None:
        while True:
            BoardView.print(self._game._current_color, self._game._board)

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
                # TODO: trans nav: code smell?
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

            # 3.4 in mate? print board + exit
            if Rules.is_in_checkmate(
                self._game._current_color.opposite, self._game._board
            ):
                break

            self._game._current_color = self._game._current_color.opposite

        BoardView.print(self._game._current_color, self._game._board)
        print(f"🎉 {self._game._current_color} wins by checkmate!")

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
