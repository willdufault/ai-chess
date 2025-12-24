from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8


class Board:
    def __init__(self) -> None:
        self.size = BOARD_SIZE

        self._white_pawns = 0
        self._white_rooks = 0
        self._white_knights = 0
        self._white_bishops = 0
        self._white_queens = 0

        self._black_pawns = 0
        self._black_rooks = 0
        self._black_knights = 0
        self._black_bishops = 0
        self._black_queens = 0

    def set_up_pieces(self) -> None:
        self._white_pawns = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
        )
        self._white_rooks = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
        )
        self._white_knights = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
        )
        self._white_bishops = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
        )
        self._white_queens = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
        )
        self._white_kings = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
        )

        self._black_pawns = (
            0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_rooks = (
            0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_knights = (
            0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_bishops = (
            0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_queens = (
            0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_kings = (
            0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )

    def print(self, color: Color) -> None:
        # Flip board based on team.
        if color == Color.WHITE:
            row_indexes = reversed(range(self.size))
            column_indexes = range(self.size)
        else:
            row_indexes = range(self.size)
            # Must be a list to not exhaust the iterator.
            column_indexes = list(reversed(range(self.size)))

        for row_index in row_indexes:
            for column_index in column_indexes:
                square = self._calculate_bitmask(row_index, column_index)

                if (self._white_pawns & square) != 0:
                    print("♙", end=" ")
                elif (self._white_knights & square) != 0:
                    print("♘", end=" ")
                elif (self._white_bishops & square) != 0:
                    print("♗", end=" ")
                elif (self._white_rooks & square) != 0:
                    print("♖", end=" ")
                elif (self._white_queens & square) != 0:
                    print("♕", end=" ")
                elif (self._white_kings & square) != 0:
                    print("♔", end=" ")

                elif (self._black_pawns & square) != 0:
                    print("♟", end=" ")
                elif (self._black_knights & square) != 0:
                    print("♞", end=" ")
                elif (self._black_bishops & square) != 0:
                    print("♝", end=" ")
                elif (self._black_rooks & square) != 0:
                    print("♜", end=" ")
                elif (self._black_queens & square) != 0:
                    print("♛", end=" ")
                elif (self._black_kings & square) != 0:
                    print("♚", end=" ")
                else:
                    print(".", end=" ")
            print()

    def move(self, move: Move) -> None:
        from_square = self._calculate_bitmask(
            move.from_coordinate.row_index, move.from_coordinate.column_index
        )
        to_square = self._calculate_bitmask(
            move.to_coordinate.row_index, move.to_coordinate.column_index
        )

        if self._white_pawns & from_square != 0:
            self._white_pawns ^= from_square
            self._white_pawns |= to_square
        elif self._white_knights & from_square != 0:
            self._white_knights ^= from_square
            self._white_knights |= to_square
        elif self._white_bishops & from_square != 0:
            self._white_bishops ^= from_square
            self._white_bishops |= to_square
        elif self._white_rooks & from_square != 0:
            self._white_rooks ^= from_square
            self._white_rooks |= to_square
        elif self._white_queens & from_square != 0:
            self._white_queens ^= from_square
            self._white_queens |= to_square
        elif self._white_kings & from_square != 0:
            self._white_kings ^= from_square
            self._white_kings |= to_square

        elif self._black_pawns & from_square != 0:
            self._black_pawns ^= from_square
            self._black_pawns |= to_square
        elif self._black_knights & from_square != 0:
            self._black_knights ^= from_square
            self._black_knights |= to_square
        elif self._black_bishops & from_square != 0:
            self._black_bishops ^= from_square
            self._black_bishops |= to_square
        elif self._black_rooks & from_square != 0:
            self._black_rooks ^= from_square
            self._black_rooks |= to_square
        elif self._black_queens & from_square != 0:
            self._black_queens ^= from_square
            self._black_queens |= to_square
        elif self._black_kings & from_square != 0:
            self._black_kings ^= from_square
            self._black_kings |= to_square

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        square = self._calculate_bitmask(coordinate.row_index, coordinate.column_index)
        if self._white_pawns & square != 0:
            return Pawn(Color.WHITE)
        elif self._white_knights & square != 0:
            return Knight(Color.WHITE)
        elif self._white_bishops & square != 0:
            return Bishop(Color.WHITE)
        elif self._white_rooks & square != 0:
            return Rook(Color.WHITE)
        elif self._white_queens & square != 0:
            return Queen(Color.WHITE)
        elif self._white_kings & square != 0:
            return King(Color.WHITE)

        elif self._black_pawns & square != 0:
            return Pawn(Color.BLACK)
        elif self._black_knights & square != 0:
            return Knight(Color.BLACK)
        elif self._black_bishops & square != 0:
            return Bishop(Color.BLACK)
        elif self._black_rooks & square != 0:
            return Rook(Color.BLACK)
        elif self._black_queens & square != 0:
            return Queen(Color.BLACK)
        elif self._black_kings & square != 0:
            return King(Color.BLACK)

        return None

    def _calculate_bitmask(self, row_index: int, column_index: int) -> int:
        offset = row_index * self.size + column_index
        return 1 << offset
