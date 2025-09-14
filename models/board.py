from abc import ABC, abstractmethod
from typing import Any

from constants.board_constants import BOARD_SIZE
from enums.color import Color
from models.coordinate import Coordinate
from models.move import Move
from models.move_strategies import (
    BishopMoveStrategy,
    KingMoveStrategy,
    KnightMoveStrategy,
    PawnMoveStrategy,
    QueenMoveStrategy,
    RookMoveStrategy,
)
from models.pieces import Bishop, FirstMovePiece, King, Knight, Pawn, Piece, Queen, Rook
from utils.board_utils import get_board_index, is_coordinate_in_bounds


class Board(ABC):
    @property
    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def to_key(self) -> tuple[Any, ...]: ...

    @abstractmethod
    def set_up_pieces(self) -> None: ...

    @abstractmethod
    def get_piece(self, coordinate: Coordinate) -> Piece | None: ...

    @abstractmethod
    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None: ...

    @abstractmethod
    def get_king_coordinate(self, color: Color) -> Coordinate: ...

    @abstractmethod
    def is_occupied(self, coordinate: Coordinate) -> bool: ...

    @abstractmethod
    def make_move(self, move: Move) -> None: ...

    @abstractmethod
    def undo_move(self, move: Move) -> None: ...

    @abstractmethod
    def get_coordinates_between(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> list[Coordinate]: ...

    @abstractmethod
    def is_path_blocked(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> bool: ...

    @abstractmethod
    def get_attacker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]: ...

    @abstractmethod
    def get_blocker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]: ...

    @abstractmethod
    def is_king_trapped(self, color: Color) -> bool: ...

    @abstractmethod
    def get_candidate_moves(self, color: Color) -> list[Move]: ...

    @abstractmethod
    def is_attacking(self, color: Color, coordinate: Coordinate) -> bool: ...


