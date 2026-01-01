from controllers.game_controller import GameController
from models.ai_factory import AiFactory
from models.board import Board
from models.game import Game


def main() -> None:
    board = Board()
    board.set_up_pieces()
    game = Game(board)
    ai_factory = AiFactory()
    game_controller = GameController(game, ai_factory)
    game_controller.configure()
    game_controller.play()


if __name__ == "__main__":
    main()
