from utils.board_utils import is_index_in_bounds

_MOVE_INPUT_LEN = 4


class InputValidator:
    @staticmethod
    def is_valid_move_input(move_input: str) -> bool:
        """Return whether the user input is valid."""
        if len(move_input) != _MOVE_INPUT_LEN:
            return False

        for digit in move_input:
            if not digit.isdigit():
                return False

            index = int(digit)
            is_in_bounds = is_index_in_bounds(index)
            if not is_in_bounds:
                return False

        return True
