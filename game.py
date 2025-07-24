from board import BOARD_SIZE, Board
from enums import Color
from pieces import King, Pawn, Piece, Rook

KING_COL_IDX = 4


class Game:
    """Represents a chess game."""

    def __init__(self, board: Board) -> None:
        self._board = board
        self._white_king_pos = (0, KING_COL_IDX)
        self._black_king_pos = (BOARD_SIZE - 1, KING_COL_IDX)

    def _move_passes_basic_checks(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
    ) -> bool:
        """Return whether the move passes basic legality checks."""
        is_from_in_bounds = self._board.is_in_bounds(from_row_idx, from_col_idx)
        is_to_in_bounds = self._board.is_in_bounds(to_row_idx, to_col_idx)
        if not (is_from_in_bounds and is_to_in_bounds):
            return False

        from_piece = self._board.get_piece(from_row_idx, from_col_idx)
        is_moving_wrong_piece = from_piece is None or from_piece.color != color
        if is_moving_wrong_piece:
            return False

        to_piece = self._board.get_piece(to_row_idx, to_col_idx)
        is_to_same_color = to_piece is not None and to_piece.color == color
        if is_to_same_color:
            return False

        return True

    def move(
        self,
        color: Color,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
    ) -> bool:
        """Return whether the move was made."""
        if not self._move_passes_basic_checks(
            color, from_row_idx, from_col_idx, to_row_idx, to_col_idx
        ):
            return False

        from_piece = self._board.get_piece(from_row_idx, from_col_idx)
        if not from_piece.move_strategy.is_legal_move(
            color,
            from_row_idx,
            from_col_idx,
            to_row_idx,
            to_col_idx,
            self._board,
        ):
            return False

        self._move_piece(from_row_idx, from_col_idx, to_row_idx, to_col_idx, from_piece)

        if from_piece.tracks_first_move:
            from_piece.has_moved = True

        return True

    def _move_piece(
        self,
        from_row_idx: int,
        from_col_idx: int,
        to_row_idx: int,
        to_col_idx: int,
        from_piece: Piece,
    ) -> None:
        """Move a piece. Assuming this is a legal move."""
        self._board.set_piece(from_row_idx, from_col_idx, None)
        self._board.set_piece(to_row_idx, to_col_idx, from_piece)


if __name__ == "__main__":
    from pieces import Pawn

    g = Game()
    g._board._squares[2][1] = Pawn(Color.BLACK)
    print(g.move(Color.WHITE, 1, 0, 2, 0))
    cw = Color.WHITE
    cb = Color.BLACK
    print(g._board)
    breakpoint()
