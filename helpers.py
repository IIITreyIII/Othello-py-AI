def count_pieces(grid):
    black_count = sum(row.count('B') for row in grid)
    white_count = sum(row.count('W') for row in grid)
    return black_count, white_count
