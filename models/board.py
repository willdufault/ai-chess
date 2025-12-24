from models.coordinate import Coordinate


class Board:
    def __init__(self) -> None:
        self.size = 8

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

    def print(self) -> None:
        # Reverse so (0,0) at bottom left.
        for row_offset in reversed(range(self.size)):
            for col_offset in range(self.size):
                offset = self.size * row_offset + col_offset
                square = 1 << offset

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

    def move(self, from_coordinate: Coordinate, to_coordinate: Coordinate) -> None:
        from_offset = from_coordinate.row_index * self.size + from_coordinate.col_index
        from_square = 1 << from_offset
        to_offset = to_coordinate.row_index * self.size + to_coordinate.col_index
        to_square = 1 << to_offset

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
