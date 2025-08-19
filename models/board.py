from enums.color import Color
from models.coordinate import Coordinate
from models.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8
KING_COLUMN_INDEX = 4
WHITE_PAWN_ROW_INDEX = 1
BLACK_PAWN_ROW_INDEX = BOARD_SIZE - 2


# TODO: when generating legal moves, cache per board, make sure hash is efficient
class Board:
    """Represents a chessboard."""

    def __init__(self) -> None:
        self._squares: list[list[Piece | None]] = [
            [None] * BOARD_SIZE for _ in range(BOARD_SIZE)
        ]
        self._white_king_coordinate = Coordinate(-1, -1)
        self._black_king_coordinate = Coordinate(-1, -1)
        # self._can_white_short_castle = True
        # self._can_white_long_castle = True
        # self._can_black_short_castle = True
        # self._can_black_long_castle = True

    @staticmethod
    def is_index_in_bounds(index: int) -> bool:
        """Return whether the index is in bounds."""
        return 0 <= index < BOARD_SIZE

    @staticmethod
    def is_coordinate_in_bounds(coordinate: Coordinate) -> bool:
        """Return whether the coordinate is in bounds."""
        return Board.is_index_in_bounds(
            coordinate.row_index
        ) and Board.is_index_in_bounds(coordinate.column_index)

    @staticmethod
    def get_last_row_index(color: Color) -> int:
        """Return the index of the last row for the color."""
        return BOARD_SIZE - 1 if color is Color.WHITE else 0

    def set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_type_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for column_index, piece_type in enumerate(piece_type_order):
            white_piece_coordinate = Coordinate(0, column_index)
            black_piece_coordinate = Coordinate(BOARD_SIZE - 1, column_index)
            white_pawn_coordinate = Coordinate(WHITE_PAWN_ROW_INDEX, column_index)
            black_pawn_coordinate = Coordinate(BLACK_PAWN_ROW_INDEX, column_index)
            self.set_piece(white_piece_coordinate, piece_type(Color.WHITE))
            self.set_piece(black_piece_coordinate, piece_type(Color.BLACK))
            self.set_piece(white_pawn_coordinate, Pawn(Color.WHITE))
            self.set_piece(black_pawn_coordinate, Pawn(Color.BLACK))
        self._set_king_coordinate(Color.WHITE, Coordinate(0, KING_COLUMN_INDEX))
        self._set_king_coordinate(
            Color.BLACK, Coordinate(BOARD_SIZE - 1, KING_COLUMN_INDEX)
        )

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        return self._squares[coordinate.row_index][coordinate.column_index]

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        self._squares[coordinate.row_index][coordinate.column_index] = piece
        if isinstance(piece, King):
            self._set_king_coordinate(piece.color, coordinate)

    def get_king_coordinate(self, color: Color) -> Coordinate:
        """Get the coordinate of the king of the color."""
        return (
            self._white_king_coordinate
            if color is Color.WHITE
            else self._black_king_coordinate
        )

    def is_occupied(self, coordinate: Coordinate) -> bool:
        """Return whether the coordinate has a piece on it."""
        return self._squares[coordinate.row_index][coordinate.column_index] is not None

    def get_coordinates_between(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates in a straight line between the from and
        to coordinates."""
        row_difference = to_coordinate.row_index - from_coordinate.row_index
        column_difference = to_coordinate.column_index - from_coordinate.column_index
        step_count = max(abs(row_difference), abs(column_difference))
        are_no_squares_between = step_count < 2
        if are_no_squares_between:
            return []

        row_delta = row_difference // step_count
        column_delta = column_difference // step_count
        between_coordinates = []
        for step in range(1, step_count):
            current_coordinate = Coordinate(
                from_coordinate.row_index + step * row_delta,
                from_coordinate.column_index + step * column_delta,
            )
            between_coordinates.append(current_coordinate)
        return between_coordinates

    def is_blocked(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> bool:
        """Return whether there is a piece between the from and to coordinates
        along a straight line."""
        between_coordinates = self.get_coordinates_between(
            from_coordinate, to_coordinate
        )
        for between_coordinate in between_coordinates:
            if self.is_occupied(between_coordinate):
                return True
        return False

    def _set_king_coordinate(self, color: Color, coordinate: Coordinate) -> None:
        """Set the coordinate of the king of the color."""
        if color is Color.WHITE:
            self._white_king_coordinate = coordinate
        else:
            self._black_king_coordinate = coordinate
