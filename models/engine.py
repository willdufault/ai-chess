from constants.board_constants import BOARD_LEN
from enums.color import Color
from models.board import Board
from models.piece import Bishop, King, Knight, Pawn, Queen, Rook
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

_POSITIONAL_SCORE_WEIGHT = 1 / 50


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
        material_score += Pawn.VALUE * board._white_pawn_bitboard.bit_count()
        material_score += Knight.VALUE * board._white_knight_bitboard.bit_count()
        material_score += Bishop.VALUE * board._white_bishop_bitboard.bit_count()
        material_score += Rook.VALUE * board._white_rook_bitboard.bit_count()
        material_score += Queen.VALUE * board._white_queen_bitboard.bit_count()
        material_score += King.VALUE * board._white_king_bitboard.bit_count()

        material_score -= Pawn.VALUE * board._black_pawn_bitboard.bit_count()
        material_score -= Knight.VALUE * board._black_knight_bitboard.bit_count()
        material_score -= Bishop.VALUE * board._black_bishop_bitboard.bit_count()
        material_score -= Rook.VALUE * board._black_rook_bitboard.bit_count()
        material_score -= Queen.VALUE * board._black_queen_bitboard.bit_count()
        material_score -= King.VALUE * board._black_king_bitboard.bit_count()
        return material_score

    @classmethod
    def _get_positional_score(cls, board: Board) -> int:
        """Return the sum of the placement scores of all white pieces minus the
        sum of the placement scores of all black pieces."""
        positional_score = 0
        is_in_endgame = cls._is_in_endgame(board)

        positional_score += cls._get_piece_placement_score(
            board._white_pawn_bitboard, Color.WHITE, _PLACEMENT_SCORES_PAWN
        )
        positional_score += cls._get_piece_placement_score(
            board._white_knight_bitboard, Color.WHITE, _PLACEMENT_SCORES_KNIGHT
        )
        positional_score += cls._get_piece_placement_score(
            board._white_bishop_bitboard, Color.WHITE, _PLACEMENT_SCORES_BISHOP
        )
        positional_score += cls._get_piece_placement_score(
            board._white_rook_bitboard, Color.WHITE, _PLACEMENT_SCORES_ROOK
        )
        positional_score += cls._get_piece_placement_score(
            board._white_queen_bitboard, Color.WHITE, _PLACEMENT_SCORES_QUEEN
        )
        positional_score += cls._get_piece_placement_score(
            board._white_king_bitboard,
            Color.WHITE,
            (
                _PLACEMENT_SCORES_KING_ENDGAME
                if is_in_endgame
                else _PLACEMENT_SCORES_KING_MIDDLEGAME
            ),
        )

        positional_score -= cls._get_piece_placement_score(
            board._black_pawn_bitboard, Color.BLACK, _PLACEMENT_SCORES_PAWN
        )
        positional_score -= cls._get_piece_placement_score(
            board._black_knight_bitboard, Color.BLACK, _PLACEMENT_SCORES_KNIGHT
        )
        positional_score -= cls._get_piece_placement_score(
            board._black_bishop_bitboard, Color.BLACK, _PLACEMENT_SCORES_BISHOP
        )
        positional_score -= cls._get_piece_placement_score(
            board._black_rook_bitboard, Color.BLACK, _PLACEMENT_SCORES_ROOK
        )
        positional_score -= cls._get_piece_placement_score(
            board._black_queen_bitboard, Color.BLACK, _PLACEMENT_SCORES_QUEEN
        )
        positional_score -= cls._get_piece_placement_score(
            board._black_king_bitboard,
            Color.BLACK,
            (
                _PLACEMENT_SCORES_KING_ENDGAME
                if is_in_endgame
                else _PLACEMENT_SCORES_KING_MIDDLEGAME
            ),
        )

        return positional_score

    @staticmethod
    def _get_piece_placement_score(
        piece_bitboard: int, color: Color, piece_placement_scores: tuple[int, ...]
    ) -> int:
        placement_score = 0
        for square_mask in enumerate_mask(piece_bitboard):
            square_shift = get_shift(square_mask)
            placement_index = (
                BOARD_LEN - 1 - square_shift if color == Color.WHITE else square_shift
            )
            placement_score += piece_placement_scores[placement_index]
        return placement_score

    @staticmethod
    def _is_in_endgame(board: Board) -> bool:
        """Return whether there are no queens left on the board."""
        return board._white_queen_bitboard == 0 and board._black_queen_bitboard == 0
