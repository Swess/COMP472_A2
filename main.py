import argparse
import json
import random
import time

from helpers import *
from puzzle import *
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


# Retracing steps of solution backward in resulting search graph
def retrace_steps(search_graph: Dict[Puzzle, Tuple[Puzzle, Any]], final_state: Puzzle) -> List[Tuple[Puzzle, int, int]]:
    steps = []
    c = final_state
    while c in search_graph.keys():
        prev_state, move = search_graph[c]
        steps.append((c, move[0], prev_state[move[1]]))
        c = prev_state

    steps.append((c, 0, 0))  # Initial state
    steps.reverse()
    return steps


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
            # "h2": lambda current, goal: 1
        }),
        "AStar": (AStar(), {
            "h1": lambda current, goal: 1,
            # "h2": lambda current, goal: 1
        })
    }

    for i, p in enumerate(puzzles):
        print("===============")
        print("Will solve puzzle:")
        print(p)
        goals = find_goals(p)

        for name in solvers:
            solver, heuristics_functions = solvers[name]
            for h_name in heuristics_functions:
                h_func = heuristics_functions[h_name]

                if h_name == "default":
                    f_name = f"{i}_{name.lower()}"
                    print(f"Solving with solver {name}...")
                else:
                    f_name = f"{i}_{name.lower()}-{h_name}"
                    print(f"Solving with solver {name}, with heuristic '{h_name}'...")

                out_sol_file = f"./_out/{f_name}_solution.txt"
                out_search_file = f"./_out/{f_name}_search.txt"

                # TODO: Parallel Search for both goals
                t_start = time.monotonic()
                search_graph, search_path = solver.solve(p, goals[0], h_func)
                elapsed = time.monotonic() - t_start
                elapsed = "{:.4f}".format(elapsed)

                print(f"Solved it in {elapsed} seconds! Solution at '{out_sol_file}'.")
                steps_to_goal = retrace_steps(search_graph, goals[0])

                # Solution output file
                with open(out_sol_file, 'w') as sol_file:
                    total_cost = 0
                    for state, move_cost, tile_moved in steps_to_goal:
                        # Display solution states in console
                        # print(f"Move tile {tile_moved}, for cost of {move_cost}.")
                        # print(state)

                        total_cost += move_cost
                        sol_file.write(f"{tile_moved} {str(move_cost)} {state.to_single_line_str()}\n")
                    sol_file.write(f"{total_cost} {elapsed}")

                # TODO: Write search file
                # Search path file
                with open(out_search_file, 'w') as search_file:
                    for s in search_path:
                        info = search_graph[search_file]

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
