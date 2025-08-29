from enums.color import Color
from models.board import Board
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
from models.pieces import FirstMovePiece, Knight, Pawn
from utils.board_utils import get_last_row_index, is_coordinate_in_bounds


class BoardController:
    """Manages the board state."""

    def __init__(self, board: Board) -> None:
        self._board = board

    # TODO: Replace with board hash for BoardView.draw()?
    @property
    def board(self) -> Board:
        return self._board

    def make_move(self, move: Move) -> None:
        """Make the move on the board and update the state of the from piece."""
        self._board.set_piece(move.from_coordinate, None)
        self._board.set_piece(move.to_coordinate, move.from_piece)
        if isinstance(move.from_piece, FirstMovePiece):
            move.from_piece.has_moved = True

    def undo_move(self, move: Move) -> None:
        """Undo a move and restore the state of both the from and to pieces."""
        reversed_move = Move(
            move.color, move.to_coordinate, move.from_coordinate, move.from_piece, None
        )
        self.make_move(reversed_move)
        self._board.set_piece(move.to_coordinate, move.to_piece)
        if isinstance(move.from_piece, FirstMovePiece):
            move.from_piece.has_moved = move.from_piece_has_moved

    def does_move_trigger_promotion(self, move: Move) -> bool:
        """Return whether the move meets the criteria for pawn promotion."""
        last_row_index = get_last_row_index(move.color)
        if move.to_coordinate.row_index != last_row_index:
            return False
        return isinstance(move.from_piece, Pawn)

    def is_attacking(self, color: Color, coordinate: Coordinate) -> bool:
        """Return whether the color is attacking the coordinate."""
        if not is_coordinate_in_bounds(coordinate):
            return False
        return len(self._get_attacker_coordinates(color, coordinate)) > 0

    def is_in_check(self, color: Color) -> bool:
        """Return whether the color is in check."""
        king_coordinate = self._board.get_king_coordinate(color)
        return self.is_attacking(color.opposite, king_coordinate)

    def is_in_checkmate(self, color: Color) -> bool:
        """Return whether the color is in checkmate."""
        # TODO: check this twice in game loop, cache with board hash
        if not self.is_in_check(color):
            return False

        if not self._is_king_trapped(color):
            return False

        king_coordinate = self._board.get_king_coordinate(color)
        attacker_coordinates = self._get_attacker_coordinates(
            color.opposite, king_coordinate
        )
        is_defense_possible = len(attacker_coordinates) < 2
        if not is_defense_possible:
            return True

        attacker_coordinate = attacker_coordinates[0]
        if self._can_capture_attacker(color, attacker_coordinate):
            return False

        if self._can_block_attacker(color, attacker_coordinate):
            return False

        return True

    def get_legal_moves(self, color: Color) -> list[Move]:
        """Return a list of all legal moves for the color."""
        # TODO
        raise NotImplementedError

    def _simulate_defense(
        self,
        color: Color,
        to_coordinate: Coordinate,
        from_coordinates: list[Coordinate],
    ) -> bool:
        """Return whether moving any of the pieces at the from coordinates can
        move to the to coordinate without revealing a discovered check."""
        to_piece = self._board.get_piece(to_coordinate)
        for from_coordinate in from_coordinates:
            from_piece = self._board.get_piece(from_coordinate)
            move = Move(color, from_coordinate, to_coordinate, from_piece, to_piece)
            self.make_move(move)
            is_still_in_check = self.is_in_check(color)
            self.undo_move(move)
            if not is_still_in_check:
                return True
        return False

    def _is_king_trapped(self, color: Color) -> bool:
        """Return whether the king of the color has any empty escape squares."""
        king_coordinate = self._board.get_king_coordinate(color)
        potential_escape_coordinates = (
            KingMoveStrategy.get_potential_escape_coordinates(
                king_coordinate, self._board
            )
        )
        for potential_escape_coordinate in potential_escape_coordinates:
            if not self.is_attacking(color.opposite, potential_escape_coordinate):
                return False
        return True

    def _get_attacker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return a list of coordinates of all pieces of the color that can
        attack the target coordinate."""
        bishop_attacker_coordinates = BishopMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        rook_attacker_coordinates = RookMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        queen_attacker_coordinates = QueenMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        knight_attacker_coordinates = KnightMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        king_attacker_coordinates = KingMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        pawn_attacker_coordinates = PawnMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        return (
            bishop_attacker_coordinates
            + rook_attacker_coordinates
            + queen_attacker_coordinates
            + knight_attacker_coordinates
            + king_attacker_coordinates
            + pawn_attacker_coordinates
        )

    def _get_blocker_coordinates(
        self, color: Color, target_coordinate: Coordinate
    ) -> list[Coordinate]:
        """Return the coordinates of all pieces of the color that can block an
        attack by moving to the empty target coordinate."""
        bishop_attacker_coordinates = BishopMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        rook_attacker_coordinates = RookMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        queen_attacker_coordinates = QueenMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        knight_blocker_coordinates = KnightMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        king_blocker_coordinates = KingMoveStrategy.get_attacker_coordinates(
            color, target_coordinate, self._board
        )
        pawn_blocker_coordinate = PawnMoveStrategy.get_blocker_coordinate(
            color, target_coordinate, self._board
        )
        return (
            bishop_attacker_coordinates
            + rook_attacker_coordinates
            + queen_attacker_coordinates
            + knight_blocker_coordinates
            + king_blocker_coordinates
            + pawn_blocker_coordinate
        )

    def _can_capture_attacker(
        self, color: Color, attacker_coordinate: Coordinate
    ) -> bool:
        """Return whether the color can capture the attacker at the coordinate."""
        defender_coordinates = self._get_attacker_coordinates(
            color, attacker_coordinate
        )
        return self._simulate_defense(color, attacker_coordinate, defender_coordinates)

    def _can_block_attacker(self, color: Color, attacker_coordinate: Coordinate):
        """Return whether the color can block an attack from the coordinate."""
        attacker = self._board.get_piece(attacker_coordinate)
        if isinstance(attacker, Knight):
            return False

        king_coordinate = self._board.get_king_coordinate(color)
        between_coordinates = self._board.get_coordinates_between(
            king_coordinate, attacker_coordinate
        )
        for between_coordinate in between_coordinates:
            blocker_coordinates = self._get_blocker_coordinates(
                color, between_coordinate
            )
            can_block_current_coordinate = self._simulate_defense(
                color, between_coordinate, blocker_coordinates
            )
            if can_block_current_coordinate:
                return True
        return False
