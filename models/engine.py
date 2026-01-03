from constants.board_constants import BOARD_LEN
from enums.color import Color
from models.board import Board
from models.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.bit_utils import get_shift
from utils.board_utils import enumerate_mask

# Tables from https://www.chessprogramming.org/Simplified_Evaluation_Function.
# fmt: off
_PLACEMENT_SCORES_PAWN = (
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
)
_PLACEMENT_SCORES_KNIGHT = (
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
)
_PLACEMENT_SCORES_BISHOP = (
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
)
_PLACEMENT_SCORES_ROOK = (
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
)
_PLACEMENT_SCORES_QUEEN = (
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
)
_PLACEMENT_SCORES_KING_MIDDLEGAME = (
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
)
_PLACEMENT_SCORES_KING_ENDGAME = (
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
)
# fmt: on

_POSITIONAL_SCORE_WEIGHT = 1 / 40


class Engine:
    @classmethod
    def evaluate(cls, board: Board) -> float:
        """Return a float that represents which color is winning (higher = white,
        lower = black)."""
        material_score = cls._get_material_score(board)
        positional_score = cls._get_positional_score(board)
        return material_score + _POSITIONAL_SCORE_WEIGHT * positional_score

    @staticmethod
    def _get_material_score(board: Board) -> int:
        """Return the sum of the values of all white pieces minus the sum of
        values of all black pieces."""
        material_score = 0
        for square_mask in enumerate_mask(board.get_mask()):
            piece = board._get_piece(square_mask)
            assert piece is not None
            if piece.color == Color.WHITE:
                material_score += piece.VALUE
            else:
                material_score -= piece.VALUE
        return material_score

    @classmethod
    def _get_positional_score(cls, board: Board) -> int:
        """Return the sum of the placement scores of all white pieces minus the
        sum of the placement scores of all black pieces."""
        positional_score = 0
        for square_mask in enumerate_mask(board.get_mask()):
            piece = board._get_piece(square_mask)
            assert piece is not None
            placement_score = cls._calculate_placement_score_endgame(
                piece, square_mask, cls._is_in_endgame(board)
            )
            if piece.color == Color.WHITE:
                positional_score += placement_score
            else:
                positional_score -= placement_score
        return positional_score

    @staticmethod
    def _is_in_endgame(board: Board) -> bool:
        """Return whether there are no queens left on the board."""
        for square_mask in enumerate_mask(board.get_mask()):
            piece = board._get_piece(square_mask)
            assert piece is not None
            if isinstance(piece, Queen):
                return False
        return True

    @staticmethod
    def _calculate_placement_score_endgame(
        piece: Piece, square_mask: int, is_in_endgame: bool
    ) -> int:
        """Return the placement score for the piece during the endgame."""
        square_shift = get_shift(square_mask)
        placement_index = (
            BOARD_LEN - 1 - square_shift if piece.color == Color.WHITE else square_shift
        )
        match piece:
            case Pawn():
                return _PLACEMENT_SCORES_PAWN[placement_index]
            case Knight():
                return _PLACEMENT_SCORES_KNIGHT[placement_index]
            case Bishop():
                return _PLACEMENT_SCORES_BISHOP[placement_index]
            case Rook():
                return _PLACEMENT_SCORES_ROOK[placement_index]
            case Queen():
                return _PLACEMENT_SCORES_QUEEN[placement_index]
            case King():
                return (
                    _PLACEMENT_SCORES_KING_ENDGAME[placement_index]
                    if is_in_endgame
                    else _PLACEMENT_SCORES_KING_MIDDLEGAME[placement_index]
                )
            case _:
                raise ValueError(f"Invalid piece type: {piece}")
