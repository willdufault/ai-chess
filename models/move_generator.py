from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.piece import Piece

_WHITE_PAWN_CAPTURE_LEFT_SHIFT = 7
_WHITE_PAWN_CAPTURE_RIGHT_SHIFT = 9
_BLACK_PAWN_CAPTURE_LEFT_SHIFT = -9
_BLACK_PAWN_CAPTURE_RIGHT_SHIFT = -7
_WHITE_PAWN_UP_ONE_MASK = (
    0b00000000_11111111_11111111_11111111_11111111_11111111_11111111_11111111
)
_WHITE_PAWN_UP_TWO_MASK = (
    0b00000000_00000000_11111111_11111111_11111111_11111111_11111111_11111111
)
_WHITE_PAWN_CAPTURE_LEFT_MASK = (
    0b00000000_11111110_11111110_11111110_11111110_11111110_11111110_11111110
)
_WHITE_PAWN_CAPTURE_RIGHT_MASK = (
    0b00000000_01111111_01111111_01111111_01111111_01111111_01111111_01111111
)
_BLACK_PAWN_DOWN_ONE_MASK = (
    0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_00000000
)
_BLACK_PAWN_DOWN_TWO_MASK = (
    0b11111111_11111111_11111111_11111111_11111111_11111111_00000000_00000000
)
_BLACK_PAWN_CAPTURE_LEFT_MASK = (
    0b11111110_11111110_11111110_11111110_11111110_11111110_11111110_00000000
)
_BLACK_PAWN_CAPTURE_RIGHT_MASK = (
    0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_00000000
)

_KNIGHT_UP_LEFT_SHIFT = 15
_KNIGHT_UP_RIGHT_SHIFT = 17
_KNIGHT_RIGHT_UP_SHIFT = 10
_KNIGHT_RIGHT_DOWN_SHIFT = -6
_KNIGHT_DOWN_RIGHT_SHIFT = -15
_KNIGHT_DOWN_LEFT_SHIFT = -17
_KNIGHT_LEFT_DOWN_SHIFT = -10
_KNIGHT_LEFT_UP_SHIFT = 6
_KNIGHT_UP_LEFT_MASK = (
    0b00000000_00000000_11111110_11111110_11111110_11111110_11111110_11111110
)
_KNIGHT_UP_RIGHT_MASK = (
    0b00000000_00000000_01111111_01111111_01111111_01111111_01111111_01111111
)
_KNIGHT_RIGHT_UP_MASK = (
    0b00000000_00111111_00111111_00111111_00111111_00111111_00111111_00111111
)
_KNIGHT_RIGHT_DOWN_MASK = (
    0b00111111_00111111_00111111_00111111_00111111_00111111_00111111_00000000
)
_KNIGHT_DOWN_RIGHT_MASK = (
    0b01111111_01111111_01111111_01111111_01111111_01111111_00000000_00000000
)
_KNIGHT_DOWN_LEFT_MASK = (
    0b11111110_11111110_11111110_11111110_11111110_11111110_00000000_00000000
)
_KNIGHT_LEFT_DOWN_MASK = (
    0b11111100_11111100_11111100_11111100_11111100_11111100_11111100_00000000
)
_KNIGHT_LEFT_UP_MASK = (
    0b00000000_11111100_11111100_11111100_11111100_11111100_11111100_11111100
)

_DIAGONAL_UP_LEFT_SHIFT = 7
_DIAGONAL_UP_RIGHT_SHIFT = 9
_DIAGONAL_DOWN_RIGHT_SHIFT = -7
_DIAGONAL_DOWN_LEFT_SHIFT = -9
_DIAGONAL_UP_LEFT_MASK = (
    0b00000000_11111110_11111110_11111110_11111110_11111110_11111110_11111110
)
_DIAGONAL_UP_RIGHT_MASK = (
    0b00000000_01111111_01111111_01111111_01111111_01111111_01111111_01111111
)
_DIAGONAL_DOWN_RIGHT_MASK = (
    0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_00000000
)
_DIAGONAL_DOWN_LEFT_MASK = (
    0b11111110_11111110_11111110_11111110_11111110_11111110_11111110_00000000
)
_DIAGONAL_DIRECTIONS = (
    (_DIAGONAL_UP_LEFT_MASK, _DIAGONAL_UP_LEFT_SHIFT),
    (_DIAGONAL_UP_RIGHT_MASK, _DIAGONAL_UP_RIGHT_SHIFT),
    (_DIAGONAL_DOWN_RIGHT_MASK, _DIAGONAL_DOWN_RIGHT_SHIFT),
    (_DIAGONAL_DOWN_LEFT_MASK, _DIAGONAL_DOWN_LEFT_SHIFT),
)

