# code from a_maze_ing.py

import sys
import maze
from grid import create_maze, generate_maze
from output import write_maze_file
from display import display_maze
from solver import solve_bfs


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 main.py config.txt")
        sys.exit(1)

    config  = maze.read_config(sys.argv[1])
    parsed  = maze.parse_config(config)

    entry  = parsed["ENTRY"]
    exit_  = parsed["EXIT"]

    # 1. criar e gerar
    grid = create_maze(parsed["WIDTH"], parsed["HEIGHT"])
    generate_maze(grid)

    # 2. mostrar maze sem solução
    print("\n=== MAZE ===")
    display_maze(grid, entry, exit_)

    # 3. resolver com BFS
    path = solve_bfs(grid, entry, exit_)

    if path:
        display_maze(grid, entry, exit_, path=path)
    else:
        print("\nSem solução encontrada.")

    # 4. escrever ficheiro
    write_maze_file(grid, parsed["OUTPUT_FILE"], entry, exit_)

    # the config file

WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=4,4
OUTPUT_FILE=maze.txt
PERFECT=True


# code from display.py

RESET = "\033[0m"
WHITE = "\033[97m"
RED = "\033[91m"
PURPLE = "\033[95m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

W = WHITE + "██" + RESET
S = "  "


def display_maze(maze, entry=None, exit_=None, path=None):
    """
    Desenha o maze no terminal.
    - entry : (x, y) célula de entrada  → roxo
    - exit_ : (x, y) célula de saída   → vermelho
    - path  : list[(x,y)] solução BFS  → amarelo
    """
    path_set = set(path) if path else set()
    height = len(maze)
    width = len(maze[0])

    print(W * (width * 2 + 1))

    for y in range(height):

        mid = W
        for x in range(width):
            cell = maze[y][x]

            if (x, y) == entry:
                mid += PURPLE + "██" + RESET
            elif (x, y) == exit_:
                mid += RED + "██" + RESET
            elif (x, y) in path_set:
                mid += YELLOW + "✧ " + RESET
            else:
                mid += S

            mid += W if cell.walls["E"] else S

        print(mid)

        bot = W
        for x in range(width):
            cell = maze[y][x]
            bot += W if cell.walls["S"] else S
            bot += W
        print(bot)

# code from grid.py


import random


class Cell:
    def __init__(self):
        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True
        }
        self.visited = False


def create_maze(width: int, height: int):
    return [[Cell() for _ in range(width)] for _ in range(height)]


def get_neighbors(maze, x, y):
    neighbors = []
    if y > 0:
        neighbors.append(("N", x, y - 1))
    if y < len(maze) - 1:
        neighbors.append(("S", x, y + 1))
    if x > 0:
        neighbors.append(("W", x - 1, y))
    if x < len(maze[0]) - 1:
        neighbors.append(("E", x + 1, y))
    return neighbors


def generate_maze(maze):
    height = len(maze)
    width = len(maze[0])

    x, y = 0, 0
    maze[y][x].visited = True

    stack = [(x, y)]

    while stack:
        x, y = stack[-1]

        neighbors = [
            (direction, nx, ny)
            for direction, nx, ny in get_neighbors(maze, x, y)
            if not maze[ny][nx].visited
        ]

        if neighbors:

            direction, nx, ny = random.choice(neighbors)

            current_cell = maze[y][x]
            next_cell = maze[ny][nx]

            remove_walls(current_cell, next_cell, direction)

            next_cell.visited = True

            stack.append((nx, ny))

        else:
            stack.pop()


def remove_walls(current, next_cell, direction):
    if direction == "N":
        current.walls["N"] = False
        next_cell.walls["S"] = False
    elif direction == "S":
        current.walls["S"] = False
        next_cell.walls["N"] = False
    elif direction == "E":
        current.walls["E"] = False
        next_cell.walls["W"] = False
    elif direction == "W":
        current.walls["W"] = False
        next_cell.walls["E"] = False


# code from maze.py

def read_config(file_path) -> dict:
    config = {}
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()
    return config


def parse_coordinates(value: str) -> tuple[int, int]:
    x, y = value.split(',')
    return int(x), int(y)


def parse_config(config: dict) -> dict:
    parsed = {}

    parsed['WIDTH'] = int(config['WIDTH'])
    parsed['HEIGHT'] = int(config['HEIGHT'])
    parsed['ENTRY'] = parse_coordinates(config['ENTRY'])
    parsed['EXIT'] = parse_coordinates(config['EXIT'])
    parsed["OUTPUT_FILE"] = config["OUTPUT_FILE"]
    parsed["PERFECT"] = config["PERFECT"] == "True"

    return parsed


# code from output.py

def cell_to_hex(cell) -> str:
    value = 0

    if cell.walls['N']:
        value += 1
    if cell.walls['E']:
        value += 2
    if cell.walls['S']:
        value += 4
    if cell.walls['W']:
        value += 8
    return format(value, 'X')


def write_maze_file(maze, output_file: str, entry: tuple[int, int], exit: tuple[int, int]) -> None:
    with open(output_file, 'w') as file:
        for row in maze:
            line = ''
            for cell in row:
                line += cell_to_hex(cell)
            file.write(line + '\n')
        file.write('\n')
        file.write(f'{entry[0]},{entry[1]}\n')
        file.write(f'{exit[0]},{exit[1]}\n')
        file.write('\n') # ADD PATH


# code from solver


from collections import deque

DIRS = {
    "N": (0, -1),
    "S": (0,  1),
    "E": (1,  0),
    "W": (-1,  0),
}


OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}


def solve_bfs(maze, entry, exit_):
    """
    Resolve o maze com BFS.
    Retorna a lista de células [(x,y), ...] do caminho,
    ou None se não houver solução.
    """
    queue = deque([entry])
    visited = {entry}
    parent = {entry: None}

    while queue:
        x, y = queue.popleft()

        if (x, y) == exit_:
            return _reconstruct(parent, exit_)

        for direction, (dx, dy) in DIRS.items():
            cell = maze[y][x]

            if cell.walls[direction]:
                continue

            nx, ny = x + dx, y + dy

            if not (0 <= nx < len(maze[0]) and 0 <= ny < len(maze)):
                continue

            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return None


def _reconstruct(parent, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path
