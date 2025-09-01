from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.pieces import Piece


class Game:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._current_color = Color.WHITE

    @property
    def board(self) -> Board:
        return self._board

    @property
    def current_color(self) -> Color:
        return self._current_color

    @current_color.setter
    def current_color(self, current_color: Color) -> None:
        self._current_color = current_color

    def make_move(self, move: Move) -> None:
        """Make the move and update the state of the from piece."""
        self._board.make_move(move)

    def undo_move(self, move: Move) -> None:
        """Undo a move and restore the state of both the from and to pieces."""
        self._board.undo_move(move)

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        return self._board.get_piece(coordinate)

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        return self._board.set_piece(coordinate, piece)
