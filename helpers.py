# Trey Ball
# Assignment 3
# 11-11-2024
# I initally planned to have a lot of helper funcs in here, but after dealing with import loop errors and circular dependencies I decided against this.
# I did however keep count_pieces, as its relatively safe.
# It counts the number of black and white pieces on the board and sends them to the header for display.

def count_pieces(grid):
    black_count = sum(row.count('B') for row in grid)
    white_count = sum(row.count('W') for row in grid)
    return black_count, white_count
