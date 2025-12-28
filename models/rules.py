from enums.color import Color
from models.board import Board
from models.move import Move
from models.move_generator import MoveGenerator
from utils.board_utils import enumerate_mask


class Rules:
    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        king_square = (
            board._white_king_bitboard
            if color is Color.WHITE
            else board._black_king_bitboard
        )
        return (
            MoveGenerator.calculate_attacker_squares_mask(
                king_square, color.opposite, board
            )
            != 0
        )

    @classmethod
    def is_in_checkmate(cls, color: Color, board: Board) -> bool:
        if not cls.is_in_check(color, board):
            return False

        king_square_mask = (
            board._white_king_bitboard
            if color == Color.WHITE
            else board._black_king_bitboard
        )

        # King escapes.
        escape_squares_mask = MoveGenerator.calculate_escape_squares_mask(
            king_square_mask, color, board
        )
        for escape_square_mask in enumerate_mask(escape_squares_mask):
            if not cls._is_in_check_after_move(
                king_square_mask, escape_square_mask, color, board
            ):
                return False

        # Multiple attackers.
        attacker_squares_mask = MoveGenerator.calculate_attacker_squares_mask(
            king_square_mask, color.opposite, board
        )
        is_impossible_to_block = attacker_squares_mask.bit_count() > 1
        if is_impossible_to_block:
            return True

        # Capture attacker.
        for attacker_square_mask in enumerate_mask(attacker_squares_mask):
            defender_squares_mask = MoveGenerator.calculate_attacker_squares_mask(
                attacker_square_mask, color, board
            )
            for defender_square_mask in enumerate_mask(defender_squares_mask):
                if not cls._is_in_check_after_move(
                    defender_square_mask, attacker_square_mask, color, board
                ):
                    return False

        # Block attack.
        for attacker_square_mask in enumerate_mask(attacker_squares_mask):
            intermediate_squares_mask = (
                MoveGenerator.calculate_intermediate_squares_mask(
                    attacker_square_mask, king_square_mask
                )
            )
            for intermediate_square_mask in enumerate_mask(intermediate_squares_mask):
                blocker_squares_mask = MoveGenerator.calculate_blocker_squares(
                    intermediate_square_mask, color, board
                )
                for blocker_square_mask in enumerate_mask(blocker_squares_mask):
                    if not cls._is_in_check_after_move(
                        blocker_square_mask, intermediate_square_mask, color, board
                    ):
                        return False

        return True

    @classmethod
    def _is_in_check_after_move(
        cls, from_square_mask: int, to_square_mask: int, color: Color, board: Board
    ) -> bool:
        """Return whether the color is in check after the move."""
        from_piece = board._get_piece(from_square_mask)
        to_piece = board._get_piece(to_square_mask)
        move = Move(from_square_mask, to_square_mask, from_piece, to_piece, color)
        board.make_move(move)
        is_in_check = cls.is_in_check(color, board)
        board.undo_move(move)
        return is_in_check
