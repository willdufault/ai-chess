from controllers.game_controller import GameController
from models.board import Board
from models.bot_factory import BotFactory
from models.game import Game


def main() -> None:
    board = Board()
    board.set_up_pieces()
    game = Game(board)
    bot_factory = BotFactory()
    game_controller = GameController(game, bot_factory)
    game_controller.configure()
    game_controller.play()


if __name__ == "__main__":
    main()
