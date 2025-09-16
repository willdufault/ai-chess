from enums.color import Color
from enums.piece import Piece

# TODO: should not interact directly with model
from models.board import Board
from models.coordinate import Coordinate

_PIECE_TO_SYMBOL = {
    Piece.WHITE_PAWN: "♙",
    Piece.WHITE_KNIGHT: "♘",
    Piece.WHITE_BISHOP: "♗",
    Piece.WHITE_ROOK: "♖",
    Piece.WHITE_QUEEN: "♕",
    Piece.WHITE_KING: "♔",
    Piece.BLACK_PAWN: "♟",
    Piece.BLACK_KNIGHT: "♞",
    Piece.BLACK_BISHOP: "♝",
    Piece.BLACK_ROOK: "♜",
    Piece.BLACK_QUEEN: "♛",
    Piece.BLACK_KING: "♚",
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
