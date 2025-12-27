from models.board import Board


class Game:
    def __init__(self, board: Board) -> None:
        self._board = board
