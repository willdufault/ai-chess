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

    def _set_up_pieces(self) -> None:
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
                pass
            print()


if __name__ == "__main__":
    b = Board()
    b._set_up_pieces()
    b.print()
