from models.board import Board
from models.game import Game


def main() -> None:
    game = Game(Board())
    game.configure()
    game.play()


if __name__ == "__main__":
    main()
