*This project has been created as part of the 42 curriculum by tochaves, kbezerra.*

# A-Maze-ing

A maze generator written in Python. It reads a configuration file, generates a
random (but reproducible) maze, writes it to a file using a hexadecimal wall
encoding, and displays it in the terminal with an interactive menu.

## Description

**Goal.** Build a maze generator that is configurable, reproducible through a
seed, valid according to the subject, and reusable in future projects.

**Overview.**

- The maze is a grid of cells. Each cell has four walls (North, East, South,
  West) stored in a single integer.
- Two generation modes, chosen with the `PERFECT` key:
  - `PERFECT=True`: a *perfect* maze, with exactly one path between any two
    cells (no loops).
  - `PERFECT=False`: a *braided* maze, meant to be used as a Pac-Man-like
    board: fully connected, with several independent routes (loops), no open
    3x3 areas and no dead ends outside the "42" pattern.
- A closed "42" pattern is drawn in the middle of the maze with fully closed
  cells.
- The shortest path from the entry to the exit is computed and can be shown or
  hidden.
- The generation logic lives in a standalone module (`mazegen`) that can be
  reused and installed with `pip`.

## Instructions

**Requirements.** Python 3.10 or later. The program only uses the standard
library. `flake8` and `mypy` are needed for the linting rules.

**Installation.**

```bash
make install
```

**Execution.**

```bash
make run
# or, directly:
python3 a_maze_ing.py config.txt
```

The only argument is the configuration file. Any invalid configuration
(missing file, bad syntax, impossible parameters) prints a clear error message
and exits without crashing.

**Interactive menu.** After the maze is generated and written to the output
file, the menu offers:

| Option | Action |
|---|---|
| 1 | Re-generate a new maze (new random seed) and rewrite the output file |
| 2 | Show / hide the shortest path from the entry to the exit |
| 3 | Rotate the wall colours |
| 4 | Quit |

In the display, the entry is drawn in magenta, the exit in red, the path in
blue and the "42" pattern as solid blocks.

**Other Makefile rules.**

| Rule | Description |
|---|---|
| `make debug` | Run the program under Python's debugger (`pdb`), see the next section |
| `make lint` | Run `flake8` and `mypy` with the flags required by the subject |
| `make lint-strict` | Run `flake8` and `mypy --strict` (optional, stricter type checking) |
| `make clean` | Remove `__pycache__` folders and the `.mypy_cache` folder |

## Debugging with `make debug`

`make debug` runs the program under Python's debugger. `pdb` stops on the
first line and waits for commands at the `(Pdb)` prompt, so the program can be
executed step by step and its variables can be inspected. The interactive
menu also reads from the terminal, so when the program waits for `Choice?`
just type the option as usual.

| Command | Action |
|---|---|
| `n` | Execute the next line (does not enter functions) |
| `s` | Execute the next line, entering the function if there is a call |
| `c` | Continue until the next breakpoint (or the end of the program) |
| `b file:line` | Set a breakpoint (`b file:line, condition` for a conditional one) |
| `l` / `ll` | Show the code around the current line / of the whole current function |
| `p expr` / `pp expr` | Print / pretty-print the value of an expression |
| `w` | Show the call stack (where we are and who called this function) |
| `r` | Continue until the current function returns |
| `q` | Quit the debugger |

Pressing `Enter` repeats the last command. Breakpoints need a line number,
which changes whenever the code changes, so look it up first in another
terminal with `grep -n` and use it in place of `<line>` below.

**Example 1: check the parsed configuration.**

```
$ grep -n "maze = build_maze" a_maze_ing.py
$ make debug
(Pdb) b a_maze_ing.py:<line>
(Pdb) c
(Pdb) pp config
{'ENTRY': (0, 0),
 'EXIT': (19, 14),
 'HEIGHT': 15,
 'OUTPUT_FILE': 'maze.txt',
 'PERFECT': True,
 'SEED': 42,
 'WIDTH': 20}
(Pdb) p type(config["WIDTH"])
<class 'int'>
```

The values are already converted by the parser (integers, tuples and a
boolean), not strings.

