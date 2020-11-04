import argparse
import json
from helpers import *
from puzzle import load_puzzles


def main(args):
    in_file, out_dir, dimensions = args.input_file, args.output, json.loads(args.dimensions)

    create_dir(out_dir)
    puzzles = load_puzzles(in_file, dimensions)

    for p in puzzles:
        print(p)

        # Print possible moves as Assignment desire
        print(list(map(lambda x: (x[0], p[x[1]]), p.get_moves())))

        # print(p.get_dimensions())
        # print(p.get_current_pos())
        print()

    # For testing
    # puzzles[0].solve(SearchType.Dijkstra)   # UCS


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Inject shape into aos-studio from a mesh directory.')

    arg_parser.add_argument('input_file', metavar='input_file', type=str,
                            help='Path to the puzzle(s) definition(s) file to use.')

    arg_parser.add_argument("-d", "--dimensions", metavar="<[width, height]>", type=str,
                            help="2D dimensions of the input puzzle. Default: [4, 2]",
                            default="[4, 2]")

    arg_parser.add_argument("-o", "--output", metavar="<output>", type=str,
                            help="Output directory relative to current working directory. Default: _out/",
                            default="_out/")

    args = arg_parser.parse_args()

    main(args)
