def viz_mask(mask: int) -> None:
    row_indexes = tuple(reversed(range(8)))
    column_indexes = tuple(range(8))
    for row_index in row_indexes:
        for column_index in column_indexes:
            cur_mask = 1 << (8 * row_index + column_index)
            symbol = "x" if mask & cur_mask else "."
            print(symbol, end=" ")
        print()


m = 0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_00000000


viz_mask(m)
