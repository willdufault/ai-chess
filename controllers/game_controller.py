from enums.color import Color
from enums.game_mode import GameMode
from models.game import Game
from models.input_parser import InputParser
from models.input_validator import InputValidator
from models.move import Move
from models.move_validator import MoveValidator
from models.pieces import Bishop, Knight, Queen, Rook
from models.rules import Rules
from views.board_view import BoardView
from views.game_view import GameView


class GameController:
    def __init__(self, game: Game) -> None:
        self._game = game

    def configure(self) -> None:
        """Prompt the user to configure the game options."""
        self._game.game_mode = GameView.prompt_game_mode()

        if self._game.game_mode == GameMode.TWO_PLAYER:
            return

        self._game.player_color = GameView.prompt_player_color()
        self._game.ai_depth = GameView.prompt_ai_depth()

    def play(self) -> None:
        """Play a game of chess."""
        match self._game.game_mode:
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
            BoardView.draw(current_color, self._game.board)

            is_in_check = Rules.is_in_check(current_color, self._game.board)
            GameView.show_turn_status(current_color, is_in_check)

            move = self._handle_move(current_color)
            self._handle_promotion(move)

            opponent_color = current_color.opposite
            if Rules.is_in_checkmate(opponent_color, self._game.board):
                winner_color = current_color
            current_color = opponent_color
        BoardView.draw(winner_color, self._game.board)
        GameView.show_winner_message(winner_color)

    def _play_ai(self) -> None:
        """Play a game of chess between a human and the AI."""
        raise NotImplementedError

    def _handle_move(self, color: Color) -> Move:
        """Prompt the user for a valid move, then make and return the move."""
        is_legal_move = False
        while not is_legal_move:
            move_coordinates = GameView.prompt_move_coordinates()
            if not InputValidator.is_valid_move_input(move_coordinates):
                GameView.show_invalid_input()
                continue

            from_coordinate, to_coordinate = InputParser.parse_input(move_coordinates)
            from_piece = self._game.get_piece(from_coordinate)
            to_piece = self._game.get_piece(to_coordinate)
            move = Move(color, from_coordinate, to_coordinate, from_piece, to_piece)
            if not MoveValidator.is_move_valid(move, self._game.board):
                GameView.show_illegal_move()
                continue

            is_in_check = Rules.is_in_check_after_move(move, self._game.board)
            if is_in_check:
                GameView.show_illegal_move(is_in_check)
                continue

            self._game.make_move(move)
            is_legal_move = True
        return move

    def _handle_promotion(self, move: Move) -> None:
        """Check if the move meets the criteria for promotion, prompt the user
        for the new piece type, and promote the pawn."""
        if not Rules.does_move_trigger_promotion(move):
            return

        BoardView.draw(move.color, self._game.board)
        new_piece_choice = GameView.prompt_promotion()
        match new_piece_choice:
            case "k":
                new_piece = Knight(move.color)
            case "b":
                new_piece = Bishop(move.color)
            case "r":
                new_piece = Rook(move.color)
            case "q":
                new_piece = Queen(move.color)
            case _:
                raise ValueError
        self._game.set_piece(move.to_coordinate, new_piece)
