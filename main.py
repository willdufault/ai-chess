from board import Board
from game import Game


def main() -> None:
    game = Game(Board())
    game.configure()
    game.play()


if __name__ == "__main__":
    main()
