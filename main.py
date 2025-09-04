from controllers.game_controller import GameController
from enums.color import Color
from models.ai import AI
from models.board import SimpleBoard
from models.game import Game


def main() -> None:
    board = SimpleBoard()
    board.set_up_pieces()
    ai = AI(Color.WHITE, 0, board)
    game = Game(board)
    game_controller = GameController(game, ai)
    game_controller.configure()
    game_controller.play()


if __name__ == "__main__":
    main()
