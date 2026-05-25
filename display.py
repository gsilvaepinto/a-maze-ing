from maze_generator import Cell
import random


RESET = "\033[0m"


class Color:
    WHITE = "\033[97m"
    RED = "\033[91m"
    PURPLE = "\033[95m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    ORANGE = "\033[33m"
    PINK = "\033[35m"
    DARK_RED = "\033[31m"
    DARK_GREEN = "\033[32m"
    DARK_BLUE = "\033[34m"
    DARK_CYAN = "\033[36m"
    BOLD_WHITE = "\033[1;97m"
    BOLD_RED = "\033[1;91m"
    BOLD_GREEN = "\033[1;92m"
    BOLD_YELLOW = "\033[1;93m"
    BOLD_BLUE = "\033[1;94m"
    BOLD_CYAN = "\033[1;96m"


def display_maze(
    maze: list[list[Cell]],
    entry: tuple[int, int] | None = None,
    exit_: tuple[int, int] | None = None,
    path: list[tuple[int, int]] | None = None,
    color_seed: int | None = None,
) -> None:
    if color_seed is not None:
        rng = random.Random(color_seed)

        color_palette = [
            Color.WHITE,
            Color.YELLOW,
            Color.CYAN,
            Color.GRAY,
            Color.GREEN,
            Color.BLUE,
            Color.ORANGE,
            Color.PINK,
            Color.DARK_RED,
            Color.DARK_GREEN,
            Color.DARK_BLUE,
            Color.DARK_CYAN,
            Color.BOLD_WHITE,
            Color.BOLD_GREEN,
            Color.BOLD_YELLOW,
            Color.BOLD_BLUE,
            Color.BOLD_CYAN,
        ]
        random_walls_color = rng.choice(color_palette)
        random_42_color = rng.choice(color_palette)

        W = random_walls_color + "██" + RESET
        S = "  "
    else:
        random_walls_color = Color.WHITE
        random_42_color = Color.YELLOW
        W = Color.WHITE
        S = "  "

    height = len(maze)
    width = len(maze[0])

    print(W * (width * 2 + 1))

    for y in range(height):

        mid = W
        for x in range(width):
            if (x, y) == entry:
                mid += Color.PURPLE + "██" + RESET
            elif (x, y) == exit_:
                mid += Color.RED + "██" + RESET
            elif maze[y][x].is_42:
                mid += random_42_color + "██" + RESET
            elif path and (x, y) in path:
                mid += Color.YELLOW + "✧ " + RESET
            else:
                mid += S

            mid += W if maze[y][x].walls["E"] else S

        print(mid)

        bot = W
        for x in range(width):
            bot += W if maze[y][x].walls["S"] else S
            bot += W
        print(bot)
