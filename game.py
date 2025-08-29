from controllers.board_controller import BoardController
from enums.color import Color
from enums.game_mode import GameMode
from models.input_parser import InputParser
from models.input_validator import InputValidator
from models.move import Move
from models.move_validator import MoveValidator
from views.board_view import BoardView
from views.game_view import GameView


class Game:
    def __init__(self, board_controller: BoardController) -> None:
        self._board_controller = board_controller
        self._game_mode = GameMode.TWO_PLAYER
        self.player_color = Color.WHITE
        self._ai_depth = 0

    def configure(self) -> None:
        """Prompt the user to configure the game options."""
        self._game_mode = GameView.prompt_game_mode()

        if self._game_mode == GameMode.TWO_PLAYER:
            return

        self.player_color = GameView.prompt_player_color()
        self.ai_depth = GameView.prompt_ai_depth()

    def play(self) -> None:
        """Play a game of chess."""
        match self._game_mode:
            case GameMode.TWO_PLAYER:
                self._play_two_player()
            case GameMode.AI:
                self._play_ai()
            case _:
                raise ValueError

    def _play_two_player(self) -> None:
        """Play a game of chess between two humans."""
        winner_color = None
        current_color = Color.WHITE
        while winner_color is None:
            BoardView.draw(current_color, self._board_controller.board)

            is_in_check = self._board_controller.is_in_check(current_color)
            GameView.show_turn_status(current_color, is_in_check)

            move = self._handle_move(current_color)
            self._handle_promotion(move)

            opponent_color = current_color.opposite
            if self._board_controller.is_in_checkmate(opponent_color):
                winner_color = current_color
            current_color = opponent_color
        BoardView.draw(winner_color, self._board_controller.board)
        GameView.show_winner_message(winner_color)

    def _play_ai(self) -> None:
        """Play a game of chess between a human and the AI."""
        raise NotImplementedError

    def _handle_move(self, color: Color) -> Move:
        """Prompt the user for a valid move, then make the move and return the move."""
        is_legal_move = False
        while not is_legal_move:
            move_coordinates = GameView.prompt_move_coordinates()
            if not InputValidator.is_valid_move_input(move_coordinates):
                GameView.show_invalid_input()
                continue

            from_coordinate, to_coordinate = InputParser.parse_input(move_coordinates)
            from_piece = self._board_controller.board.get_piece(from_coordinate)
            to_piece = self._board_controller.board.get_piece(to_coordinate)
            move = Move(color, from_coordinate, to_coordinate, from_piece, to_piece)
            if not MoveValidator.is_move_valid(move, self._board_controller.board):
                GameView.show_illegal_move()
                continue

            self._board_controller.make_move(move)
            is_in_check = self._board_controller.is_in_check(color)
            if is_in_check:
                self._board_controller.undo_move(move)
                GameView.show_illegal_move(is_in_check)
                continue

            is_legal_move = True
        return move

    def _handle_promotion(self, move: Move) -> None:
        """Check if the move meets the criteria for promotion, prompt the user
        for the new piece type, and promote the pawn."""
        if not self._board_controller.does_move_trigger_promotion(move):
            return

        BoardView.draw(move.color, self._board_controller.board)
        new_piece_type = GameView.prompt_promotion()
        new_piece = new_piece_type(move.color)
        self._board_controller.board.set_piece(move.to_coordinate, new_piece)
