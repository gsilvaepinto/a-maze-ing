from __future__ import annotations

import random
import sys
from typing import Any
import os

from display import display_maze
from maze_generator import MazeGenerator
from output import write_maze_file
from parse import read_config, parse_config, validator


def print_menu():
    print(r"""
  #=======================================#
  #          A _ M a z e _ i n g          #
  #---------------------------------------#
  #                                       #
  #          [1]  Generate Maze           #
  #                                       #
  #          [2]  Solve Maze              #
  #                                       #
  #          [3]  Change Color            #
  #                                       #
  #          [4]  Quit                    #
  #                                       #
  #=======================================#
""")


def main() -> None:
    validator(sys.argv)
    config: dict[str, str] = read_config(sys.argv[1])
    parsed: dict[str, Any] = parse_config(config)

    width: int = parsed['WIDTH']
    height: int = parsed['HEIGHT']
    entry: tuple[int, int] = parsed['ENTRY']
    exit_: tuple[int, int] = parsed['EXIT']
    output_file: str = parsed['OUTPUT_FILE']
    perfect: bool = parsed['PERFECT']

    color = random.randint(0, 100)
    seed = random.randint(0, 100)
    gen_maze = MazeGenerator(width, height, seed)
    gen_maze.generate(perfect)
    gen_maze.embed_42(entry, exit_)
    path: list[tuple[int, int]] | None = gen_maze.solve_bfs(entry, exit_)
    display_maze(gen_maze.grid, entry, exit_, None, color)

    is_solved = False
    while (1):
        print_menu()
        option = input("Choose a option: ").strip()

        os.system('clear')
        if option == "1":
            seed = random.randint(0, 100)
            gen_maze = MazeGenerator(width, height, seed)
            gen_maze.generate(perfect)
            gen_maze.embed_42(entry, exit_)
            path = gen_maze.solve_bfs(entry, exit_)
            display_maze(gen_maze.grid, entry, exit_, None, color)
            is_solved = False
        elif option == "2":
            if is_solved:
                display_maze(gen_maze.grid, entry, exit_, None, color)
                is_solved = False
            else:
                display_maze(gen_maze.grid, entry, exit_, path, color)
                is_solved = True
        elif option == "3":
            color = random.randint(0, 100)
            display_maze(gen_maze.grid, entry, exit_, None, color)
        elif option == "4":
            print("\n  Goodbye!\n")
            break
        else:
            continue

        write_maze_file(gen_maze.grid, output_file, entry, exit_, path)


if __name__ == '__main__':
    main()
