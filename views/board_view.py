from enums.color import Color

# TODO: should not interact directly with model
from models.board import Board
from models.coordinate import Coordinate
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook

_PIECE_TO_SYMBOL = {
    Pawn(Color.WHITE): "♙",
    Knight(Color.WHITE): "♘",
    Bishop(Color.WHITE): "♗",
    Rook(Color.WHITE): "♖",
    Queen(Color.WHITE): "♕",
    King(Color.WHITE): "♔",
    Pawn(Color.BLACK): "♟",
    Knight(Color.BLACK): "♞",
    Bishop(Color.BLACK): "♝",
    Rook(Color.BLACK): "♜",
    Queen(Color.BLACK): "♛",
    King(Color.BLACK): "♚",
}


class BoardView:
    @staticmethod
    def draw(board: Board, color: Color) -> None:
        if color is Color.WHITE:
            row_indexes = tuple(reversed(range(board.SIZE)))
            column_indexes = tuple(range(board.SIZE))
        else:
            row_indexes = tuple(range(board.SIZE))
            column_indexes = tuple(reversed(range(board.SIZE)))

        for row_index in row_indexes:
            for column_index in column_indexes:
                coordinate = Coordinate(row_index, column_index)
                piece = board.get_piece(coordinate)
                symbol = "." if piece is None else _PIECE_TO_SYMBOL[piece]
                print(symbol, end=" ")
            print()