**Example 2: follow the generation algorithm step by step.** Stop on the line
of the `while len(stack) > 0:` loop that decides whether to advance or to
backtrack.

```
$ grep -n "if len(options) > 0" mazegen/generator.py
$ make debug
(Pdb) b mazegen/generator.py:<line>
(Pdb) c
(Pdb) p (x, y)
(Pdb) p options
(Pdb) p stack
(Pdb) c
```

Each `c` runs one more iteration of the loop. `(x, y)` is the cell being
visited, `options` are the directions towards unvisited neighbours, and
`stack` is the current path. The stack grows when the algorithm advances and
shrinks when `options` is empty and it backtracks.

**Example 3: check that the exit was reached by the shortest-path search.**

```
$ grep -n "if self.exit_ not in came_from" mazegen/generator.py
$ make debug
(Pdb) b mazegen/generator.py:<line>
(Pdb) c
(Pdb) p self.exit_
(Pdb) p len(came_from)
(Pdb) p self.exit_ in came_from
True
```

`came_from` stores, for every cell discovered by the search, the cell it came
from and the direction used. If the exit is in it, the path can be rebuilt.

**Example 4: watch the braiding open a dead end** (set `PERFECT=False` in the
configuration first).

```
$ grep -n "old_a = self.grid" mazegen/generator.py
$ make debug
(Pdb) b mazegen/generator.py:<line>
(Pdb) c
(Pdb) p (x, y)
(Pdb) p self.count_walls(x, y)
3
(Pdb) p direction
(Pdb) n
(Pdb) n
(Pdb) n
(Pdb) p self.has_open_3x3()
```

The cell `(x, y)` is a dead end (three closed walls). After the lines that
open the wall have run, `has_open_3x3()` tells whether the opening created a
forbidden 3x3 area, in which case the wall is restored.

## Configuration file

One `KEY=VALUE` pair per line. Empty lines and lines starting with `#` are
ignored, and spaces around the key and the value are trimmed.

| Key | Required | Description | Example |
|---|---|---|---|
| `WIDTH` | yes | Maze width in cells (integer greater than 0) | `WIDTH=20` |
| `HEIGHT` | yes | Maze height in cells (integer greater than 0) | `HEIGHT=15` |
| `ENTRY` | yes | Entry coordinates `x,y` (inside the maze) | `ENTRY=0,0` |
| `EXIT` | yes | Exit coordinates `x,y` (inside the maze, different from the entry) | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Name of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True` or `False` | `PERFECT=True` |
| `SEED` | no | Integer seed. Without it, every run gives a different maze | `SEED=42` |

Default configuration (`config.txt`):

```
# Maze width (number of cells)
WIDTH=20

# Maze height
HEIGHT=15

# Entry coordinates (x,y)
ENTRY=0,0

# Exit coordinates (x,y)
EXIT=19,14

# Output filename
OUTPUT_FILE=maze.txt

# Is the maze perfect?
PERFECT=True

