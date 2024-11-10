import numpy as np
from Config import *


def new_grid():
    grid = np.zeros((ROWS, COLUMNS))
    print(np.flip(grid, 0))
    return grid

def is_valid_position(grid, col):
    return grid[ROWS-1][col] == 0

def get_valid_position(grid):
    valid_position = []
    for col in range(COLUMNS):
        if is_valid_position(grid, col):
            valid_position.append(col)

    return valid_position

def get_next_open_row(grid, c):
    for r in range(ROWS):
        if grid[r][c] == 0:
            return r