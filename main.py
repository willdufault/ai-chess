from controllers.board_controller import BoardController
from game import Game
from models.board import Board


def main() -> None:
    board = Board()
    board.set_up_pieces()
    board_controller = BoardController(board)
    game = Game(board_controller)
    game.configure()
    game.play()


if __name__ == "__main__":
    main()
