import argparse
import json
import random
import time
import concurrent.futures
from concurrent.futures.thread import ThreadPoolExecutor

from helpers import *
from heuristics import h0, h1, h2
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

    if len(dimensions) < 2:
        raise ValueError("Invalid dimensions given.")

    if gen > 0:
        generate_rand_puzzles(gen, dimensions)

    create_dir(out_dir)
    puzzles = load_puzzles(in_file, dimensions)

    # Solvers with each heuristics
    demo_heuristics_func_set = {"h0": h0}
    heuristics_func_set = {"h1": h1, "h2": h2}
    best = {"h1": h1}

    # heuristics_func_set = best

    solvers = {
        "UCS": (UCS(), {
            "default": lambda current, goal: 0
        }),
        "GBFS": (GBFS(), heuristics_func_set),
        "AStar": (AStar(), heuristics_func_set)
    }

    executor = ThreadPoolExecutor(max_workers=2)
    all_metrics = []
    for i, p in enumerate(puzzles):
        print("===============")
        print("Will solve puzzle:")
        print(p)
        goals = find_goals(p)

        for name in solvers:
            solver, heuristics_functions = solvers[name]
            for h_name in heuristics_functions:
                print("-----")
                h_func = heuristics_functions[h_name]

                if h_name == "default":
                    f_name = f"{i}_{name.lower()}"
                    print(f"Solving with solver {name}...")
                else:
                    f_name = f"{i}_{name.lower()}-{h_name}"
                    print(f"Solving with solver {name}, with heuristic '{h_name}'...")

                out_sol_file = f"./{out_dir}{f_name}_solution.txt"
                out_search_file = f"./{out_dir}{f_name}_search.txt"

                steps_to_goal = None
                t_start = time.monotonic()
                future = executor.submit(solver.solve, p, list(goals), h_func)
                try:
                    steps_to_goal, visited_nodes = future.result(timeout=60)
                    elapsed = time.monotonic() - t_start
                    elapsed = "{:.4f}".format(elapsed)
                except concurrent.futures.TimeoutError as e:
                    future.cancel()
                    print(f"Could not find solution in 60sec.")
                    print("Failed to find solution...")
                    with open(out_sol_file, 'w') as sol_file:
                        sol_file.write("no solution")
                    with open(out_search_file, 'w') as search_file:
                        search_file.write("no solution")

                    # Register as not found
                    all_metrics.append({
                        "solver": name,
                        "heuristic_function": h_name,
                        "no_sol": True
                    })
                    continue

                print(f"Solved it in {elapsed} seconds!")

                # Solution output file
                total_cost = 0
                with open(out_sol_file, 'w') as sol_file:
                    for state, move_cost, tile_moved in steps_to_goal:
                        # Display solution states in console
                        # print(f"Move tile {tile_moved}, for cost of {move_cost}.")
                        # print(state)
                        # print()

                        total_cost += move_cost
                        sol_file.write(f"{tile_moved} {str(move_cost)} {state.to_single_line_str()}\n")
                    sol_file.write(f"{total_cost} {elapsed}")

                print(f"Solution at '{out_sol_file}'.")

                # Search path file
                with open(out_search_file, 'w') as search_file:
                    for n in visited_nodes:
                        f, g, h = visited_nodes[n]
                        f = solver.f(g, h)
                        search_file.write(f"{f} {g} {h} {n.to_single_line_str()}\n")

                print(f"Search path at '{out_search_file}'.")

                # Add Metrics
                all_metrics.append({
                    "solver": name,
                    "heuristic_function": h_name,
                    "solution_length": len(steps_to_goal),
                    "search_length": len(visited_nodes),
                    "total_cost": float(total_cost),
                    "elapsed": float(elapsed)
                })

    ########
    # All metrics
    total_nb_run = len(all_metrics)
    h_names = [h for h in heuristics_func_set if h != "default"]

    print("\n\n\n>>>>>>>>>>>>>>>>>")
    print("Metrics >>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>\n")
    if total_nb_run == 0:
        print("Nothing to show...")
        return

    # No Solutions...
    group = [m for m in all_metrics if 'no_sol' in m]
    total = len(group)
    print("<| No Solution |>")
    print(f"Total: {total}")
    print(f"Average: {total / total_nb_run} ({total} / {total_nb_run})\n")

    # By solver
    for s_name in solvers:
        s_group = len([m for m in all_metrics if m["solver"] == s_name])
        s_total_count = len([m for m in group if m["solver"] == s_name])
        if s_group == 0:
            continue

        print(f"{s_name} Average: {s_total_count / s_group} ({s_total_count} / {s_group})")

    # By Heuristic
    for h_name in h_names:
        h_group = len([m for m in all_metrics if m["heuristic_function"] == h_name])
        h_total_m = len([m for m in group if m["heuristic_function"] == h_name])
        if h_group == 0:
            continue
        print(f"{h_name} Average: {h_total_m / h_group} ({h_total_m} / {h_group})")

    print("\n\n")

    # Other numerical metrics
    metrics = {
        # "No Solution": [m for m in all_metrics if 'no_sol' in m],
        "Solution Length": "solution_length",
        "Search Length": "search_length",
        "Total Cost": "total_cost",
        "Elapsed": "elapsed"
    }

    for metric_display_name in metrics:
        metric = metrics[metric_display_name]
        group = [m[metric] for m in all_metrics]
        group_count = len(group)
        group_sum = sum(group)

        print(f"<| {metric_display_name} |>")
        print(f"Total: {group_sum}")
        print(f"Average: {group_sum / group_count} ({group_sum} / {group_count})\n")

        # By solver
        for s_name in solvers:
            s_group = [m[metric] for m in all_metrics if "solver" in m and m["solver"] == s_name]
            s_group_sum = sum(s_group)
            if len(s_group) == 0:
                continue

            print(f"{s_name} Average: {s_group_sum / len(s_group)} ({s_group_sum} / {len(s_group)})")

        # By Heuristic
        for h_name in h_names:
            h_group = [m[metric] for m in all_metrics if
                       "heuristic_function" in m and m["heuristic_function"] == h_name]
            h_group_sum = sum(h_group)
            if len(h_group) == 0:
                continue
            print(f"{h_name} Average: {h_group_sum / len(h_group)} ({h_group_sum} / {len(h_group)})")

        print()
        # By solver -> Heuristic
        for s_name in solvers:
            for h_name in h_names:
                s_group = [m[metric] for m in all_metrics if ("solver" in m and m["solver"] == s_name) and (
                            "heuristic_function" in m and m["heuristic_function"] == h_name)]
                s_group_sum = sum(s_group)
                if len(s_group) == 0:
                    continue

                print(f"{s_name} {h_name} Average: {s_group_sum / len(s_group)} ({s_group_sum} / {len(s_group)})")

        print("\n\n\n")


if __name__ == "__main__":
    print("<<<<<<<<<<<<>>>>>>>>>>>>")
    print("COMP 472 - Assignment 2")
    print("Isaac Doré - 40043159")
    print("<<<<<<<<<<<<>>>>>>>>>>>>")
    print()

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
