*This project has been created as part of the 42 curriculum by rparreir, guilheda.*

# A-Maze-ing

## Description

A Python maze generator that reads a configuration file, generates a maze (perfect or imperfect), displays it in the terminal with colours, and writes the result to a hex-encoded output file. The maze always contains a visible **"42"** pattern and a solvable path from entry to exit.

## Instructions

### Install dependencies
```
make install
```

### Run
```
make run
```
Or directly:
```
python3 a_maze_ing.py config.txt
```

### Debug
```
make debug
```

### Lint
```
make lint
```

### Clean
```
make clean
```

## Configuration File

One `KEY=VALUE` pair per line. Lines starting with `#` are ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` for a perfect maze | `PERFECT=True` |

## Algorithm

The maze uses the **recursive backtracker (DFS)** algorithm:

1. Start at cell `(0, 0)`, mark it visited.
2. Randomly pick an unvisited neighbour, remove the shared wall, move to it.
3. If no unvisited neighbours remain, backtrack.
4. Repeat until all cells are visited.

For `PERFECT=False`, a number of extra walls are removed after generation to create loops and multiple paths.

**Why this algorithm?** It is simple to implement, naturally produces perfect mazes (spanning tree), generates long winding corridors, and integrates cleanly with BFS for solving.

## Reusable Module

`MazeGenerator` lives in `maze_generator.py` and can be imported independently:

```python
from maze_generator import MazeGenerator

# Instantiate
gen = MazeGenerator(width=20, height=15, seed=42)

# Generate
gen.generate(perfect=True)

# Access the grid: grid[y][x] returns a Cell with .walls dict and .is_42 flag
grid = gen.grid

# Solve: returns a list of (x, y) tuples or None
path = gen.solve_bfs(entry=(0, 0), exit_=(19, 14))
```

The package `mazegen-1.0.0-py3-none-any.whl` at the root of the repository can be installed with:
```
pip install mazegen-1.0.0-py3-none-any.whl
```

To rebuild the package from source:
```
pip install build
python -m build
```

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [BFS shortest path — GeeksForGeeks](https://www.geeksforgeeks.org/shortest-path-unweighted-graph/)
- [Python type hints — mypy docs](https://mypy.readthedocs.io/en/stable/)
- [flake8 style guide](https://flake8.pycqa.org/en/latest/)

### AI Usage

AI (Claude) was used for:
- Reviewing the output file hex format against the subject specification.
- Suggesting improvements to type hints and error handling.
- Generating the README structure.

All AI-generated content was reviewed, tested, and understood before inclusion.

## Team & Project Management

**Team:** Solo — `<your-login>`

**Roles:** Full implementation (generation, display, parsing, output, solving).

**Planning:**
- Phase 1: Maze generation algorithm and coherent wall structure.
- Phase 2: Config parser, output file format, BFS solver.
- Phase 3: Terminal display, interactive menu, "42" pattern.
- Phase 4: Type hints, docstrings, linting, packaging.

**What worked well:** DFS backtracker was straightforward; BFS integration was natural.

**What could be improved:** More granular error messages for edge-case config inputs.

**Tools used:** VS Code, Git, mypy, flake8, Python 3.13.
