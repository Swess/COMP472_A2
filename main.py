import argparse
import json
import random
import time

from helpers import *
from puzzle import load_puzzles, find_goals
from solvers import *
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
        raise ValueError("Invalid dimensions given.")

    if gen > 0:
        generate_rand_puzzles(gen, dimensions)

    create_dir(out_dir)
    puzzles = load_puzzles(in_file, dimensions)

    # Solvers with each heuristics
    solvers = {
        "UCS": (UCS(), {
            "default": lambda current, goal: 1
        }),
        "GBFS": (GBFS(), {
            "h1": lambda current, goal: 1,
            #"h2": lambda current, goal: 1
        }),
        "AStar": (AStar(), {
            "h1": lambda current, goal: 1,
            #"h2": lambda current, goal: 1
        })
    }

    for p in puzzles:
        print("===============")
        print("Will solve puzzle:")
        print(p)
        goals = find_goals(p)

        for name in solvers:
            solver, heuristics_functions = solvers[name]
            for h_name in heuristics_functions:
                h_func = heuristics_functions[h_name]

                if h_name == "default":
                    print(f"Solving with solver {name}...")
                else:
                    print(f"Solving with solver {name}, with heuristic '{h_name}'...")

                # TODO: Parallel Search for both goals
                t_start = time.monotonic()
                steps_to_goal = solver.solve(p, goals[0], h_func)
                elapsed = time.monotonic() - t_start

                print(f"Solved it in {elapsed} seconds! Solution is:")
                print()
                for s in steps_to_goal:
                    print()
                    print(s)

        # Print possible moves as Assignment desire
        # print(list(map(lambda x: (x[0], p[x[1]]), p.get_moves())))
        print()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Solves given X-Puzzle with different solvers.')

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
