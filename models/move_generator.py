from enums.color import Color
from models.board import Board
from models.move import Move

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
    def generate_white_pawn_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN - board.SIZE):
            from_mask = 1 << offset
            is_white_pawn = from_mask & board.white_pawn_mask > 0
            if not is_white_pawn:
                continue

            to_mask = from_mask << board.SIZE
            if board.is_square_occupied(to_mask):
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            to_coordinate = board.get_coordinate_from_mask(to_mask)
            move = Move(Color.WHITE, from_coordinate, to_coordinate)
            moves.append(move)
        return moves

    @staticmethod
    def generate_black_pawn_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.SIZE, board.LEN):
            from_mask = 1 << offset
            is_black_pawn = from_mask & board.black_pawn_mask > 0
            if not is_black_pawn:
                continue

            to_mask = from_mask >> board.SIZE
            if board.is_square_occupied(to_mask):
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            to_coordinate = board.get_coordinate_from_mask(to_mask)
            move = Move(Color.WHITE, from_coordinate, to_coordinate)
            moves.append(move)
        return moves

    @staticmethod
    def generate_white_knight_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_white_knight = from_mask & board.white_knight_mask > 0
            if not is_white_knight:
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
                is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                if not is_attacking_white_piece:
                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.WHITE, from_coordinate, to_coordinate)
                    moves.append(move)
        return moves

    @staticmethod
    def generate_black_knight_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_black_knight = from_mask & board.black_knight_mask
            if not is_black_knight:
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
                is_attacking_black_piece = to_mask & board.black_pieces_mask
                if not is_attacking_black_piece:
                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.BLACK, from_coordinate, to_coordinate)
                    moves.append(move)
        return moves

    @staticmethod
    def generate_white_bishop_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_white_bishop = from_mask & board.white_bishop_mask > 0
            if not is_white_bishop:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in _DIAGONAL_DIRECTIONS:
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                    if is_attacking_white_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.WHITE, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_black_piece = to_mask & board.black_pieces_mask > 0
                    if is_attacking_black_piece:
                        break
        return moves

    @staticmethod
    def generate_black_bishop_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_black_bishop = from_mask & board.black_bishop_mask > 0
            if not is_black_bishop:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in _DIAGONAL_DIRECTIONS:
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_black_piece = to_mask & board.black_pieces_mask > 0
                    if is_attacking_black_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.BLACK, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                    if is_attacking_white_piece:
                        break
        return moves

    @staticmethod
    def generate_white_rook_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_white_rook = from_mask & board.white_rook_mask
            if not is_white_rook:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in _HORIZONTAL_DIRECTIONS:
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                    if is_attacking_white_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.WHITE, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_black_piece = to_mask & board.black_pieces_mask > 0
                    if is_attacking_black_piece:
                        break
        return moves

    @staticmethod
    def generate_black_rook_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_black_rook = from_mask & board.black_rook_mask
            if not is_black_rook:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in _HORIZONTAL_DIRECTIONS:
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_black_piece = to_mask & board.black_pieces_mask > 0
                    if is_attacking_black_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.BLACK, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                    if is_attacking_white_piece:
                        break
        return moves

    @staticmethod
    def generate_white_queen_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_white_queen = from_mask & board.white_queen_mask
            if not is_white_queen:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in (
                _HORIZONTAL_DIRECTIONS + _DIAGONAL_DIRECTIONS
            ):
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                    if is_attacking_white_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.WHITE, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_black_piece = to_mask & board.black_pieces_mask > 0
                    if is_attacking_black_piece:
                        break
        return moves

    @staticmethod
    def generate_black_queen_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_black_queen = from_mask & board.black_queen_mask
            if not is_black_queen:
                continue

            from_coordinate = board.get_coordinate_from_mask(from_mask)
            for direction_mask, direction_shift in (
                _HORIZONTAL_DIRECTIONS + _DIAGONAL_DIRECTIONS
            ):
                to_mask = from_mask
                while to_mask & direction_mask > 0:
                    to_mask = (
                        to_mask << direction_shift
                        if direction_shift > 0
                        else to_mask >> -direction_shift
                    )

                    is_attacking_black_piece = to_mask & board.black_pieces_mask > 0
                    if is_attacking_black_piece:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.BLACK, from_coordinate, to_coordinate)
                    moves.append(move)

                    is_attacking_white_piece = to_mask & board.white_pieces_mask > 0
                    if is_attacking_white_piece:
                        break
        return moves

    @staticmethod
    def generate_white_king_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_white_king = from_mask & board.white_king_mask
            if not is_white_king:
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
                if can_move_in_direction:
                    if to_mask & board.white_pieces_mask > 0:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.WHITE, from_coordinate, to_coordinate)
                    moves.append(move)
        return moves

    @staticmethod
    def generate_black_king_moves(board: Board) -> list[Move]:
        moves = []
        for offset in range(board.LEN):
            from_mask = 1 << offset
            is_black_king = from_mask & board.black_king_mask
            if not is_black_king:
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
                if can_move_in_direction:
                    if to_mask & board.black_pieces_mask > 0:
                        break

                    to_coordinate = board.get_coordinate_from_mask(to_mask)
                    move = Move(Color.BLACK, from_coordinate, to_coordinate)
                    moves.append(move)
        return moves