# The maze seed
SEED=42
```

Coordinates are `(x, y)`: `x` is the column and `y` is the row, with `(0, 0)`
in the top-left corner. The parser rejects: lines without `=`, missing
mandatory keys, non-integer numbers, coordinates that do not have exactly two
values, an entry or exit outside the maze, an entry equal to the exit, and a
`PERFECT` value that is not `True` or `False`.

**The "42" pattern** needs a maze of at least 10x7 cells. In a smaller maze
the pattern is omitted and an error message is printed. If the entry or the
exit falls inside the pattern, the pattern is also omitted and a message is
printed.

## Output file format

Each cell is written as one hexadecimal digit. A bit set to `1` means the wall
is closed:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

For example `D` (`1101`) is a cell with the North, South and West walls closed
and the East wall open. A cell of the "42" pattern is `F` (all walls closed).

The file contains one row of digits per line, then an empty line, then the
entry coordinates, the exit coordinates and the shortest path using the
letters `N`, `E`, `S`, `W`. All lines end with `\n`.

## Algorithms

**Generation: recursive backtracker (depth-first search).** Every cell starts
with its four walls closed. Starting from the entry, the algorithm keeps a
stack with the current path:

1. Look at the cell on top of the stack and list its neighbours that are inside
   the maze and not yet visited.
2. If there is at least one, pick one at random (with the seeded generator),
   open the wall between the two cells, mark the new cell as visited and push
   it on the stack.
3. If there is none, pop the stack (backtrack).
4. Stop when the stack is empty.

The cells of the "42" pattern are marked as visited before the algorithm
starts, so it never enters them and they stay fully closed.

**Braiding (only with `PERFECT=False`).** After the depth-first search, the
maze is still perfect and full of dead ends. For each dead end (a cell with
three closed walls) the algorithm tries to open one of its closed walls
towards a neighbour that is inside the maze and is not part of the "42". After
each attempt, it checks that no fully open 3x3 area was created, and if one was
created the wall is restored and another candidate is tried. This creates
loops and removes the dead ends.

**Solving: breadth-first search (BFS).** The shortest path is found by
exploring the maze layer by layer from the entry, storing for each discovered
cell where it came from, and rebuilding the path backwards from the exit. BFS
is used because it always returns the shortest path, including in non-perfect
mazes where several paths exist.

**Why these algorithms.**

- The recursive backtracker is simple to implement and to explain, it needs no
  extra data structure beyond a stack, and it produces a connected perfect
  maze by construction (a spanning tree of the grid): no loops, no isolated
  cells and no open 3x3 areas.
- It is fully reproducible: the same seed, size and configuration always give
  the same maze.
- Marking the "42" cells as visited integrates the pattern without any special
  case in the algorithm.
- Braiding reuses the same wall-opening function, keeps the maze connected
  (walls are only removed, never added) and never creates new dead ends.
- BFS guarantees the shortest path and keeps working when the maze has loops.

## Reusable module

The generation logic is in `mazegen/generator.py`, in the class
`MazeGenerator`. It does not depend on the display, the configuration parser
or the output writer, so it can be imported on its own.

**Basic example.**

```python
from mazegen.generator import MazeGenerator, N, E, S, W

maze = MazeGenerator(20, 15, (0, 0), (19, 14), perfect=True, seed=42)
maze.generate()

