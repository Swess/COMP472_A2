import math
import numpy as np
from puzzle import Puzzle


def h0(current: Puzzle, goal: Puzzle) -> int:
    dim = current.get_dimensions()
    pos = current.get_current_pos()
    if pos == (dim[0] - 1, dim[1] - 1):
        return 0
    return 1


def h1(current: Puzzle, goal: Puzzle) -> int:
    # Manhattan Distance, will toroidal consideration
    total = 0
    dim = current.get_dimensions()
    count = dim[0] * dim[1]
    is_hor_goal = goal[(1, 0)] == 2  # To speed of function computation and use goal state assumption (2 goals only)

    for x in range(dim[0]):
        for y in range(dim[1]):
            v = current[(x, y)]
            shifted_v = (v - 1) % count
            if is_hor_goal:
                expected_x = shifted_v % dim[0]
                expected_y = math.floor(shifted_v / dim[0])
            else:
                expected_x = math.floor(shifted_v / dim[1])
                expected_y = shifted_v % dim[1]

            diff_x = abs(expected_x - x)
            diff_y = abs(expected_y - y)
            calc_diff_x = math.ceil(diff_x / 2) if diff_x > math.ceil(dim[0] / 2) else diff_x
            calc_diff_y = math.ceil(diff_y / 2) if diff_y > math.ceil(dim[1] / 2) else diff_y
            total += calc_diff_x + calc_diff_y

    return total


def h2(current: Puzzle, goal: Puzzle) -> int:
    # Sum of element-wise numerical difference of tile values
    # Ex: Tile should have 6, but has 4 => 6-4
    grid1 = current.get_internal_state()
    grid2 = goal.get_internal_state()
    sub = np.subtract(grid1, grid2)
    diff = np.abs(sub)
    x = np.sum(diff.flatten())
    return x