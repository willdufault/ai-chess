from models.board import Board

MOVE_INPUT_LEN = 4


class InputValidator:
    """Handles input validation checking."""

    @staticmethod
    def is_valid_move_input(move_input: str) -> bool:
        """Return whether the user input is valid."""
        if len(move_input) != MOVE_INPUT_LEN:
            return False

        for digit in move_input:
            if not digit.isdigit():
                return False

            index = int(digit)
            is_in_bounds = Board.is_index_in_bounds(index)
            if not is_in_bounds:
                return False

        return True
