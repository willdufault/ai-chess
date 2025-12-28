from enums.color import Color
from models.board import Board
from utils.bit_utils import intersects
from utils.board_utils import calculate_mask


class BoardView:
    @staticmethod
    def print(color: Color, board: Board) -> None:
        # Flip board based on team.
        if color == Color.WHITE:
            row_indexes = reversed(range(board.size))
            column_indexes = range(board.size)
        else:
            row_indexes = range(board.size)
            # Must be a list to not exhaust the iterator.
            column_indexes = list(reversed(range(board.size)))

        for row_index in row_indexes:
            for column_index in column_indexes:
                square_mask = calculate_mask(row_index, column_index)

                if intersects(board._white_pawn_bitboard, square_mask):
                    print("♙", end=" ")
                elif intersects(board._white_knight_bitboard, square_mask):
                    print("♘", end=" ")
                elif intersects(board._white_bishop_bitboard, square_mask):
                    print("♗", end=" ")
                elif intersects(board._white_rook_bitboard, square_mask):
                    print("♖", end=" ")
                elif intersects(board._white_queen_bitboard, square_mask):
                    print("♕", end=" ")
                elif intersects(board._white_king_bitboard, square_mask):
                    print("♔", end=" ")

                elif intersects(board._black_pawn_bitboard, square_mask):
                    print("♟", end=" ")
                elif intersects(board._black_knight_bitboard, square_mask):
                    print("♞", end=" ")
                elif intersects(board._black_bishop_bitboard, square_mask):
                    print("♝", end=" ")
                elif intersects(board._black_rook_bitboard, square_mask):
                    print("♜", end=" ")
                elif intersects(board._black_queen_bitboard, square_mask):
                    print("♛", end=" ")
                elif intersects(board._black_king_bitboard, square_mask):
                    print("♚", end=" ")
                else:
                    print(".", end=" ")
            print()
