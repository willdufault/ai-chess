from enums.color import Color
from models.board import Board
from utils.bit_utils import intersects
from utils.board_utils import calculate_mask


class BoardView:
    @staticmethod
    def print(color: Color, board: Board) -> None:
        # Flip board based on team.
        if color == Color.WHITE:
            row_indexes = tuple(reversed(range(board.size)))
            column_indexes = tuple(range(board.size))
        else:
            row_indexes = tuple(range(board.size))
            column_indexes = tuple(reversed(range(board.size)))

        print("  ┌───┬───┬───┬───┬───┬───┬───┬───┐")

        row_count = 0
        for row_index in row_indexes:
            print(row_index, end="")

            for column_index in column_indexes:
                print(f" │ ", end="")

                square_mask = calculate_mask(row_index, column_index)
                if intersects(board._white_pawn_bitboard, square_mask):
                    print(f"♙", end="")
                elif intersects(board._white_knight_bitboard, square_mask):
                    print(f"♘", end="")
                elif intersects(board._white_bishop_bitboard, square_mask):
                    print(f"♗", end="")
                elif intersects(board._white_rook_bitboard, square_mask):
                    print(f"♖", end="")
                elif intersects(board._white_queen_bitboard, square_mask):
                    print(f"♕", end="")
                elif intersects(board._white_king_bitboard, square_mask):
                    print(f"♔", end="")

                elif intersects(board._black_pawn_bitboard, square_mask):
                    print(f"♟", end="")
                elif intersects(board._black_knight_bitboard, square_mask):
                    print(f"♞", end="")
                elif intersects(board._black_bishop_bitboard, square_mask):
                    print(f"♝", end="")
                elif intersects(board._black_rook_bitboard, square_mask):
                    print(f"♜", end="")
                elif intersects(board._black_queen_bitboard, square_mask):
                    print(f"♛", end="")
                elif intersects(board._black_king_bitboard, square_mask):
                    print(f"♚", end="")
                else:
                    print(f" ", end="")

            print(" │", end="")

            row_count += 1
            if row_count < board.size:
                print("\n  ├───┼───┼───┼───┼───┼───┼───┼───┤")

        print("\n  └───┴───┴───┴───┴───┴───┴───┴───┘")
        print("    " + "   ".join(map(str, column_indexes)))
