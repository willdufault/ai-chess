from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums.color import Color
    from models.coordinate import Coordinate
    from models.pieces import Piece


@dataclass(frozen=True, slots=True)
class Move:
    color: Color
    from_coordinate: Coordinate
    to_coordinate: Coordinate
    from_piece: Piece | None
    to_piece: Piece | None
    from_piece_has_moved: bool = field(init=False)

    def __post_init__(self) -> None:
        from_piece_has_moved = getattr(self.from_piece, "has_moved", False)
        object.__setattr__(self, "from_piece_has_moved", from_piece_has_moved)
