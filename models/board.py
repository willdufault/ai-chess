from abc import ABC, abstractmethod

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

_KING_COLUMN_INDEX = 4
_WHITE_PAWN_ROW_INDEX = 1
_BLACK_PAWN_ROW_INDEX = BOARD_SIZE - 2


# TODO: TRY BITBOARD WITH ABS BOARD CLASS TO KEEP PUBLIC INTERFACE
class Board(ABC):
    @abstractmethod
    def to_key(self) -> str:
        """Return an immutable version of the board state for caching."""
        pass

    @abstractmethod
    def set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        pass

    @abstractmethod
    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        """Get the piece at the coordinate."""
        pass

    @abstractmethod
    def set_piece(self, coordinate: Coordinate, piece: Piece | None) -> None:
        """Set the piece at the coordinate."""
        pass

    @abstractmethod
    def get_king_coordinate(self, color: Color) -> Coordinate:
        """Get the coordinate of the king of the color."""
        pass

    @abstractmethod
    def is_occupied(self, coordinate: Coordinate) -> bool:
        """Return whether the coordinate has a piece on it."""
        pass

    @abstractmethod
    def make_move(self, move: Move) -> None:
        """Make the move and update the state of the from piece."""
        pass

    @abstractmethod
    def undo_move(self, move: Move) -> None:
        """Undo a move and restore the state of both the from and to pieces."""
        pass

    @abstractmethod
    def get_coordinates_between(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates in a straight line between the from and
        to coordinates."""
        pass

    @abstractmethod
    def is_path_blocked(
        self, from_coordinate: Coordinate, to_coordinate: Coordinate
    ) -> bool:
        """Return whether there is a piece between the from and to coordinates
        along a straight line."""
        pass

    @abstractmethod
    def get_attacker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color that can
        attack the target coordinate."""
        pass

    @abstractmethod
    def get_blocker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return the coordinates of all pieces of the color that can block an
        attack by moving to the empty target coordinate."""
        pass

    @abstractmethod
    def is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has any empty escape squares."""
        pass

    @abstractmethod
    def get_candidate_moves(self, color: Color) -> list[Move]:
        """Return a list of candidate moves for the color not accounting for
        discovered check."""
        pass

    @abstractmethod
    def is_attacking(self, color: Color, coordinate: Coordinate) -> bool:
        """Return whether the color is attacking the coordinate."""
        pass


class SimpleBoard(Board):
    def __init__(self) -> None:
        self.size = BOARD_SIZE
        self._squares: list[Piece | None] = [None] * (self.size * self.size)
        self._white_king_coordinate = Coordinate(-1, -1)
        self._black_king_coordinate = Coordinate(-1, -1)

    def to_key(self) -> str:
        """Return an immutable version of the board state for caching."""
        key = []
        for row_index in range(self.size):
            for column_index in range(self.size):
                coordinate = Coordinate(row_index, column_index)
                if not self.is_occupied(coordinate):
                    key.append("_")
                    continue

                piece = self.get_piece(coordinate)
                assert piece is not None
                key.append(piece.to_key())
        key_str = "".join(key)
        return key_str

    def set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_type_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for column_index, piece_type in enumerate(piece_type_order):
            white_piece_coordinate = Coordinate(0, column_index)
            black_piece_coordinate = Coordinate(self.size - 1, column_index)
            white_pawn_coordinate = Coordinate(_WHITE_PAWN_ROW_INDEX, column_index)
            black_pawn_coordinate = Coordinate(_BLACK_PAWN_ROW_INDEX, column_index)
            self.set_piece(white_piece_coordinate, piece_type(Color.WHITE))
            self.set_piece(black_piece_coordinate, piece_type(Color.BLACK))
            self.set_piece(white_pawn_coordinate, Pawn(Color.WHITE))
            self.set_piece(black_pawn_coordinate, Pawn(Color.BLACK))
        self._set_king_coordinate(Color.WHITE, Coordinate(0, _KING_COLUMN_INDEX))
        self._set_king_coordinate(
            Color.BLACK, Coordinate(self.size - 1, _KING_COLUMN_INDEX)
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
        reversed_move = Move(
            move.color, move.to_coordinate, move.from_coordinate, move.from_piece, None
        )
        self.make_move(reversed_move)
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
        for row_index in range(self.size):
            for column_index in range(self.size):
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
    def __init__(self) -> None:
        self.size = BOARD_SIZE
        self._squares: list[Piece | None] = [None] * (self.size * self.size)
        self._white_king_coordinate = Coordinate(-1, -1)
        self._black_king_coordinate = Coordinate(-1, -1)

    def to_key(self) -> str:
        """Return an immutable version of the board state for caching."""
        key = []
        for row_index in range(self.size):
            for column_index in range(self.size):
                coordinate = Coordinate(row_index, column_index)
                if not self.is_occupied(coordinate):
                    key.append("_")
                    continue

                piece = self.get_piece(coordinate)
                assert piece is not None
                key.append(piece.to_key())
        key_str = "".join(key)
        return key_str

    def set_up_pieces(self) -> None:
        """Place the pieces on their starting squares."""
        piece_type_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for column_index, piece_type in enumerate(piece_type_order):
            white_piece_coordinate = Coordinate(0, column_index)
            black_piece_coordinate = Coordinate(self.size - 1, column_index)
            white_pawn_coordinate = Coordinate(_WHITE_PAWN_ROW_INDEX, column_index)
            black_pawn_coordinate = Coordinate(_BLACK_PAWN_ROW_INDEX, column_index)
            self.set_piece(white_piece_coordinate, piece_type(Color.WHITE))
            self.set_piece(black_piece_coordinate, piece_type(Color.BLACK))
            self.set_piece(white_pawn_coordinate, Pawn(Color.WHITE))
            self.set_piece(black_pawn_coordinate, Pawn(Color.BLACK))
        self._set_king_coordinate(Color.WHITE, Coordinate(0, _KING_COLUMN_INDEX))
        self._set_king_coordinate(
            Color.BLACK, Coordinate(self.size - 1, _KING_COLUMN_INDEX)
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
        reversed_move = Move(
            move.color, move.to_coordinate, move.from_coordinate, move.from_piece, None
        )
        self.make_move(reversed_move)
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
        for row_index in range(self.size):
            for column_index in range(self.size):
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
