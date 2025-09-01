from enums.color import Color
from models.board import Board
from models.coordinate import Coordinate
from models.move import Move
from models.move_strategies import StraightMoveStrategy
from models.pieces import Pawn
from utils.board_utils import get_last_row_index


class Rules:
    @staticmethod
    def is_in_check(color: Color, board: Board) -> bool:
        """Return whether the color is in check."""
        king_coordinate = board.get_king_coordinate(color)
        return board.is_attacking(color.opposite, king_coordinate)

    @classmethod
    def is_in_checkmate(cls, color: Color, board: Board) -> bool:
        """Return whether the color is in checkmate."""
        if not cls.is_in_check(color, board):
            return False

        if not board.is_king_trapped(color):
            return False

        king_coordinate = board.get_king_coordinate(color)
        attacker_coordinates = board.get_attacker_coordinates(
            color.opposite, king_coordinate
        )
        is_defense_possible = len(attacker_coordinates) < 2
        if not is_defense_possible:
            return True

        attacker_coordinate = attacker_coordinates[0]
        if cls._can_capture_attacker(color, attacker_coordinate, board):
            return False

        if cls._can_block_attacker(color, attacker_coordinate, board):
            return False

        return True

    @staticmethod
    def does_move_trigger_promotion(move: Move) -> bool:
        """Return whether the move meets the criteria for pawn promotion."""
        last_row_index = get_last_row_index(move.color)
        if move.to_coordinate.row_index != last_row_index:
            return False
        return isinstance(move.from_piece, Pawn)

    @classmethod
    def get_legal_moves(cls, color: Color, board: Board) -> list[Move]:
        """Return a list of all legal moves for the color."""
        candidate_moves = board.get_candidate_moves(color)
        return cls._get_legal_candidate_moves(candidate_moves, board)

    @classmethod
    def is_in_check_after_move(cls, move: Move, board: Board) -> bool:
        """Return whether making the move puts the color in check."""
        board.make_move(move)
        is_in_check = cls.is_in_check(move.color, board)
        board.undo_move(move)
        return is_in_check

    @classmethod
    def _get_legal_candidate_moves(
        cls, candidate_moves: list[Move], board: Board
    ) -> list[Move]:
        """Return a list of legal moves out of the candidate moves."""
        legal_moves = []
        for move in candidate_moves:
            if not cls.is_in_check_after_move(move, board):
                legal_moves.append(move)
        return legal_moves

    @classmethod
    def _can_move_to_coordinate(
        cls,
        color: Color,
        to_coordinate: Coordinate,
        from_coordinates: list[Coordinate],
        board: Board,
    ) -> bool:
        """Return whether moving any of the pieces at the from coordinates can
        move to the to coordinate without revealing a discovered check."""
        to_piece = board.get_piece(to_coordinate)
        for from_coordinate in from_coordinates:
            from_piece = board.get_piece(from_coordinate)
            move = Move(color, from_coordinate, to_coordinate, from_piece, to_piece)
            if not cls.is_in_check_after_move(move, board):
                return True
        return False

    @classmethod
    def _can_capture_attacker(
        cls, color: Color, attacker_coordinate: Coordinate, board: Board
    ) -> bool:
        """Return whether the color can capture the attacker at the coordinate."""
        defender_coordinates = board.get_attacker_coordinates(
            color, attacker_coordinate
        )
        return cls._can_move_to_coordinate(
            color, attacker_coordinate, defender_coordinates, board
        )

    @classmethod
    def _can_block_attacker(
        cls, color: Color, attacker_coordinate: Coordinate, board: Board
    ):
        """Return whether the color can block an attack from the coordinate."""
        attacker = board.get_piece(attacker_coordinate)
        assert attacker is not None
        if not isinstance(attacker.MOVE_STRATEGY, StraightMoveStrategy):
            return False

        king_coordinate = board.get_king_coordinate(color)
        between_coordinates = board.get_coordinates_between(
            king_coordinate, attacker_coordinate
        )
        for between_coordinate in between_coordinates:
            blocker_coordinates = board.get_blocker_coordinates(
                color, between_coordinate
            )
            can_block_current_coordinate = cls._can_move_to_coordinate(
                color, between_coordinate, blocker_coordinates, board
            )
            if can_block_current_coordinate:
                return True
        return False
