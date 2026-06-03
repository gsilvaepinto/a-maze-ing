from __future__ import annotations

import random
import sys
from typing import Any
import os

from display import display_maze
from maze_generator import MazeGenerator
from output import write_maze_file
from parse import read_config, parse_config, validator


def print_menu() -> None:
    """Print the interactive menu options."""
    print(r"""
  #=======================================#
  #          A _ M a z e _ i n g          #
  #---------------------------------------#
  #                                       #
  #          [1]  Generate Maze           #
  #                                       #
  #          [2]  Solve/Unsolve Maze      #
  #                                       #
  #          [3]  Change Color            #
  #                                       #
  #          [4]  Quit                    #
  #                                       #
  #=======================================#
""")


def clear() -> None:
    """Move terminal cursor to top-left without clearing the screen."""
    print("\033[H", end="", flush=True)


def main() -> None:
    """Parse config, generate the maze, and run the interactive loop."""
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
    os.system('clear')
    clear()
    while True:
        seed = random.randint(0, 99999999)
        gen_maze = MazeGenerator(width, height, seed)
        gen_maze.generate(perfect)
        success, error = gen_maze.embed_42(entry, exit_)
        path = gen_maze.solve_bfs(entry, exit_)
        if path is not None:
            break
    display_maze(gen_maze.grid, entry, exit_, None, color)
    try:
        is_solved = False
        while (1):
            print_menu()
            if not success and error is not None:
                print(error)
            option = input("\033[2K\rChoose a option: ").strip()

            if width > 16 or height > 16:
                os.system('clear')
            else:
                clear()

            if option == "1":
                while (1):
                    seed = random.randint(0, 99999999)
                    gen_maze = MazeGenerator(width, height, seed)
                    gen_maze.generate(perfect)
                    success, error = gen_maze.embed_42(entry, exit_)
                    path = gen_maze.solve_bfs(entry, exit_)
                    if path is not None:
                        if is_solved:
                            display_maze(gen_maze.grid, entry, exit_, path,
                                         color)
                        else:
                            display_maze(gen_maze.grid, entry, exit_, None,
                                         color)
                        break
            elif option == "2":
                if is_solved:
                    display_maze(gen_maze.grid, entry, exit_, None, color)
                    is_solved = False
                else:
                    display_maze(gen_maze.grid, entry, exit_, path, color)
                    is_solved = True
            elif option == "3":
                color = random.randint(0, 100)
                if is_solved:
                    display_maze(gen_maze.grid, entry, exit_, path,
                                 color)
                else:
                    display_maze(gen_maze.grid, entry, exit_, None,
                                 color)
            elif option == "4":
                os.system('clear')
                print("\n  Goodbye!\n")
                break
            else:
                if is_solved:
                    display_maze(gen_maze.grid, entry, exit_, path, color)
                else:
                    display_maze(gen_maze.grid, entry, exit_, None, color)

            write_maze_file(gen_maze.grid, output_file, entry, exit_, path)
    except KeyboardInterrupt:
        os.system('clear')
        print("You Exit the program")


if __name__ == '__main__':
    main()
