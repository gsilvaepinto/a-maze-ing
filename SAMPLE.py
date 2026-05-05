import sys
import maze
from grid import create_maze, generate_maze
from output import write_maze_file
from display import display_maze


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    config = maze.read_config(config_file)
    parsed = maze.parse_config(config)

    grid = create_maze(parsed['WIDTH'], parsed['HEIGHT'])

    generate_maze(grid)

    display_maze(
        grid,
        parsed["ENTRY"],
        parsed["EXIT"]
    )

    write_maze_file(
        grid,
        parsed["OUTPUT_FILE"],
        parsed["ENTRY"],
        parsed["EXIT"]
    )