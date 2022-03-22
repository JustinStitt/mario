from meta import meta

def row_col_to_pos(r: int, c: int) -> list[int]:
    x = r * meta.screen.CELL_HEIGHT
    y = c * meta.screen.CELL_WIDTH
    return (x, y)