_HORIZONTAL_UP_SHIFT = 8
_HORIZONTAL_RIGHT_SHIFT = 1
_HORIZONTAL_DOWN_SHIFT = -8
_HORIZONTAL_LEFT_SHIFT = -1
_HORIZONTAL_UP_MASK = (
    0b00000000_11111111_11111111_11111111_11111111_11111111_11111111_11111111
)
_HORIZONTAL_RIGHT_MASK = (
    0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_01111111
)
_HORIZONTAL_DOWN_MASK = (
    0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_00000000
)
_HORIZONTAL_LEFT_MASK = (
    0b11111110_11111110_11111110_11111110_11111110_11111110_11111110_11111110
)
_HORIZONTAL_DIRECTIONS = (
    (_HORIZONTAL_UP_MASK, _HORIZONTAL_UP_SHIFT),
    (_HORIZONTAL_RIGHT_MASK, _HORIZONTAL_RIGHT_SHIFT),
    (_HORIZONTAL_DOWN_MASK, _HORIZONTAL_DOWN_SHIFT),
    (_HORIZONTAL_LEFT_MASK, _HORIZONTAL_LEFT_SHIFT),
)


class MoveGenerator:
    @staticmethod
    def _is_pawn_single_move_valid(board: Board, color: Color, from_mask: int) -> bool:
        """Assumes a valid pawn at from_mask."""
        move_mask = (
            _WHITE_PAWN_UP_ONE_MASK
            if color is Color.WHITE
            else _BLACK_PAWN_DOWN_ONE_MASK
        )
        is_move_in_bounds = from_mask & move_mask > 0
        if not is_move_in_bounds:
            return False

        forward_one_mask = (
            from_mask << board.SIZE if color is Color.WHITE else from_mask >> board.SIZE
        )
        if board.is_square_occupied(forward_one_mask):
            return False

        return True

    @staticmethod
    def _is_pawn_double_move_valid(board: Board, color: Color, from_mask: int) -> bool:
        """Assumes a valid pawn at from_mask."""
        move_mask = (
            _WHITE_PAWN_UP_TWO_MASK
            if color is Color.WHITE
            else _BLACK_PAWN_DOWN_TWO_MASK
        )
        is_move_in_bounds = from_mask & move_mask > 0
        if not is_move_in_bounds:
            return False

        forward_one_mask = (
            from_mask << board.SIZE if color is Color.WHITE else from_mask >> board.SIZE
        )
        if board.is_square_occupied(forward_one_mask):
            return False

        forward_two_mask = (
            from_mask << (board.SIZE << 1)
            if color is Color.WHITE
            else from_mask >> (board.SIZE << 1)
        )
        if board.is_square_occupied(forward_two_mask):
            return False

        # TODO
        has_pawn_moved = True
        if has_pawn_moved:
            return False

        return True

    @staticmethod
    def _is_pawn_capture_valid(
        board: Board, color: Color, from_mask: int, is_left: bool
    ) -> bool:
        """Assumes a valid pawn at from_mask."""
        if color is Color.WHITE:
            if is_left:
                move_mask = _WHITE_PAWN_CAPTURE_LEFT_MASK
                move_shift = _WHITE_PAWN_CAPTURE_LEFT_SHIFT
            else:
                move_mask = _WHITE_PAWN_CAPTURE_RIGHT_MASK
                move_shift = _WHITE_PAWN_CAPTURE_RIGHT_SHIFT
        else:
            if is_left:
                move_mask = _BLACK_PAWN_CAPTURE_LEFT_MASK
                move_shift = _BLACK_PAWN_CAPTURE_LEFT_SHIFT
            else:
                move_mask = _BLACK_PAWN_CAPTURE_RIGHT_MASK
                move_shift = _BLACK_PAWN_CAPTURE_RIGHT_SHIFT

        is_move_in_bounds = from_mask & move_mask > 0
        if not is_move_in_bounds:
            return False

        capture_mask = (
            from_mask << move_shift
            if color is Color.WHITE
            else from_mask >> -move_shift
        )
        is_capturing_opposite_color_piece = (
            board.is_black_piece_on_square(capture_mask)
            if color is Color.WHITE
            else board.is_white_piece_on_square(capture_mask)
        )
        if not is_capturing_opposite_color_piece:
            return False

        return True

    @classmethod
    def generate_pawn_moves(cls, board: Board, color: Color) -> list[Move]:
        moves = []
        if color is Color.WHITE:
            pawn_mask = board.white_pawn_mask
        else:
            pawn_mask = board.black_pawn_mask

        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_same_color_pawn = from_mask & pawn_mask > 0
            if not is_same_color_pawn:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)

            if cls._is_pawn_single_move_valid(board, color, from_mask):
                to_mask = (
                    from_mask << board.SIZE
                    if color is Color.WHITE
                    else from_mask >> board.SIZE
                )
                to_coordinate = board.get_coordinate_from_mask(to_mask)
                move = Move(color, from_coordinate, to_coordinate)
                moves.append(move)

            if cls._is_pawn_double_move_valid(board, color, from_mask):
                to_mask = (
                    from_mask << (board.SIZE << 1)
                    if color is Color.WHITE
                    else from_mask >> (board.SIZE << 1)
                )
                to_coordinate = board.get_coordinate_from_mask(to_mask)
                move = Move(color, from_coordinate, to_coordinate)
                moves.append(move)

            if cls._is_pawn_capture_valid(board, color, from_mask, True):
                to_mask = (
                    from_mask << _WHITE_PAWN_CAPTURE_LEFT_MASK
                    if color is Color.WHITE
                    else from_mask >> -_BLACK_PAWN_CAPTURE_LEFT_MASK
                )
                to_coordinate = board.get_coordinate_from_mask(to_mask)
                move = Move(color, from_coordinate, to_coordinate)
                moves.append(move)

            if cls._is_pawn_capture_valid(board, color, from_mask, False):
                to_mask = (
                    from_mask << _WHITE_PAWN_CAPTURE_RIGHT_MASK
                    if color is Color.WHITE
                    else from_mask >> -_BLACK_PAWN_CAPTURE_RIGHT_MASK
                )
                to_coordinate = board.get_coordinate_from_mask(to_mask)
                move = Move(color, from_coordinate, to_coordinate)
                moves.append(move)

        return moves

    @staticmethod
    def generate_knight_moves(board: Board, color: Color) -> list[Move]:
        moves = []
        if color is Color.WHITE:
            knight_mask = board.white_knight_mask
            same_color_mask = board.white_pieces_mask
        else:
            knight_mask = board.black_knight_mask
            same_color_mask = board.black_pieces_mask

        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_same_color_knight = from_mask & knight_mask > 0
            if not is_same_color_knight:
                continue

            to_masks = []
            if from_mask & _KNIGHT_UP_LEFT_MASK > 0:
                to_masks.append(from_mask << _KNIGHT_UP_LEFT_SHIFT)
            if from_mask & _KNIGHT_UP_RIGHT_MASK > 0:
                to_masks.append(from_mask << _KNIGHT_UP_RIGHT_SHIFT)
            if from_mask & _KNIGHT_RIGHT_UP_MASK > 0:
                to_masks.append(from_mask << _KNIGHT_RIGHT_UP_SHIFT)
            if from_mask & _KNIGHT_RIGHT_DOWN_MASK > 0:
                to_masks.append(from_mask >> -_KNIGHT_RIGHT_DOWN_SHIFT)
            if from_mask & _KNIGHT_DOWN_RIGHT_MASK > 0:
                to_masks.append(from_mask >> -_KNIGHT_DOWN_RIGHT_SHIFT)
            if from_mask & _KNIGHT_DOWN_LEFT_MASK > 0:
                to_masks.append(from_mask >> -_KNIGHT_DOWN_LEFT_SHIFT)
            if from_mask & _KNIGHT_LEFT_DOWN_MASK > 0:
                to_masks.append(from_mask >> -_KNIGHT_LEFT_DOWN_SHIFT)
            if from_mask & _KNIGHT_LEFT_UP_MASK > 0:
                to_masks.append(from_mask << _KNIGHT_LEFT_UP_SHIFT)

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for to_mask in to_masks:
                is_attacking_same_color_piece = to_mask & same_color_mask > 0
                if not is_attacking_same_color_piece:
                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(color, from_coordinate, to_coordinate)
                    moves.append(move)
        return moves

    @classmethod
    def generate_bishop_moves(cls, board: Board, color: Color) -> list[Move]:
        bishop_mask = (
            board.white_bishop_mask if color is Color.WHITE else board.black_bishop_mask
        )
        return cls._generate_straight_moves(
            board, color, bishop_mask, _DIAGONAL_DIRECTIONS
        )

    @classmethod
    def generate_rook_moves(cls, board: Board, color: Color) -> list[Move]:
        rook_mask = (
            board.white_rook_mask if color is Color.WHITE else board.black_rook_mask
        )
        return cls._generate_straight_moves(
            board, color, rook_mask, _HORIZONTAL_DIRECTIONS
        )

    @classmethod
    def generate_queen_moves(cls, board: Board, color: Color) -> list[Move]:
        queen_mask = (
            board.white_queen_mask if color is Color.WHITE else board.black_queen_mask
        )
        return cls._generate_straight_moves(
            board, color, queen_mask, _HORIZONTAL_DIRECTIONS + _DIAGONAL_DIRECTIONS
        )

    @staticmethod
    def generate_king_moves(board: Board, color: Color) -> list[Move]:
        moves = []
        if color is Color.WHITE:
            king_mask = board.white_king_mask
            same_color_mask = board.white_pieces_mask
        else:
            king_mask = board.black_king_mask
            same_color_mask = board.black_pieces_mask

        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_same_color_king = from_mask & king_mask
            if not is_same_color_king:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in (
                _HORIZONTAL_DIRECTIONS + _DIAGONAL_DIRECTIONS
            ):
                to_mask = (
                    from_mask << direction_shift
                    if direction_shift > 0
                    else from_mask >> -direction_shift
                )

                can_move_in_direction = to_mask & direction_mask > 0
                is_attacking_same_color_piece = to_mask & same_color_mask > 0
                if can_move_in_direction and not is_attacking_same_color_piece:
                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.WHITE, from_coordinate, to_coordinate)
                    moves.append(move)
        return moves

    @staticmethod
    def list_attacking_(
        board: Board, color: Color, coordinate: Coordinate
    ) -> list[Piece]: ...

    @staticmethod
    def _generate_straight_moves(
        board: Board,
        color: Color,
        piece_mask: int,
        directions: tuple[tuple[int, int], ...],
    ) -> list[Move]:
        moves = []
        if color is Color.WHITE:
            same_color_mask = board.white_pieces_mask
            opposite_color_mask = board.black_pieces_mask
        else:
            same_color_mask = board.black_pieces_mask
            opposite_color_mask = board.white_pieces_mask

        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_same_color_right_piece = from_mask & piece_mask > 0
            if not is_same_color_right_piece:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in directions:
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_same_color_piece = to_mask & same_color_mask > 0
                    if is_attacking_same_color_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(color, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_opposite_color_piece = (
                        to_mask & opposite_color_mask > 0
                    )
                    if is_attacking_opposite_color_piece:
                        break
        return moves
