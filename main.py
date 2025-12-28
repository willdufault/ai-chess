from controllers.game_controller import GameController
from models.board import Board
from models.game import Game


def main() -> None:
    board = Board()
    game = Game(board)
    game_controller = GameController(game)
    game_controller.configure()
    game_controller.play()


if __name__ == "__main__":
    main()
