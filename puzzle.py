from typing import List, Tuple
from solvers import ISolvable
import numpy as np


# Main objects
class Puzzle(ISolvable):
    """Puzzle grid with X & Y Axis representation with a coordinate system with the origin
    at the top left of the grid."""

    def __init__(self, int_list: List[int], dimension: Tuple[int, int]) -> None:
        super().__init__()
        self.__dimensions = dimension
        if len(dimension) < 2 or dimension[0] < 2 or dimension[1] < 2:
            raise ValueError("Invalid puzzle dimensions. Width & Height needs greater or equal than 2.")

        self.__grid = np.reshape(int_list, (dimension[1], dimension[0]))
        self.__tile_pos = self.__locate_empty_tile()
        self.goal1, self.goal2 = self.__find_goals_states()

    def get_dimensions(self):
        return self.__dimensions

    def get_current_pos(self):
        return self.__tile_pos

    def is_complete(self) -> bool:
        # Quick check. 0 Tile has to minimally be in bottom-right corner.
        if self.get_current_pos() != (self.__dimensions[0] - 1, self.__dimensions[1] - 1):
            return False

        at_1 = np.array_equal(self.__grid, self.goal1)
        at_2 = np.array_equal(self.__grid, self.goal2)

        return at_1 or at_2

    # Puzzle have 2D coordinate system origin at top left of the image
    def __getitem__(self, pos: Tuple[int, int]) -> int:
        return self.__grid[pos[1], pos[0]]

    def __locate_empty_tile(self) -> Tuple[int, int]:
        x, y = 0, 0

        for row in self.__grid:
            for tile in row:
                if tile == 0:
                    return x, y
                x += 1

            y += 1
            x = 0

        raise Exception("No empty tile marked as '0' found in the puzzle definition.")

    def __str__(self) -> str:
        return np.array_str(self.__grid)

    def __find_goals_states(self):
        count = self.__grid.shape[0] * self.__grid.shape[1]
        lin = np.arange(count)
        lin = np.append(lin[1:], lin[0])  # 0 tile is last

        goal1 = np.reshape(lin, self.__grid.shape)

        goal2 = np.reshape(lin, (self.__grid.shape[1], self.__grid.shape[0])).T
        return goal1, goal2

    ## Solvable to be passed in a Solver
    # def solve(self, search_type: SearchType):
    #     if search_type is SearchType.DIJKSTRA:
    #         solver = Djikstra()
    #     if search_type is SearchType.GBFS:
    #         pass
    #     if search_type is SearchType.ASTAR:
    #         pass

    def get_state(self):
        return self.__grid.copy()

    def get_moves(self) -> List[Tuple[int, Tuple[int, int]]]:
        moves = []
        w, h = self.__dimensions
        x, y = self.__tile_pos

        def cost(tile) -> int:
            # Wrapped Horizontally
            if (w > 2) and ((tile[0] == 0 and x == w - 1) or (tile[0] == w - 1 and x == 0)):
                return 2

            # Wrapped Vertically
            if (h > 2) and ((tile[1] == 0 and y == h - 1) or (tile[1] == h - 1 and y == 0)):
                return 2

            # Default: Regular
            return 1

        # Adjacent Moves (Regular [Cost: 1] & Wrapping [Cost: 2])
        top = x, ((y - 1) % h)
        right = ((x + 1) % w), y
        bottom = x, ((y + 1) % h)
        left = ((x - 1) % w), y

        # No duplicate tiles if wrapped with Width or Height of 2
        laterals = []
        if top == bottom:
            laterals.append(top)
        else:
            laterals.append(top)
            laterals.append(bottom)

        if right == left:
            laterals.append(right)
        else:
            laterals.append(right)
            laterals.append(left)

        # Add with tile's cost
        for t in laterals:
            moves.append((cost(t), t))

        # Diagonals
        diagonals = []
        if (h, w) != (2, 2):  # Don't consider 2x2 puzzles
            d1, d2 = None, None
            # Top left || Bottom Right
            if (x, y) == (0, 0) or (x, y) == (w - 1, h - 1):
                d1 = ((x - 1) % w), ((y - 1) % h)
                d2 = ((x + 1) % w), ((y + 1) % h)

            # Top right || Bottom Left
            if (x, y) == (w - 1, 0) or (x, y) == (0, h - 1):
                d1 = ((x - 1) % w), ((y + 1) % h)
                d2 = ((x + 1) % w), ((y - 1) % h)

            if d1 and d2:
                diagonals.append(d1)
                diagonals.append(d2)

        # Add with tile's cost
        for t in diagonals:
            moves.append((3, t))

        # [(cost, (tile.x, tile.y)), ...]
        return moves


# ======

def parse_puzzle(p_list: list, dimension: Tuple[int, int]) -> Puzzle:
    int_arr = np.array(p_list, dtype=np.uint32)
    return Puzzle(int_arr, dimension)


def load_puzzles(puzzle_filename, dimension: Tuple[int, int]) -> List[Puzzle]:
    with open(puzzle_filename, "r") as file:
        p_lines = file.readlines()

    p_list = list(map(lambda l: l.split(), p_lines))
    return list(map(lambda l: parse_puzzle(l, dimension), p_list))
