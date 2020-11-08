from puzzle import Puzzle


def h0(current: Puzzle, goal: Puzzle) -> int:
    dim = current.get_dimensions()
    pos = current.get_current_pos()
    if pos == (dim[0]-1, dim[1]-1):
        return 0
    return 1


def h1(current: Puzzle, goal: Puzzle) -> int:
    return 1


def h2(current: Puzzle, goal: Puzzle) -> int:
    return 1
