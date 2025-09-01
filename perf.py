
from controllers.game_controller import GameController
from enums.color import Color
from models.ai import AI
from models.board import Board
from models.game import Game


def main() -> None:
    board = Board()
    board.set_up_pieces()
    ai = AI(Color.WHITE, 0, board)
    game = Game(board)
    game_controller = GameController(game, ai)
    game_controller.configure()
    game_controller.play()


if __name__ == "__main__":
    from cProfile import Profile
    from unittest.mock import patch
    with Profile() as pr:
        try:
            with patch('builtins.input', side_effect=['ai', 'w', '3', '1434', '1333']):
                main()
        except:
            pass
        pr.print_stats(sort=2)
