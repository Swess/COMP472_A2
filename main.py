import argparse
import json
import random
from helpers import *
from puzzle import load_puzzles, find_goals
from solvers import Djikstra
import numpy as np


def generate_rand_puzzles(n, dimensions):
    exist = os.path.isfile('./generated_puzzles.txt')
    if exist:
       input("The file 'generated_puzzles.txt' already exist.\nPress any key to confirm content overwriting. Close "
             "process otherwise.")

    lines = []
    for i in range(n):
        lin = np.arange(dimensions[0] * dimensions[1])
        puzzle_arr = lin.tolist()
        random.shuffle(puzzle_arr)
        lines.append(" ".join(list(map(str, puzzle_arr))) + "\n")

    with open("generated_puzzles.txt", "w") as file:
        file.writelines(lines)


def main(args):
    gen, in_file, out_dir, dimensions = args.generate, args.input_file, args.output, json.loads(args.dimensions)

    if len(dimensions) < 2 or (dimensions[0] * dimensions[1]) % 2 != 0:
        raise ValueError("Invalid given dimension.")

    if gen > 0:
        generate_rand_puzzles(gen, dimensions)

    create_dir(out_dir)
    puzzles = load_puzzles(in_file, dimensions)

    for p in puzzles:
        print(p)
        # Print possible moves as Assignment desire
        # print(list(map(lambda x: (x[0], p[x[1]]), p.get_moves())))
        print()

    # For testing
    solver = Djikstra()
    goals = find_goals(puzzles[0])
    steps_to_goal = solver.solve(puzzles[0], goals[0])

    print("Solved it! Solution is:")
    print()
    for s in steps_to_goal:
        print()
        print(s)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Solves gixen X-Puzzle with different solvers.')

    arg_parser.add_argument('input_file', metavar='input_file', type=str,
                            help='Path to the puzzle(s) definition(s) file to use.')

    arg_parser.add_argument("-g", "--generate", type=int, default=0,
                            help="If this flag is set, N random puzzles with given dimension will be generated in "
                                 "./generated_puzzles.txt before anything else.")

    arg_parser.add_argument("-d", "--dimensions", metavar="<[width, height]>", type=str,
                            help="2D dimensions of the input puzzle. Default: [4, 2]",
                            default="[4, 2]")

    arg_parser.add_argument("-o", "--output", metavar="<output>", type=str,
                            help="Output directory relative to current working directory. Default: _out/",
                            default="_out/")

    args = arg_parser.parse_args()

    main(args)
