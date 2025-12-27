from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from utils.board_utils import calculate_mask


class Rules:
    @classmethod
    def is_in_check(cls, color: Color, board: Board) -> bool:
        king_square = (
            board._white_king_squares
            if color is Color.WHITE
            else board._black_king_squares
        )
        return board.calculate_attacker_squares(color.opposite, king_square) != 0

    @classmethod
    def is_in_checkmate(cls, color: Color, board: Board) -> bool:
        if not cls.is_in_check(color, board):
            return False

        king_square = (
            board._white_king_squares
            if color == Color.WHITE
            else board._black_king_squares
        )
        # TODO: replace with shift
        king_row_index, king_column_index = divmod(king_square.bit_length() - 1, board.size)

        # 1. escape squares
        escape_squares = board.calculate_escape_squares(king_square)
        for escape_row_index in range(board.size):
            for escape_column_index in range(board.size):
                escape_square = calculate_mask(escape_row_index, escape_column_index)
                if escape_square & escape_squares != 0:
                    c1 = Coordinate(king_row_index, king_column_index)
                    c2 = Coordinate(escape_row_index, escape_column_index)
                    p1 = board.get_piece_from_square(king_square)
                    p2 = board.get_piece_from_square(escape_square)
                    m = Move(c1, c2, p1, p2, color)
                    board.move(m)
                    is_in_check = cls.is_in_check(color, board)
                    board.undo_move(m)
                    if not is_in_check:
                        return False

        # 2. capture attacker w/out check
        attacker_squares = board.calculate_attacker_squares(color.opposite, king_square)
        for attacker_row_index in range(board.size):
            for attacker_column_index in range(board.size):
                attacker_square = calculate_mask(attacker_row_index, attacker_column_index)
                # TODO add helper for this to return gen for squares
                if attacker_square & attacker_squares != 0:
                    # defender = capture attacker
                    defender_squares = board.calculate_attacker_squares(color, attacker_square)
                    for defender_row_index in range(board.size):
                        for defender_column_index in range(board.size):
                            defender_square = calculate_mask(defender_row_index, defender_column_index)
                            if defender_square & defender_squares != 0:
                                c1 = Coordinate(defender_row_index, defender_column_index)
                                c2 = Coordinate(attacker_row_index, attacker_column_index)
                                p1 = board.get_piece_from_square(defender_square)
                                p2 = board.get_piece_from_square(attacker_square)
                                m = Move(c1, c2, p1, p2, color)
                                board.move(m)
                                is_in_check = cls.is_in_check(color, board)
                                board.undo_move(m)
                                if not is_in_check:
                                    return False

        # 3. can't block
        attacker_squares = board.calculate_attacker_squares(color.opposite, king_square)
        is_impossible_to_block = attacker_squares.bit_count() > 1
        if is_impossible_to_block:
            return True

        # 4. block w/out check
        for attacker_row_index in range(board.size):
            for attacker_column_index in range(board.size):
                attacker_square = calculate_mask(attacker_row_index, attacker_column_index)
                # TODO add helper for this to return gen for squares
                if attacker_square & attacker_squares != 0:
                    intermediate_squares = board.calculate_intermediate_squares(attacker_square, king_square)
                    for inter_row_index in range(board.size):
                        for inter_column_index in range(board.size):
                            inter_square = calculate_mask(inter_row_index, inter_column_index)
                            if inter_square & intermediate_squares != 0:
                                # found intermediate square
                                blocker_squares = board.calculate_blocker_squares(color, inter_square)
                                for blk_row_idx in range(board.size):
                                    for blk_col_idx in range(board.size):
                                        blk_sq = calculate_mask(blk_row_idx, blk_col_idx)
                                        if blk_sq & blocker_squares != 0:
                                            # found blocker square
                                            c1 = Coordinate(blk_row_idx, blk_col_idx)
                                            c2 = Coordinate(inter_row_index, inter_column_index)
                                            p1 = board.get_piece_from_square(blk_sq)
                                            p2 = board.get_piece_from_square(inter_square)
                                            m = Move(c1, c2, p1, p2, color)
                                            board.move(m)
                                            is_in_check = cls.is_in_check(color, board)
                                            board.undo_move(m)
                                            if not is_in_check:
                                                return False
        
        return True

    # TODO: clean up
    @classmethod
    def is_in_checkmate1(cls, color: Color, board: Board) -> bool:
        if not cls.is_in_check(color, board):
            return False

        king_square = (
            board._white_king_squares
            if color == Color.WHITE
            else board._black_king_squares
        )
        king_row_index, king_column_index = divmod(king_square.bit_length(), board.size)

        attacker_squares = board.calculate_attacker_squares(color.opposite, king_square)
        is_impossible_to_block = attacker_squares.bit_count() > 1
        if is_impossible_to_block:
            return True

        # TODO: ADD CHECK HERE IF KING CAN ESCAPE, THEN CHECK CHECK
        escape_squares = board.calculate_escape_squares(king_square)
        for escape_row_index in range(board.size):
            for escape_column_index in range(board.size):
                escape_square = calculate_mask(escape_row_index, escape_column_index)
                if escape_square & escape_squares != 0:
                    from_coordinate = Coordinate(king_row_index, king_column_index)
                    to_coordinate = Coordinate(escape_row_index, escape_column_index)
                    from_piece = board.get_piece_from_square(king_square)
                    to_piece = board.get_piece_from_square(escape_square)
                    move = Move(
                        from_coordinate,
                        to_coordinate,
                        from_piece,
                        to_piece,
                        color,
                    )
                    board.move(move)
                    is_in_check = cls.is_in_check(color, board)
                    board.undo_move(move)

                    if not is_in_check:
                        return False

        for attacker_shift in range(board.size**2):
            attacker_square = 1 << attacker_shift
            if attacker_squares & attacker_square != 0:
                intermediate_squares = board.calculate_intermediate_squares(
                    king_square, attacker_square
                )
                candidate_squares = intermediate_squares | attacker_square
                # TODO: change to range(64) shift?
                for candidate_row_index in range(board.size):
                    for candidate_column_index in range(board.size):
                        candidate_square = calculate_mask(
                            candidate_row_index, candidate_column_index
                        )
                        if candidate_square & candidate_squares != 0:
                            defender_squares = board.calculate_attacker_squares(
                                color, candidate_square
                            )
                            # TODO: will be slow, too much overhead
                            for defender_row_index in range(board.size):
                                for defender_column_index in range(board.size):
                                    defender_square = calculate_mask(
                                        defender_row_index, defender_column_index
                                    )
                                    if defender_square & defender_squares != 0:
                                        from_coordinate = Coordinate(
                                            defender_row_index, defender_column_index
                                        )
                                        to_coordinate = Coordinate(
                                            candidate_row_index, candidate_column_index
                                        )
                                        from_piece = board.get_piece_from_square(
                                            defender_square
                                        )
                                        to_piece = board.get_piece_from_square(
                                            candidate_square
                                        )
                                        move = Move(
                                            from_coordinate,
                                            to_coordinate,
                                            from_piece,
                                            to_piece,
                                            color,
                                        )
                                        board.move(move)
                                        is_in_check = cls.is_in_check(color, board)
                                        board.undo_move(move)

                                        if not is_in_check:
                                            return False

        return True
