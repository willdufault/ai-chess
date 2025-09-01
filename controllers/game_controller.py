from enums.color import Color
from enums.game_mode import GameMode
from models.ai import AI
from models.game import Game
from models.input_parser import InputParser
from models.input_validator import InputValidator
from models.move import Move
from models.move_validator import MoveValidator
from models.pieces import Bishop, Knight, Piece, Queen, Rook
from models.rules import Rules
from views.board_view import BoardView
from views.game_view import GameView


class GameController:
    def __init__(self, game: Game, ai: AI) -> None:
        self._game = game
        self._ai = ai
        self._game_mode = GameMode.TWO_PLAYER

    def configure(self) -> None:
        """Prompt the user to configure the game options."""
        self._game_mode = GameView.prompt_game_mode()
        if self._game_mode == GameMode.TWO_PLAYER:
            return

        human_color = GameView.prompt_human_color()
        self._ai.color = human_color.opposite
        self._ai.depth = GameView.prompt_ai_depth()

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
        while winner_color is None:
            BoardView.draw(self._game.current_color, self._game.board)
            is_in_check = Rules.is_in_check(self._game.current_color, self._game.board)
            GameView.show_turn_status(self._game.current_color, is_in_check)

            self._handle_human_move(self._game.current_color)

            if Rules.is_in_checkmate(
                self._game.current_color.opposite, self._game.board
            ):
                winner_color = self._game.current_color
            else:
                self._game.current_color = self._game.current_color.opposite
        BoardView.draw(winner_color, self._game.board)
        GameView.show_winner_message(winner_color)

    def _play_ai(self) -> None:
        """Play a game of chess between a human and the AI."""
        winner_color = None
        while winner_color is None:
            BoardView.draw(self._game.current_color, self._game.board)
            is_in_check = Rules.is_in_check(self._game.current_color, self._game.board)
            GameView.show_turn_status(self._game.current_color, is_in_check)

            if self._game.current_color == self._ai.color:
                self._handle_ai_move(self._game.current_color)
            else:
                self._handle_human_move(self._game.current_color)

            if Rules.is_in_checkmate(
                self._game.current_color.opposite, self._game.board
            ):
                winner_color = self._game.current_color
            else:
                self._game.current_color = self._game.current_color.opposite
        BoardView.draw(winner_color, self._game.board)
        GameView.show_winner_message(winner_color)
        breakpoint()

    def _handle_human_move(self, color: Color) -> None:
        """Prompt the player to make a legal move for the color and promote if
        applicable."""
        move = self._prompt_legal_move(color)
        self._game.make_move(move)
        self._handle_human_promotion(move)

    def _handle_ai_move(self, color: Color) -> None:
        """Have the AI choose a move for the color and promote if applicable."""
        move = self._ai.get_best_move(color)
        self._game.make_move(move)
        self._handle_ai_promotion(move)

    def _prompt_legal_move(self, color: Color) -> Move:
        """Prompt the user for a legal move and return it."""
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

            is_legal_move = True
        return move

    def _handle_human_promotion(self, move: Move) -> None:
        """If the move triggers promotion, prompt the player for a new piece and
        promote the pawn."""
        if Rules.does_move_trigger_promotion(move):
            new_piece = self._prompt_promotion_piece(move)
            self._game.set_piece(move.to_coordinate, new_piece)

    def _handle_ai_promotion(self, move: Move) -> None:
        """If the move triggers promotion, have the AI choose a piece to promote to."""
        if Rules.does_move_trigger_promotion(move):
            # TODO
            print("Game._handle_ai_promotion NOT IMPLEMENTED YET!")

    def _prompt_promotion_piece(self, move: Move) -> Piece:
        """Prompt the user for the new piece and return it."""
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
        return new_piece
