def signed_shift(base: int, shift: int) -> int:
    return base << shift if shift > 0 else base >> -shift


def intersects(value: int, mask: int) -> bool:
    return (value & mask) != 0


def get_shift(square_mask: int) -> int:
    return square_mask.bit_length() - 1
