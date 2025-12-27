from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from utils.board_utils import calculate_mask, enumerate_mask


class Rules:
    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        king_square = (
            board._white_king_bitboard
            if color is Color.WHITE
            else board._black_king_bitboard
        )
        return board.calculate_attacker_squares_mask(king_square, color.opposite) != 0

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
        escape_squares_mask = board.calculate_escape_squares_mask(
            king_square_mask, color
        )
        for escape_square_mask in enumerate_mask(escape_squares_mask):
            if not cls._is_in_check_after_move(
                king_square_mask, escape_square_mask, color, board
            ):
                return False

        # Multiple attackers.
        attacker_squares_mask = board.calculate_attacker_squares_mask(
            king_square_mask, color.opposite
        )
        is_impossible_to_block = attacker_squares_mask.bit_count() > 1
        if is_impossible_to_block:
            return True

        # Capture attacker.
        for attacker_square_mask in enumerate_mask(attacker_squares_mask):
            defender_squares_mask = board.calculate_attacker_squares_mask(
                attacker_square_mask, color
            )
            for defender_square_mask in enumerate_mask(defender_squares_mask):
                if not cls._is_in_check_after_move(
                    defender_square_mask, attacker_square_mask, color, board
                ):
                    return False

        # Block attack.
        for attacker_square_mask in enumerate_mask(attacker_squares_mask):
            intermediate_squares_mask = board.calculate_intermediate_squares_mask(
                attacker_square_mask, king_square_mask
            )
            for intermediate_square_mask in enumerate_mask(intermediate_squares_mask):
                blocker_squares_mask = board.calculate_blocker_squares(
                    intermediate_square_mask, color
                )
                for blocker_square_mask in enumerate_mask(blocker_squares_mask):
                    if not cls._is_in_check_after_move(
                        blocker_square_mask, intermediate_square_mask, color, board
                    ):
                        return False

        return True

    @classmethod
    def is_in_checkmate2(cls, color: Color, board: Board) -> bool:
        if not cls.is_in_check(color, board):
            return False

        king_square = (
            board._white_king_bitboard
            if color == Color.WHITE
            else board._black_king_bitboard
        )
        # TODO: replace with shift
        king_row_index, king_column_index = divmod(
            king_square.bit_length() - 1, board.size
        )

        # TODO: ESCAPE SQUARES CAN HAVE ENEMY PIECES
        # 1. escape squares
        escape_squares = board.calculate_escape_squares_mask(king_square, color)
        for escape_row_index in range(board.size):
            for escape_column_index in range(board.size):
                escape_square = calculate_mask(escape_row_index, escape_column_index)
                if escape_square & escape_squares != 0:
                    c1 = Coordinate(king_row_index, king_column_index)
                    c2 = Coordinate(escape_row_index, escape_column_index)
                    p1 = board.get_piece(square_mask=king_square)
                    p2 = board.get_piece(square_mask=escape_square)
                    m = Move.from_coordinates(c1, c2, p1, p2, color)
                    board.make_move(m)
                    is_in_check = cls.is_in_check(color, board)
                    board.undo_move(m)
                    if not is_in_check:
                        return False

        # 2. capture attacker w/out check
        attacker_squares = board.calculate_attacker_squares_mask(
            king_square, color.opposite
        )
        for attacker_row_index in range(board.size):
            for attacker_column_index in range(board.size):
                attacker_square = calculate_mask(
                    attacker_row_index, attacker_column_index
                )
                # TODO add helper for this to return gen for squares
                if attacker_square & attacker_squares != 0:
                    # defender = capture attacker
                    defender_squares = board.calculate_attacker_squares_mask(
                        attacker_square, color
                    )
                    for defender_row_index in range(board.size):
                        for defender_column_index in range(board.size):
                            defender_square = calculate_mask(
                                defender_row_index, defender_column_index
                            )
                            if defender_square & defender_squares != 0:
                                c1 = Coordinate(
                                    defender_row_index, defender_column_index
                                )
                                c2 = Coordinate(
                                    attacker_row_index, attacker_column_index
                                )
                                p1 = board.get_piece(square_mask=defender_square)
                                p2 = board.get_piece(square_mask=attacker_square)
                                m = Move.from_coordinates(c1, c2, p1, p2, color)
                                board.make_move(m)
                                is_in_check = cls.is_in_check(color, board)
                                board.undo_move(m)
                                if not is_in_check:
                                    return False

        # 3. can't block
        attacker_squares = board.calculate_attacker_squares_mask(
            king_square, color.opposite
        )
        is_impossible_to_block = attacker_squares.bit_count() > 1
        if is_impossible_to_block:
            return True

        # 4. block w/out check
        for attacker_row_index in range(board.size):
            for attacker_column_index in range(board.size):
                attacker_square = calculate_mask(
                    attacker_row_index, attacker_column_index
                )
                # TODO add helper for this to return gen for squares
                if attacker_square & attacker_squares != 0:
                    intermediate_squares = board.calculate_intermediate_squares_mask(
                        attacker_square, king_square
                    )
                    for inter_row_index in range(board.size):
                        for inter_column_index in range(board.size):
                            inter_square = calculate_mask(
                                inter_row_index, inter_column_index
                            )
                            if inter_square & intermediate_squares != 0:
                                # found intermediate square
                                blocker_squares = board.calculate_blocker_squares(
                                    inter_square, color
                                )
                                for blk_row_idx in range(board.size):
                                    for blk_col_idx in range(board.size):
                                        blk_sq = calculate_mask(
                                            blk_row_idx, blk_col_idx
                                        )
                                        if blk_sq & blocker_squares != 0:
                                            # found blocker square
                                            c1 = Coordinate(blk_row_idx, blk_col_idx)
                                            c2 = Coordinate(
                                                inter_row_index, inter_column_index
                                            )
                                            p1 = board.get_piece(square_mask=blk_sq)
                                            p2 = board.get_piece(
                                                square_mask=inter_square
                                            )
                                            m = Move.from_coordinates(
                                                c1, c2, p1, p2, color
                                            )
                                            board.make_move(m)
                                            is_in_check = cls.is_in_check(color, board)
                                            board.undo_move(m)
                                            if not is_in_check:
                                                return False

        return True

    @classmethod
    def _is_in_check_after_move(
        cls, from_square_mask: int, to_square_mask: int, color: Color, board: Board
    ) -> bool:
        """Return whether the color is in check after the move."""
        from_piece = board.get_piece(square_mask=from_square_mask)
        to_piece = board.get_piece(square_mask=to_square_mask)
        move = Move(from_square_mask, to_square_mask, from_piece, to_piece, color)
        board.make_move(move)
        is_in_check = cls.is_in_check(color, board)
        board.undo_move(move)
        return is_in_check
