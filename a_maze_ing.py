import sys
import os
from maze_generator import MazeGenerator
from display import display_maze
from parse import validator, read_config, parse_config

if __name__ == '__main__':
    validator(sys.argv)
    config = read_config(sys.argv[1])
    parsed = parse_config(config)


# 1. criar e gerar
    maze_test = MazeGenerator(10, 10, 100)
    maze_test.generate(True)
    os.system('cls' if os.name == 'nt' else 'clear')
    display_maze(maze_test.grid, (8, 0), (5, 5))
    input()
