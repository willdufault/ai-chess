import re

from utils.board_utils import is_index_in_bounds

_MOVE_INPUT_LENGTH = 4
_MOVE_INPUT_PATTERN = rf"\d{{{_MOVE_INPUT_LENGTH}}}"


class MoveParser:
    @staticmethod
    def parse_input(move_input: str) -> tuple[int, int, int, int] | None:
        """Parse the move input return a tuple of four integers if it's valid, otherwise
        return None."""
        match = re.fullmatch(_MOVE_INPUT_PATTERN, move_input)
        if match is None:
            return None

        indexes = tuple(map(int, move_input))
        assert len(indexes) == _MOVE_INPUT_LENGTH
        return indexes
