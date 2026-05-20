from __future__ import annotations

import random
import sys
from typing import Any

from display import display_maze
from maze_generator import MazeGenerator
from output import write_maze_file
from parse import read_config, parse_config, validator


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv
    validator(argv)

    config: dict[str, str] = read_config(argv[1])
    parsed: dict[str, Any] = parse_config(config)
    width: int = parsed['WIDTH']
    height: int = parsed['HEIGHT']
    entry: tuple[int, int] = parsed['ENTRY']
    exit_: tuple[int, int] = parsed['EXIT']
    output_file: str = parsed['OUTPUT_FILE']
    perfect: bool = parsed['PERFECT']

    gen_maze = MazeGenerator(width, height, random.randint(0, 100))
    gen_maze.embed_42(entry, exit_)
    gen_maze.generate(perfect)

    path: list[tuple[int, int]] | None = gen_maze.solve_bfs(entry, exit_)
    display_maze(gen_maze.grid, entry, exit_)
    display_maze(gen_maze.grid, entry, exit_, path)
    write_maze_file(gen_maze.grid, output_file, entry, exit_)


if __name__ == '__main__':
    main()
