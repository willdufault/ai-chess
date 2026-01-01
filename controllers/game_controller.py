from enums.color import Color
from enums.game_mode import GameMode
from enums.game_status import GameStatus
from enums.promotion_piece import PromotionPiece
from models.ai import Ai
from models.ai_factory import AiFactory
from models.game import Game
from models.move import Move
from models.move_parser import MoveParser
from models.move_validator import MoveValidator
from models.piece import Bishop, Knight, Queen, Rook
from models.rules import Rules
from utils.board_utils import calculate_mask
from views.board_view import BoardView
from views.game_view import GameView


class GameController:
    def __init__(self, game: Game, ai_factory: AiFactory) -> None:
        self._game = game
        self._ai_factory = ai_factory
        self._game_mode = GameMode.VS_PLAYER
        self._ai_depth = 0
        self._player_color = Color.WHITE
        self._ai = None

    def configure(self) -> None:
        self._game_mode = GameView.prompt_game_mode()
        if self._game_mode == GameMode.VS_AI:
            self._ai_depth = GameView.prompt_ai_depth()
            self._player_color = GameView.prompt_player_color()
            self._ai = self._ai_factory.get_ai(self._ai_depth)

    def play(self) -> None:
        while self._game.status == GameStatus.ACTIVE:
            BoardView.print(self._game.current_color, self._game.board)

            if (
                self._game_mode == GameMode.VS_PLAYER
                or self._game.current_color == self._player_color
            ):
                self._take_player_turn()
            else:
                self._take_ai_turn()

            if Rules.is_in_checkmate(
                self._game.current_color.opposite, self._game.board
            ):
                self._game.status = GameStatus.CHECKMATE
                break

            if Rules.is_in_stalemate(self._game.current_color, self._game.board):
                self._game.status = GameStatus.STALEMATE
                break

            self._game.current_color = self._game.current_color.opposite

        match self._game.status:
            case GameStatus.CHECKMATE:
                BoardView.print(self._game.current_color, self._game.board)
                print(f"🎉 {self._game.current_color} wins by checkmate!")
            case GameStatus.STALEMATE:
                BoardView.print(self._game.current_color, self._game.board)
                print(f"🤝 Draw by stalemate.")
            case _:
                raise ValueError(f"Unknown game status: {self._game.status}")

    def _take_player_turn(self) -> None:
        if Rules.is_in_check(self._game.current_color, self._game.board):
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
            from_piece = self._game.board._get_piece(from_square_mask)
            to_piece = self._game.board._get_piece(to_square_mask)
            move = Move(
                from_square_mask,
                to_square_mask,
                from_piece,
                to_piece,
                self._game.current_color,
            )

            ignoring_checks = move_input.endswith("!")
            if not ignoring_checks:
                if not MoveValidator.is_valid_move(move):
                    print("Invalid move.")
                    continue

                if not Rules.is_legal_move(move, self._game.board):
                    print("Illegal move.")
                    continue

                if Rules.is_in_check_after_move(move, self._game.board):
                    print("Illegal move. You would be in check.")
                    continue

            break

        self._game.make_move(move)

        if Rules.can_promote(move):
            promotion_piece = GameView.prompt_promotion()
            self._promote_player(move, promotion_piece)

    def _promote_player(self, move: Move, promotion_piece: PromotionPiece) -> None:
        match promotion_piece:
            case PromotionPiece.KNIGHT:
                piece = Knight(move.color)
            case PromotionPiece.BISHOP:
                piece = Bishop(move.color)
            case PromotionPiece.ROOK:
                piece = Rook(move.color)
            case PromotionPiece.QUEEN:
                piece = Queen(move.color)
            case _:
                raise ValueError(f"Invalid promotion piece: {promotion_piece}")
        self._game.board._set_piece(piece, move.to_square_mask)

    def _take_ai_turn(self) -> None:
        # ai get best move
        assert isinstance(self._ai, Ai)
        move = self._ai.calculate_best_move(
            self._player_color.opposite, self._game.board
        )
        self._game.make_move(move)
        # TODO: promo queen?
        pass
