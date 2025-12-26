from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

BOARD_SIZE = 8


class Board:
    def __init__(self) -> None:
        self.size = BOARD_SIZE

        self._white_pawn_squares = 0
        self._white_rook_squares = 0
        self._white_knight_squares = 0
        self._white_bishop_squares = 0
        self._white_queen_squares = 0
        self._white_king_square = 0

        self._black_pawn_squares = 0
        self._black_rook_squares = 0
        self._black_knight_squares = 0
        self._black_bishop_squares = 0
        self._black_queen_squares = 0
        self._black_king_square = 0

    def set_up_pieces(self) -> None:
        self._white_pawn_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
        )
        self._white_rook_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
        )
        self._white_knight_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
        )
        self._white_bishop_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
        )
        self._white_queen_squares = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
        )
        self._white_king_square = (
            0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
        )

        self._black_pawn_squares = (
            0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_rook_squares = (
            0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_knight_squares = (
            0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_bishop_squares = (
            0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_queen_squares = (
            0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self._black_king_square = (
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
                square = self._calculate_mask(row_index, column_index)

                if (self._white_pawn_squares & square) != 0:
                    print("♙", end=" ")
                elif (self._white_knight_squares & square) != 0:
                    print("♘", end=" ")
                elif (self._white_bishop_squares & square) != 0:
                    print("♗", end=" ")
                elif (self._white_rook_squares & square) != 0:
                    print("♖", end=" ")
                elif (self._white_queen_squares & square) != 0:
                    print("♕", end=" ")
                elif self._white_king_square == square:
                    print("♔", end=" ")

                elif (self._black_pawn_squares & square) != 0:
                    print("♟", end=" ")
                elif (self._black_knight_squares & square) != 0:
                    print("♞", end=" ")
                elif (self._black_bishop_squares & square) != 0:
                    print("♝", end=" ")
                elif (self._black_rook_squares & square) != 0:
                    print("♜", end=" ")
                elif (self._black_queen_squares & square) != 0:
                    print("♛", end=" ")
                elif self._black_king_square == square:
                    print("♚", end=" ")
                else:
                    print(".", end=" ")
            print()

    def move(self, move: Move) -> None:
        from_square = self._calculate_mask(
            move.from_coordinate.row_index, move.from_coordinate.column_index
        )
        to_square = self._calculate_mask(
            move.to_coordinate.row_index, move.to_coordinate.column_index
        )

        if self._white_pawn_squares & from_square != 0:
            self._white_pawn_squares ^= from_square
            self._white_pawn_squares |= to_square
        elif self._white_knight_squares & from_square != 0:
            self._white_knight_squares ^= from_square
            self._white_knight_squares |= to_square
        elif self._white_bishop_squares & from_square != 0:
            self._white_bishop_squares ^= from_square
            self._white_bishop_squares |= to_square
        elif self._white_rook_squares & from_square != 0:
            self._white_rook_squares ^= from_square
            self._white_rook_squares |= to_square
        elif self._white_queen_squares & from_square != 0:
            self._white_queen_squares ^= from_square
            self._white_queen_squares |= to_square
        elif self._white_king_square == from_square:
            self._white_king_square ^= from_square
            self._white_king_square |= to_square

        elif self._black_pawn_squares & from_square != 0:
            self._black_pawn_squares ^= from_square
            self._black_pawn_squares |= to_square
        elif self._black_knight_squares & from_square != 0:
            self._black_knight_squares ^= from_square
            self._black_knight_squares |= to_square
        elif self._black_bishop_squares & from_square != 0:
            self._black_bishop_squares ^= from_square
            self._black_bishop_squares |= to_square
        elif self._black_rook_squares & from_square != 0:
            self._black_rook_squares ^= from_square
            self._black_rook_squares |= to_square
        elif self._black_queen_squares & from_square != 0:
            self._black_queen_squares ^= from_square
            self._black_queen_squares |= to_square
        elif self._black_king_square == from_square:
            self._black_king_square ^= from_square
            self._black_king_square |= to_square

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        square = self._calculate_mask(coordinate.row_index, coordinate.column_index)
        if self._white_pawn_squares & square != 0:
            return Pawn(Color.WHITE)
        elif self._white_knight_squares & square != 0:
            return Knight(Color.WHITE)
        elif self._white_bishop_squares & square != 0:
            return Bishop(Color.WHITE)
        elif self._white_rook_squares & square != 0:
            return Rook(Color.WHITE)
        elif self._white_queen_squares & square != 0:
            return Queen(Color.WHITE)
        elif self._white_king_square == square:
            return King(Color.WHITE)

        elif self._black_pawn_squares & square != 0:
            return Pawn(Color.BLACK)
        elif self._black_knight_squares & square != 0:
            return Knight(Color.BLACK)
        elif self._black_bishop_squares & square != 0:
            return Bishop(Color.BLACK)
        elif self._black_rook_squares & square != 0:
            return Rook(Color.BLACK)
        elif self._black_queen_squares & square != 0:
            return Queen(Color.BLACK)
        elif self._black_king_square == square:
            return King(Color.BLACK)

        return None

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        mask = self._calculate_mask(coordinate.row_index, coordinate.column_index)

        self._white_pawn_squares &= ~mask
        self._white_knight_squares &= ~mask
        self._white_bishop_squares &= ~mask
        self._white_rook_squares &= ~mask
        self._white_queen_squares &= ~mask
        self._white_king_square &= ~mask

        self._black_pawn_squares &= ~mask
        self._black_knight_squares &= ~mask
        self._black_bishop_squares &= ~mask
        self._black_rook_squares &= ~mask
        self._black_queen_squares &= ~mask
        self._black_king_square &= ~mask

        if piece is None:
            return

        match piece:
            case Pawn():
                if piece.color == Color.WHITE:
                    self._white_pawn_squares |= mask
                else:
                    self._black_pawn_squares |= mask
            case Knight():
                if piece.color == Color.WHITE:
                    self._white_knight_squares |= mask
                else:
                    self._black_knight_squares |= mask
            case Bishop():
                if piece.color == Color.WHITE:
                    self._white_bishop_squares |= mask
                else:
                    self._black_bishop_squares |= mask
            case Rook():
                if piece.color == Color.WHITE:
                    self._white_rook_squares |= mask
                else:
                    self._black_rook_squares |= mask
            case Queen():
                if piece.color == Color.WHITE:
                    self._white_queen_squares |= mask
                else:
                    self._black_queen_squares |= mask
            case King():
                if piece.color == Color.WHITE:
                    self._white_king_square |= mask
                else:
                    self._black_king_square |= mask
            case _:
                raise ValueError(f"Invalid piece type {piece}.")

    def is_occupied(self, square: int) -> bool:
        return (
            self._white_pawn_squares & square != 0
            or self._white_knight_squares & square != 0
            or self._white_bishop_squares & square != 0
            or self._white_rook_squares & square != 0
            or self._white_queen_squares & square != 0
            or self._white_king_square == square
            or self._black_pawn_squares & square != 0
            or self._black_knight_squares & square != 0
            or self._black_bishop_squares & square != 0
            or self._black_rook_squares & square != 0
            or self._black_queen_squares & square != 0
            or self._black_king_square == square
        )

    def _calculate_mask(self, row_index: int, column_index: int) -> int:
        shift = row_index * self.size + column_index
        return 1 << shift
