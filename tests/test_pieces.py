from enums.color import Color
from models.pieces import Bishop, King, Knight, Pawn, Queen, Rook


def test_equals() -> None:
    assert Pawn(Color.WHITE) == Pawn(Color.WHITE)
    assert Knight(Color.WHITE) == Knight(Color.WHITE)
    assert Bishop(Color.WHITE) == Bishop(Color.WHITE)
    assert Rook(Color.BLACK) == Rook(Color.BLACK)
    assert Queen(Color.BLACK) == Queen(Color.BLACK)
    assert King(Color.BLACK) == King(Color.BLACK)


def test_not_equals() -> None:
    assert Pawn(Color.WHITE) != Pawn(Color.BLACK)
    assert Pawn(Color.WHITE) != Bishop(Color.WHITE)
    assert Pawn(Color.WHITE) != None
