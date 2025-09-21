from models.board import Board


def main() -> None:
    board = Board()
    board.set_up_pieces()

    from enums.color import Color
    from models.coordinate import Coordinate as Cd
    from models.move import Move as Mv
    from views.board_view import BoardView

    dr = BoardView.draw
    cw = Color.WHITE
    cb = Color.BLACK
    dr(board, cw)
    breakpoint()


if __name__ == "__main__":
    main()
