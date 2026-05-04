RESET = "\033[0m"
WHITE = "\033[97m"
RED = "\033[91m"
PURPLE = "\033[95m"


def display_maze(maze, entry=None, exit_=None):
    WALL = WHITE + "██" + RESET
    SPACE = "  "

    width = len(maze[0])

    print(WALL * (width * 2 + 1))

    for y, row in enumerate(maze):
        middle = WALL
        bottom = WALL

        for x, cell in enumerate(row):

            if entry == (x, y):
                content = PURPLE + "██" + RESET
            elif exit_ == (x, y):
                content = RED + "██" + RESET
            else:
                content = SPACE

            middle += content

            if cell.walls["E"]:
                middle += WALL
            else:
                middle += SPACE

            if cell.walls["S"]:
                bottom += WALL + WALL
            else:
                bottom += SPACE + WALL

        print(middle)
        print(bottom)