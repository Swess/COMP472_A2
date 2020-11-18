[Github Repo](https://github.com/Swess/COMP472_A2)

# COMP 472 - Assignment 2
**Author:** Isaac Doré - 40043159

# Dependencies
To run the code, the requirements first needs to be installed.
If you are using a Virtual Environment (venv), activate it first.
Regardless if you are using a python Virtual Environment or not, you can install the project dependencies like so:
```
pip install -r requirements.txt
```

# Executing
At any moment you can have the command-line help by typing: `python main.py -h`

```
usage: main.py [-h] [-g GENERATE] [-d <[width, height]>] [-o <output>] input_file

Solves given X-Puzzle with different solvers.

positional arguments:
  input_file            Path to the puzzle(s) definition(s) file to use.

optional arguments:
  -h, --help            show this help message and exit
  -g GENERATE, --generate GENERATE
                        If this flag is set, N random puzzles with given dimension will be generated in ./generated_puzzles.txt before anything else.
  -d <[width, height]>, --dimensions <[width, height]>
                        2D dimensions of the input puzzle. Default: [4, 2]
  -o <output>, --output <output>
                        Output directory relative to current working directory. Default: _out/
```

Solve the input file with `python main.py _relative_filepath_`. If the dimensions are different than [4, 2], add the `-d` option with the dimension in the required format.