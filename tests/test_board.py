from unittest import TestCase, main

from enums import Color
from models.board import BOARD_SIZE, Board
from models.coordinate import Coordinate
from models.pieces import Bishop, Queen, Rook


class TestBoard(TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_is_occupied(self) -> None:
        self.assertTrue(self.board.is_occupied(Coordinate(0, 0)))
        self.assertFalse(self.board.is_occupied(Coordinate(4, 4)))

    def test_out_of_bounds(self) -> None:
        self.assertTrue(self.board.is_in_bounds(Coordinate(0, 0)))
        self.assertTrue(
            self.board.is_in_bounds(Coordinate(BOARD_SIZE - 1, BOARD_SIZE - 1))
        )
        self.assertFalse(self.board.is_in_bounds(Coordinate(-1, 0)))
        self.assertFalse(self.board.is_in_bounds(Coordinate(0, BOARD_SIZE)))

    def test_is_attacking(self) -> None:
        self.assertFalse(self.board.is_attacking(Color.WHITE, Coordinate(-1, -1)))
        self.assertTrue(self.board.is_attacking(Color.WHITE, Coordinate(2, 0)))

    def test_blocked_vertical(self) -> None:
        self.assertFalse(self.board.is_blocked(Coordinate(0, 0), Coordinate(1, 0)))
        self.assertTrue(self.board.is_blocked(Coordinate(0, 0), Coordinate(2, 0)))

    def test_blocked_horizontal(self) -> None:
        self.assertFalse(self.board.is_blocked(Coordinate(0, 0), Coordinate(0, 1)))
        self.assertTrue(self.board.is_blocked(Coordinate(0, 0), Coordinate(0, 2)))

    def test_blocked_diagonal(self) -> None:
        self.assertFalse(self.board.is_blocked(Coordinate(0, 0), Coordinate(1, 1)))
        self.assertTrue(self.board.is_blocked(Coordinate(0, 0), Coordinate(2, 2)))

    def test_is_king_trapped(self) -> None:
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), None)
        self.assertFalse(self.board.is_king_trapped(Color.WHITE))

        self.board._set_piece(Coordinate(2, 3), Bishop(Color.BLACK))
        self.assertTrue(self.board.is_king_trapped(Color.WHITE))

    def test_is_in_check(self) -> None:
        self.assertFalse(self.board.is_in_check(Color.WHITE))

        self.board._set_piece(Coordinate(3, 4), Queen(Color.BLACK))
        self.assertFalse(self.board.is_in_check(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), None)
        self.assertTrue(self.board.is_in_check(Color.WHITE))

    def test_is_in_checkmate(self) -> None:
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), Queen(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(3, 2), Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 5), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 6), None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), Rook(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(3, 2), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_block(self) -> None:
        self.board._set_piece(Coordinate(1, 3), None)
        self.board._set_piece(Coordinate(3, 1), Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 2), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), Bishop(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 2), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 1), None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 5), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_capture(self) -> None:
        self.board._set_piece(Coordinate(1, 5), None)
        self.board._set_piece(Coordinate(2, 6), Bishop(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 7), None)
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(2, 0), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_pin(self) -> None:
        self.board._set_piece(Coordinate(1, 5), None)
        self.board._set_piece(Coordinate(1, 6), None)
        self.board._set_piece(Coordinate(3, 7), Bishop(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(1, 4), Rook(Color.WHITE))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(3, 4), Rook(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_is_in_checkmate_double_check(self) -> None:
        self.board._set_piece(Coordinate(1, 1), None)
        self.board._set_piece(Coordinate(1, 3), None)
        self.board._set_piece(Coordinate(1, 4), None)
        self.board._set_piece(Coordinate(5, 4), Rook(Color.BLACK))
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(2, 2), Bishop(Color.BLACK))
        self.assertTrue(self.board.is_in_checkmate(Color.WHITE))

        self.board._set_piece(Coordinate(0, 3), None)
        self.assertFalse(self.board.is_in_checkmate(Color.WHITE))

    def test_move_undo_move(self) -> None:
        from_coord = Coordinate(1, 0)
        to_coord = Coordinate(2, 0)
        from_piece = self.board.get_piece(from_coord)
        to_piece = self.board.get_piece(to_coord)
        has_moved = from_piece.has_moved
        self.board.move(from_coord, to_coord)
        self.assertEqual(self.board.get_piece(from_coord), None)
        self.assertEqual(self.board.get_piece(to_coord), from_piece)
        self.board.undo_move(from_coord, to_coord, to_piece, has_moved)
        self.assertEqual(self.board.get_piece(from_coord), from_piece)
        self.assertEqual(self.board.get_piece(to_coord), to_piece)


if __name__ == "__main__":
    main()