class SimpleBoard(Board):
    _KING_COLUMN_INDEX = 4
    _WHITE_PAWN_ROW_INDEX = 1
    _BLACK_PAWN_ROW_INDEX = BOARD_SIZE - 2

    def __init__(self) -> None:
        self._size = BOARD_SIZE
        self._squares: list[Piece | None] = [None] * (self._size * self._size)
        self._white_king_coordinate = Coordinate(-1, -1)
        self._black_king_coordinate = Coordinate(-1, -1)

    @property
    def size(self) -> int:
        return self._size

    def to_key(self) -> tuple[Any, ...]:
        """Return an immutable version of the board state for caching."""
        key = []
        for row_index in range(self._size):
            for column_index in range(self._size):
                coordinate = Coordinate(row_index, column_index)
                if not self.is_occupied(coordinate):
                    key.append("_")
                    continue

                piece = self.get_piece(coordinate)
                assert piece is not None
                key.append(piece.to_key())
        return tuple(key)

    def set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_type_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for column_index, piece_type in enumerate(piece_type_order):
            white_piece_coordinate = Coordinate(0, column_index)
            black_piece_coordinate = Coordinate(self._size - 1, column_index)
            white_pawn_coordinate = Coordinate(self._WHITE_PAWN_ROW_INDEX, column_index)
            black_pawn_coordinate = Coordinate(self._BLACK_PAWN_ROW_INDEX, column_index)
            self.set_piece(white_piece_coordinate, piece_type(Color.WHITE))
            self.set_piece(black_piece_coordinate, piece_type(Color.BLACK))
            self.set_piece(white_pawn_coordinate, Pawn(Color.WHITE))
            self.set_piece(black_pawn_coordinate, Pawn(Color.BLACK))
        self._set_king_coordinate(Color.WHITE, Coordinate(0, self._KING_COLUMN_INDEX))
        self._set_king_coordinate(
            Color.BLACK, Coordinate(self._size - 1, self._KING_COLUMN_INDEX)
        )

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        board_index = get_board_index(coordinate)
        return self._squares[board_index]

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        board_index = get_board_index(coordinate)
        self._squares[board_index] = piece
        if isinstance(piece, King):
            self._set_king_coordinate(piece.color, coordinate)

    def get_king_coordinate(self, color: Color) -> Coordinate:
        """Get the coordinate of the king of the color."""
        return (
            self._white_king_coordinate
            if color is Color.WHITE
            else self._black_king_coordinate
        )

    def is_occupied(self, coordinate: Coordinate) -> bool:
        """Return whether the coordinate has a piece on it."""
        piece = self.get_piece(coordinate)
        return piece is not None

    def make_move(self, move: Move) -> None:
        """Make the move and update the state of the from piece."""
        self.set_piece(move.from_coordinate, None)
        self.set_piece(move.to_coordinate, move.from_piece)
        if isinstance(move.from_piece, FirstMovePiece):
            move.from_piece.has_moved = True

    def undo_move(self, move: Move) -> None:
        """Undo a move and restore the state of both the from and to pieces."""
        self.set_piece(move.from_coordinate, move.from_piece)
        self.set_piece(move.to_coordinate, move.to_piece)
        if isinstance(move.from_piece, FirstMovePiece):
            move.from_piece.has_moved = move.from_piece_has_moved

    def get_coordinates_between(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates in a straight line between the from and
        to coordinates."""
        row_difference = to_coordinate.row_index - from_coordinate.row_index
        column_difference = to_coordinate.column_index - from_coordinate.column_index
        step_count = max(abs(row_difference), abs(column_difference))
        are_no_squares_between = step_count < 2
        if are_no_squares_between:
            return []

        row_delta = row_difference // step_count
        column_delta = column_difference // step_count
        between_coordinates = []
        for step in range(1, step_count):
            current_coordinate = Coordinate(
                from_coordinate.row_index + step * row_delta,
                from_coordinate.column_index + step * column_delta,
            )
            between_coordinates.append(current_coordinate)
        return between_coordinates

    def is_path_blocked(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> bool:
        """Return whether there is a piece between the from and to coordinates
        along a straight line."""
        between_coordinates = self.get_coordinates_between(
            from_coordinate, to_coordinate
        )
        for between_coordinate in between_coordinates:
            if self.is_occupied(between_coordinate):
                return True
        return False

    def get_attacker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color that can
        attack the target coordinate."""
        bishop_attacker_coordinates = BishopMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        rook_attacker_coordinates = RookMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        queen_attacker_coordinates = QueenMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        knight_attacker_coordinates = KnightMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        king_attacker_coordinates = KingMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        pawn_attacker_coordinates = PawnMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        return (
            bishop_attacker_coordinates
            + rook_attacker_coordinates
            + queen_attacker_coordinates
            + knight_attacker_coordinates
            + king_attacker_coordinates
            + pawn_attacker_coordinates
        )

    def get_blocker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return the coordinates of all pieces of the color that can block an
        attack by moving to the empty target coordinate."""
        bishop_attacker_coordinates = BishopMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        rook_attacker_coordinates = RookMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        queen_attacker_coordinates = QueenMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        knight_blocker_coordinates = KnightMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        king_blocker_coordinates = KingMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        pawn_blocker_coordinate = PawnMoveStrategy.get_blocker_coordinate(
            color, target_coordinate, self
        )
        return (
            bishop_attacker_coordinates
            + rook_attacker_coordinates
            + queen_attacker_coordinates
            + knight_blocker_coordinates
            + king_blocker_coordinates
            + pawn_blocker_coordinate
        )

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has any empty escape squares."""
        king_coordinate = self.get_king_coordinate(color)
        potential_escape_coordinates = (
            KingMoveStrategy.get_potential_escape_coordinates(king_coordinate, self)
        )
        for potential_escape_coordinate in potential_escape_coordinates:
            if not self.is_attacking(color.opposite, potential_escape_coordinate):
                return False
        return True

    def get_candidate_moves(self, color: Color) -> list[Move]:
        """Return a list of candidate moves for the color not accounting for
        discovered check."""
        candidate_moves = []
        for row_index in range(self._size):
            for column_index in range(self._size):
                current_coordinate = Coordinate(row_index, column_index)
                if not self.is_occupied(current_coordinate):
                    continue

                current_piece = self.get_piece(current_coordinate)
                assert current_piece is not None
                if current_piece.color != color:
                    continue

                candidate_moves.extend(
                    current_piece.MOVE_STRATEGY.get_candidate_moves(
                        color, current_coordinate, self
                    )
                )
        return candidate_moves

    def is_attacking(self, color: Color, coordinate: Coordinate) -> bool:
        """Return whether the color is attacking the coordinate."""
        if not is_coordinate_in_bounds(coordinate):
            return False
        return len(self.get_attacker_coordinates(color, coordinate)) > 0

    def _set_king_coordinate(self, color: Color, coordinate: Coordinate) -> None:
        """Set the coordinate of the king of the color."""
        if color is Color.WHITE:
            self._white_king_coordinate = coordinate
        else:
            self._black_king_coordinate = coordinate


class BitBoard(Board):
    _WHITE_PAWNS_STARTING_POSITION = 65280
    _WHITE_KNIGHTS_STARTING_POSITION = 66
    _WHITE_BISHOPS_STARTING_POSITION = 36
    _WHITE_ROOKS_STARTING_POSITION = 129
    _WHITE_QUEENS_STARTING_POSITION = 8
    _WHITE_KINGS_STARTING_POSITION = 16

    _BLACK_PAWNS_STARTING_POSITION = 71776119061217280
    _BLACK_KNIGHTS_STARTING_POSITION = 4755801206503243776
    _BLACK_BISHOPS_STARTING_POSITION = 2594073385365405696
    _BLACK_ROOKS_STARTING_POSITION = 9295429630892703744
    _BLACK_QUEENS_STARTING_POSITION = 576460752303423488
    _BLACK_KINGS_STARTING_POSITION = 1152921504606846976

    _WHITE_KING_STARTING_OFFSET = 4
    _BLACK_KING_STARTING_OFFSET = 60

    def __init__(self) -> None:
        self._size = BOARD_SIZE

        self._white_pawns_not_moved_position = 0
        self._white_pawns_moved_position = 0
        self._white_knights_position = 0
        self._white_bishops_position = 0
        self._white_rooks_not_moved_position = 0
        self._white_rooks_moved_position = 0
        self._white_queens_position = 0
        self._white_kings_not_moved_position = 0
        self._white_kings_moved_position = 0

        self._black_pawns_not_moved_position = 0
        self._black_pawns_moved_position = 0
        self._black_knights_position = 0
        self._black_bishops_position = 0
        self._black_rooks_not_moved_position = 0
        self._black_rooks_moved_position = 0
        self._black_queens_position = 0
        self._black_kings_not_moved_position = 0
        self._black_kings_moved_position = 0

        self._white_king_offset = -1
        self._black_king_offset = -1

    @property
    def size(self) -> int:
        return self._size

    def to_key(self) -> tuple[Any, ...]:
        """Return an immutable version of the board state for caching."""
        key = (
            self._white_pawns_not_moved_position,
            self._white_pawns_moved_position,
            self._white_knights_position,
            self._white_bishops_position,
            self._white_rooks_not_moved_position,
            self._white_rooks_moved_position,
            self._white_queens_position,
            self._white_kings_not_moved_position,
            self._white_kings_moved_position,
            self._black_pawns_not_moved_position,
            self._black_pawns_moved_position,
            self._black_knights_position,
            self._black_bishops_position,
            self._black_rooks_not_moved_position,
            self._black_rooks_moved_position,
            self._black_queens_position,
            self._black_kings_not_moved_position,
            self._black_kings_moved_position,
        )
        return key

    def set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        self._white_pawns_not_moved_position = self._WHITE_PAWNS_STARTING_POSITION
        self._white_knights_position = self._WHITE_KNIGHTS_STARTING_POSITION
        self._white_bishops_position = self._WHITE_BISHOPS_STARTING_POSITION
        self._white_rooks_not_moved_position = self._WHITE_ROOKS_STARTING_POSITION
        self._white_queens_position = self._WHITE_QUEENS_STARTING_POSITION
        self._white_kings_not_moved_position = self._WHITE_KINGS_STARTING_POSITION

        self._black_pawns_not_moved_position = self._BLACK_PAWNS_STARTING_POSITION
        self._black_knights_position = self._BLACK_KNIGHTS_STARTING_POSITION
        self._black_bishops_position = self._BLACK_BISHOPS_STARTING_POSITION
        self._black_rooks_not_moved_position = self._BLACK_ROOKS_STARTING_POSITION
        self._black_queens_position = self._BLACK_QUEENS_STARTING_POSITION
        self._black_kings_not_moved_position = self._BLACK_KINGS_STARTING_POSITION

        self._white_king_offset = self._WHITE_KING_STARTING_OFFSET
        self._black_king_offset = self._BLACK_KING_STARTING_OFFSET

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        board_offset = self._get_board_offset(coordinate)
        board_mask = 1 << board_offset
        # TODO: cleaner way of doing this? DRY?
        if (board_mask & self._white_pawns_not_moved_position) > 0:
            return Pawn(Color.WHITE)
        if (board_mask & self._white_pawns_moved_position) > 0:
            return Pawn(Color.WHITE, True)
        if (board_mask & self._white_knights_position) > 0:
            return Knight(Color.WHITE)
        if (board_mask & self._white_bishops_position) > 0:
            return Bishop(Color.WHITE)
        if (board_mask & self._white_rooks_not_moved_position) > 0:
            return Rook(Color.WHITE)
        if (board_mask & self._white_rooks_moved_position) > 0:
            return Rook(Color.WHITE, True)
        if (board_mask & self._white_queens_position) > 0:
            return Queen(Color.WHITE)
        if (board_mask & self._white_kings_not_moved_position) > 0:
            return King(Color.WHITE)
        if (board_mask & self._white_kings_moved_position) > 0:
            return King(Color.WHITE, True)

        if (board_mask & self._black_pawns_not_moved_position) > 0:
            return Pawn(Color.BLACK)
        if (board_mask & self._black_pawns_moved_position) > 0:
            return Pawn(Color.BLACK, True)
        if (board_mask & self._black_knights_position) > 0:
            return Knight(Color.BLACK)
        if (board_mask & self._black_bishops_position) > 0:
            return Bishop(Color.BLACK)
        if (board_mask & self._black_rooks_not_moved_position) > 0:
            return Rook(Color.BLACK)
        if (board_mask & self._black_rooks_moved_position) > 0:
            return Rook(Color.BLACK, True)
        if (board_mask & self._black_queens_position) > 0:
            return Queen(Color.BLACK)
        if (board_mask & self._black_kings_not_moved_position) > 0:
            return King(Color.BLACK)
        if (board_mask & self._black_kings_moved_position) > 0:
            return King(Color.BLACK, True)

        return None

    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        board_offset = self._get_board_offset(coordinate)
        board_mask = 1 << board_offset
        self._clear_position_bit(board_mask)
        if piece is None:
            return
        self._set_position_bit(piece, board_mask)
        if isinstance(piece, King):
            self._set_king_offset(piece.color, coordinate)

    def get_king_coordinate(self, color: Color) -> Coordinate:
        """Get the coordinate of the king of the color."""
        king_offset = self._get_king_offset(color)
        row_index, column_index = divmod(king_offset, self.size)
        return Coordinate(row_index, column_index)

    def is_occupied(self, coordinate: Coordinate) -> bool:
        """Return whether the coordinate has a piece on it."""
        piece = self.get_piece(coordinate)
        return piece is not None

    def make_move(self, move: Move) -> None:
        """Make the move and update the state of the from piece."""
        self.set_piece(move.from_coordinate, None)
        if isinstance(move.from_piece, FirstMovePiece):
            move.from_piece.has_moved = True
        self.set_piece(move.to_coordinate, move.from_piece)

    def undo_move(self, move: Move) -> None:
        """Undo a move and restore the state of both the from and to pieces."""
        self.set_piece(move.to_coordinate, move.to_piece)
        if isinstance(move.from_piece, FirstMovePiece):
            move.from_piece.has_moved = move.from_piece_has_moved
        self.set_piece(move.from_coordinate, move.from_piece)

    def get_coordinates_between(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates in a straight line between the from and
        to coordinates."""
        row_difference = to_coordinate.row_index - from_coordinate.row_index
        column_difference = to_coordinate.column_index - from_coordinate.column_index
        step_count = max(abs(row_difference), abs(column_difference))
        are_no_squares_between = step_count < 2
        if are_no_squares_between:
            return []

        row_delta = row_difference // step_count
        column_delta = column_difference // step_count
        between_coordinates = []
        for step in range(1, step_count):
            current_coordinate = Coordinate(
                from_coordinate.row_index + step * row_delta,
                from_coordinate.column_index + step * column_delta,
            )
            between_coordinates.append(current_coordinate)
        return between_coordinates

    def is_path_blocked(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> bool:
        """Return whether there is a piece between the from and to coordinates
        along a straight line."""
        between_coordinates = self.get_coordinates_between(
            from_coordinate, to_coordinate
        )
        for between_coordinate in between_coordinates:
            if self.is_occupied(between_coordinate):
                return True
        return False

    def get_attacker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color that can
        attack the target coordinate."""
        bishop_attacker_coordinates = BishopMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        rook_attacker_coordinates = RookMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        queen_attacker_coordinates = QueenMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        knight_attacker_coordinates = KnightMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        king_attacker_coordinates = KingMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        pawn_attacker_coordinates = PawnMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        return (
            bishop_attacker_coordinates
            + rook_attacker_coordinates
            + queen_attacker_coordinates
            + knight_attacker_coordinates
            + king_attacker_coordinates
            + pawn_attacker_coordinates
        )

    def get_blocker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return the coordinates of all pieces of the color that can block an
        attack by moving to the empty target coordinate."""
        bishop_attacker_coordinates = BishopMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        rook_attacker_coordinates = RookMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        queen_attacker_coordinates = QueenMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        knight_blocker_coordinates = KnightMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        king_blocker_coordinates = KingMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self
        )
        pawn_blocker_coordinate = PawnMoveStrategy.get_blocker_coordinate(
            color, target_coordinate, self
        )
        return (
            bishop_attacker_coordinates
            + rook_attacker_coordinates
            + queen_attacker_coordinates
            + knight_blocker_coordinates
            + king_blocker_coordinates
            + pawn_blocker_coordinate
        )

    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has any empty escape squares."""
        king_coordinate = self.get_king_coordinate(color)
        potential_escape_coordinates = (
            KingMoveStrategy.get_potential_escape_coordinates(king_coordinate, self)
        )
        for potential_escape_coordinate in potential_escape_coordinates:
            if not self.is_attacking(color.opposite, potential_escape_coordinate):
                return False
        return True

    def get_candidate_moves(self, color: Color) -> list[Move]:
        """Return a list of candidate moves for the color not accounting for
        discovered check."""
        candidate_moves = []
        for row_index in range(self._size):
            for column_index in range(self._size):
                current_coordinate = Coordinate(row_index, column_index)
                if not self.is_occupied(current_coordinate):
                    continue

                current_piece = self.get_piece(current_coordinate)
                assert current_piece is not None
                if current_piece.color != color:
                    continue

                candidate_moves.extend(
                    current_piece.MOVE_STRATEGY.get_candidate_moves(
                        color, current_coordinate, self
                    )
                )
        return candidate_moves

    def is_attacking(self, color: Color, coordinate: Coordinate) -> bool:
        """Return whether the color is attacking the coordinate."""
        if not is_coordinate_in_bounds(coordinate):
            return False
        return len(self.get_attacker_coordinates(color, coordinate)) > 0

    def _get_king_offset(self, color: Color) -> int:
        """Return the position of the kinf of the color."""
        return (
            self._white_king_offset if color is Color.WHITE else self._black_king_offset
        )

    def _set_king_offset(self, color: Color, coordinate: Coordinate) -> None:
        """Set the position of the king of the color."""
        board_offset = self._get_board_offset(coordinate)
        if color is Color.WHITE:
            self._white_king_offset = board_offset
        else:
            self._black_king_offset = board_offset

    def _get_board_offset(self, coordinate: Coordinate) -> int:
        """Return the bit offset for the coordinate."""
        return self.size * coordinate.row_index + coordinate.column_index

    def _clear_position_bit(self, board_mask: int) -> None:
        """Clear the bit given by the bit mask for all pieces."""
        self._white_pawns_not_moved_position &= ~board_mask
        self._white_pawns_moved_position &= ~board_mask
        self._white_knights_position &= ~board_mask
        self._white_bishops_position &= ~board_mask
        self._white_rooks_not_moved_position &= ~board_mask
        self._white_rooks_moved_position &= ~board_mask
        self._white_queens_position &= ~board_mask
        self._white_kings_not_moved_position &= ~board_mask
        self._white_kings_moved_position &= ~board_mask

        self._black_pawns_not_moved_position &= ~board_mask
        self._black_pawns_moved_position &= ~board_mask
        self._black_knights_position &= ~board_mask
        self._black_bishops_position &= ~board_mask
        self._black_rooks_not_moved_position &= ~board_mask
        self._black_rooks_moved_position &= ~board_mask
        self._black_queens_position &= ~board_mask
        self._black_kings_not_moved_position &= ~board_mask
        self._black_kings_moved_position &= ~board_mask

    def _set_position_bit(self, piece: Piece, board_mask: int) -> None:
        """Set the bit given by the bit mask for the corresponding piece position."""
        match piece:
            case Pawn(Color.WHITE, False):
                self._white_pawns_not_moved_position |= board_mask
            case Pawn(Color.WHITE, True):
                self._white_pawns_moved_position |= board_mask
            case Knight(Color.WHITE):
                self._white_knights_position |= board_mask
            case Bishop(Color.WHITE):
                self._white_bishops_position |= board_mask
            case Rook(Color.WHITE, False):
                self._white_rooks_not_moved_position |= board_mask
            case Rook(Color.WHITE, True):
                self._white_rooks_moved_position |= board_mask
            case Queen(Color.WHITE):
                self._white_queens_position |= board_mask
            case King(Color.WHITE, False):
                self._white_kings_not_moved_position |= board_mask
            case King(Color.WHITE, True):
                self._white_kings_moved_position |= board_mask

            case Pawn(Color.BLACK, False):
                self._black_pawns_not_moved_position |= board_mask
            case Pawn(Color.BLACK, True):
                self._black_pawns_moved_position |= board_mask
            case Knight(Color.BLACK):
                self._black_knights_position |= board_mask
            case Bishop(Color.BLACK):
                self._black_bishops_position |= board_mask
            case Rook(Color.BLACK, False):
                self._black_rooks_not_moved_position |= board_mask
            case Rook(Color.BLACK, True):
                self._black_rooks_moved_position |= board_mask
            case Queen(Color.BLACK):
                self._black_queens_position |= board_mask
            case King(Color.BLACK, False):
                self._black_kings_not_moved_position |= board_mask
            case King(Color.BLACK, True):
                self._black_kings_moved_position |= board_mask
            case _:
                raise ValueError
