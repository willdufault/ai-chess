from enums.color import Color

from ..models.board import BOARD_SIZE, Board
from ..models.coordinate import Coordinate

TOP_BORDER = "  ┌───┬───┬───┬───┬───┬───┬───┬───┐"
MIDDLE_BORDER = "  ├───┼───┼───┼───┼───┼───┼───┼───┤"
BOTTOM_BORDER = "  └───┴───┴───┴───┴───┴───┴───┴───┘"
column_LABELS = "    0   1   2   3   4   5   6   7"


class BoardView:
    """Handles drawing the board."""

    @staticmethod
    def draw(color: Color, board: Board) -> None:
        """Draw the board from the perspective of the color."""
        rows = [TOP_BORDER]
        if color is Color.WHITE:
            row_indexes = tuple(reversed(range(BOARD_SIZE)))
            column_indexes = tuple(range(BOARD_SIZE))
        else:
            row_indexes = tuple(range(BOARD_SIZE))
            column_indexes = tuple(reversed(range(BOARD_SIZE)))

        for row_indes in row_indexes:
            row = BoardView._get_row(row_indes, column_indexes, board)
            rows.append(row)
            if row_indes != row_indexes[-1]:
                rows.append(MIDDLE_BORDER)

        rows.append(BOTTOM_BORDER)
        rows.append(column_LABELS)
        board_str = "\n".join(rows)
        print(board_str)

    @staticmethod
    def _get_row(row_indes: int, column_indexes: tuple[int, ...], board: Board) -> str:
        """Return the string representation of the row."""
        row = [f"{row_indes} │"]
        for column_indes in column_indexes:
            coord = Coordinate(row_indes, column_indes)
            piece = board.get_piece(coord)
            symbol = " " if piece is None else piece.symbol
            row.append(f" {symbol} │")
        row_str = "".join(row)
        return row_str
