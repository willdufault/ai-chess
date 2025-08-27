from enums.color import Color
from models.board import BOARD_SIZE, Board
from models.coordinate import Coordinate

TOP_BORDER = "  ┌───┬───┬───┬───┬───┬───┬───┬───┐"
MIDDLE_BORDER = "  ├───┼───┼───┼───┼───┼───┼───┼───┤"
BOTTOM_BORDER = "  └───┴───┴───┴───┴───┴───┴───┴───┘"
COLUMN_LABELS = "    0   1   2   3   4   5   6   7"


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

        for row_index in row_indexes:
            row = [f"{row_index} │"]
            for column_index in column_indexes:
                coordinate = Coordinate(row_index, column_index)
                piece = board.get_piece(coordinate)
                symbol = " " if piece is None else piece.symbol
                row.append(f" {symbol} │")
            row_str = "".join(row)
            rows.append(row_str)
            if row_index != row_indexes[-1]:
                rows.append(MIDDLE_BORDER)

        rows.append(BOTTOM_BORDER)
        rows.append(COLUMN_LABELS)
        board_str = "\n".join(rows)
        print(board_str)