print(maze.solve())              # shortest path, for example "SSEENE..."
print(maze.grid[0][0])           # integer encoding the walls of cell (0, 0)
print(bool(maze.grid[0][0] & (1 << N)))   # is there a wall to the north?
```

**Custom parameters.**

| Parameter | Description |
|---|---|
| `width`, `height` | Size of the maze in cells |
| `entry`, `exit_` | `(x, y)` tuples, inside the maze and different from each other |
| `perfect` | `True` for a perfect maze, `False` for a braided maze (default `True`) |
| `seed` | Integer seed for reproducibility, or `None` for a different maze each time |

**Accessing the result.**

- `maze.grid`: list of rows (`grid[y][x]`). Each value is an integer from 0 to
  15 whose bits are the closed walls (`N=0, E=1, S=2, W=3`). The constants
  `N`, `E`, `S`, `W` are exported by the module.
- `maze.entry` and `maze.exit_`: the entry and exit coordinates.
- `maze.cells_42`: list of the `(x, y)` cells of the "42" pattern (empty if the
  maze is too small).
- `maze.solve()`: shortest path from the entry to the exit as a string of
  `N`, `E`, `S`, `W` letters. It returns an empty string if the exit cannot be
  reached. It only reads the grid and never modifies it.

Note: call `generate()` once per object. To get a new maze, create a new
`MazeGenerator` (the grid is not reset between calls).

**Building and installing the package.**

```bash
python3 -m venv venv
source venv/bin/activate
pip install build
python3 -m build
```

The built package (`mazegen-1.0.0-py3-none-any.whl`) is available at the root
of the repository. The license that allows reusing and distributing the
generator is in `LICENSE.md`.

## Project structure

```
.
├── a_maze_ing.py        main program and interactive menu
├── config.txt           default configuration
├── config_parser.py     reads and validates the configuration file
├── display.py           terminal rendering (walls, entry, exit, path, colours)
├── output_writer.py     writes the output file
├── mazegen/
│   ├── __init__.py
│   └── generator.py     MazeGenerator (reusable module)
├── Makefile
├── pyproject.toml
└── README.md
```

## Features

- Seeded, reproducible generation.
- Perfect and braided (non-perfect) modes.
- **Bonus:** the default (non-perfect) maze has no dead ends outside the "42"
  pattern, confirmed with the provided analysis script using
  `--max-dead-ends 0`.
- Closed "42" pattern drawn with fully closed cells.
- Interactive terminal menu: regenerate, show/hide the path, change the wall
  colours.
- Strict configuration validation with clear error messages.
- Type hints on all functions, checked with `mypy`, and `flake8` compliance.

## Team and project management

**Roles.**

- `tochaves`: maze generator (`MazeGenerator`: generation, "42" pattern,
  shortest path, braiding), configuration parser, output writer, main program
  and menu, Makefile.
- `kbezerra`: terminal display (rendering of walls, entry, exit and path,
  colours), the BFS algorithm (`solve`) and `config.txt`.

**Planning and how it evolved.**

We planned to build the project from the inside out: first the generator and
the wall encoding, then the shortest path, then the output file, the
configuration parser and the display, and finally the non-perfect mode and
the interactive menu. The main change along the way was separating the display
from the generator: the first version printed the maze from inside the class,
and we moved it to its own module so that the generator stays reusable and
independent. The non-perfect mode was the last and hardest part, and it was
developed on top of an already working perfect maze.

**What worked well.**

- Agreeing early on the interface of `MazeGenerator` (`grid`, `entry`,
  `exit_`, `cells_42`, `solve()`), which let us work in parallel.
- Testing each step with small hand-made grids before using it in the full
  program.
- Reviewing each other's code, so that both of us can explain the whole
  project.

**What could be improved.**

- Writing automated tests earlier instead of only checking visually.
- Adding a second generation algorithm (a possible extension is a randomized
  Prim) and an animation of the generation.

**Tools used.** Git, Make, `flake8`, `mypy`, Python's debugger (`pdb`),
virtual environments, the analysis script provided with the subject, and
Claude as an AI assistant (see below).

## Resources

**Mazes, graphs and algorithms.**

- [Maze generation algorithms (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Maze Generation: Recursive Backtracking, Jamis Buck](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Maze Generation Algorithm Recap, Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Spanning tree (Wikipedia)](https://en.wikipedia.org/wiki/Spanning_tree): a perfect maze is a spanning tree of the grid
- [Depth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search)

**Bits, masks and hexadecimal.**

- [Bitwise operation (Wikipedia)](https://en.wikipedia.org/wiki/Bitwise_operation)
- [Mask (computing) (Wikipedia)](https://en.wikipedia.org/wiki/Mask_(computing))
- [Hexadecimal (Wikipedia)](https://en.wikipedia.org/wiki/Hexadecimal)
- [Bitwise operations on integer types (Python docs)](https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types)
- [Python BitManipulation (Python wiki)](https://wiki.python.org/moin/BitManipulation)

**Python.**

- [`random` module (seeds and reproducibility)](https://docs.python.org/3/library/random.html)
- [`typing` module (type hints)](https://docs.python.org/3/library/typing.html)
- [Errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Reading and writing files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Modules and packages](https://docs.python.org/3/tutorial/modules.html)
- [`sys.argv` (command-line arguments)](https://docs.python.org/3/library/sys.html#sys.argv)
- [ANSI escape codes (Wikipedia)](https://en.wikipedia.org/wiki/ANSI_escape_code): used for the colours in the terminal

**Tools and standards.**

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [`pdb`, the Python debugger](https://docs.python.org/3/library/pdb.html)
- [GNU Make manual](https://www.gnu.org/software/make/manual/make.html)
- [Python Packaging User Guide](https://packaging.python.org/)

**Use of AI.** We used Claude as a tutor and code reviewer. It helped us
understand the concepts behind the project (graphs, depth-first and
breadth-first search, bitwise operations), plan each step, review our code and
spot bugs and style problems, and draft the Makefile and this README. We wrote
the code ourselves, adapted the few snippets it suggested, tested everything,
and we can explain every part of it.
