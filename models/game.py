from enums.color import Color
from enums.game_mode import GameMode
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.pieces import Piece


class Game:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._game_mode = GameMode.TWO_PLAYER
        self._current_color = Color.WHITE
        self._player_color = Color.WHITE
        self._ai_depth = 0

    @property
    def board(self) -> Board:
        return self._board

    @property
    def game_mode(self) -> GameMode:
        return self._game_mode

    @game_mode.setter
    def game_mode(self, game_mode: GameMode) -> None:
        self._game_mode = game_mode

    @property
    def current_color(self) -> Color:
        return self._current_color

    @current_color.setter
    def current_color(self, current_color: Color) -> None:
        self._current_color = current_color

    @property
    def player_color(self) -> Color:
        return self._player_color

    @player_color.setter
    def player_color(self, player_color: Color) -> None:
        self._player_color = player_color

    @property
    def ai_depth(self) -> int:
        return self._ai_depth

    @ai_depth.setter
    def ai_depth(self, ai_depth: int) -> None:
        self._ai_depth = ai_depth

    def make_move(self, move: Move) -> None:
        """Make the move and update the state of the from piece."""
        self._board.make_move(move)

    def undo_move(self, move: Move) -> None:
        """Undo a move and restore the state of both the from and to pieces."""
        self._board.undo_move(move)

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        self._board.get_piece(coordinate)

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        self._board.set_piece(coordinate, piece)
