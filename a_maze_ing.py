import maze
import sys
from grid import create_maze, generate_maze

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    config_file = sys.argv[1]
    config = maze.read_config('config.txt')
    parsed = maze.parse_config(config)

    maze = create_maze(parsed['WIDTH'], parsed['HEIGHT'])
    # generate_maze(maze)
