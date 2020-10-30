from typing import List, Tuple
import numpy as np


# Main objects
class Puzzle:

    def __init__(self, int_list: List[int], dimension: Tuple[int, int]) -> None:
        super().__init__()
        self.grid = np.reshape(int_list, (dimension[1], dimension[0]))
        self.tile_pos = self.__locate_empty_tile()
        self.goal1, self.goal2 = self.__find_goals()

    def is_complete(self):
        at_1 = np.array_equal(self.grid, self.goal1)
        at_2 = np.array_equal(self.grid, self.goal2)

        return at_1 or at_2

    # Puzzle have 2D coordinate system origin at top left of the image
    def __getitem__(self, pos: Tuple[int, int]) -> int:
        return self.grid[pos[1], pos[0]]

    def __locate_empty_tile(self) -> Tuple[int, int]:
        x, y = 0, 0

        for row in self.grid:
            for tile in row:
                if tile == 0:
                    return x, y
                x += 1

            y += 1
            x = 0

        raise Exception("No empty tile marked as '0' found in the puzzle definition.")

    def __str__(self) -> str:
        return np.array_str(self.grid)

    def __find_goals(self):
        count = self.grid.shape[0] * self.grid.shape[1]
        lin = np.arange(count)
        lin = np.append(lin[1:], lin[0])  # 0 tile is last

        goal1 = np.reshape(lin, self.grid.shape)

        goal2 = np.reshape(lin, (self.grid.shape[1], self.grid.shape[0])).T
        return goal1, goal2


# ======

def parse_puzzle(p_list: list, dimension: Tuple[int, int]):
    int_arr = np.array(p_list, dtype=np.uint32)
    return Puzzle(int_arr, dimension)


def load_puzzles(puzzle_filename, dimension: Tuple[int, int]):
    with open(puzzle_filename, "r") as file:
        p_lines = file.readlines()

    p_list = list(map(lambda l: l.split(), p_lines))
    return list(map(lambda l: parse_puzzle(l, dimension), p_list))
