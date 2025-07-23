from board import Board
from enums import Color


class Game:
    """Represents a chess game."""

    def __init__(self) -> None:
        self._board = Board()

    def _move_passes_basic_checks(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
    ) -> bool:
        """Return whether the move passes basic legality checks."""
        if not (
            self._board.is_in_bounds(from_row_index, from_column_index)
            and self._board.is_in_bounds(to_row_index, to_column_index)
        ):
            return False

        from_piece = self._board.get_piece(from_row_index, from_column_index)
        if from_piece is None or from_piece.color != color:
            return False

        to_piece = self._board.get_piece(to_row_index, to_column_index)
        if to_piece is not None and to_piece.color == color:
            return False

        return True

    def move(
        self,
        color: Color,
        from_row_index: int,
        from_column_index: int,
        to_row_index: int,
        to_column_index: int,
    ) -> bool:
        """Return whether the move was made."""
        if not self._move_passes_basic_checks(
            color, from_row_index, from_column_index, to_row_index, to_column_index
        ):
            return False

        from_piece = self._board.get_piece(from_row_index, from_column_index)
        if not from_piece.move_strategy.is_legal_move(
            color,
            from_row_index,
            from_column_index,
            to_row_index,
            to_column_index,
            self._board,
        ):
            return False

        self._board.set_piece(from_row_index, from_column_index, None)
        self._board.set_piece(to_row_index, to_column_index, from_piece)
        return True


if __name__ == "__main__":
    from piece import Pawn

    g = Game()

    # TODO: PICK UP HERE
    # testing pawn move strategy, need to figure out import error

    g._board._squares[2][1] = Pawn(Color.BLACK)
    print(g.move(Color.WHITE, 1, 0, 2, 0))
    cw = Color.WHITE
    cb = Color.BLACK
    print(g._board)
    breakpoint()
