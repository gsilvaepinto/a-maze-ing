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
    x, y = 0, 0
    maze[y][x].visited = True

    neighbors = get_neighbors(maze, x, y)
    if neighbors:
        direction, nx, ny = random.choice(neighbors)
        current_cell = maze[y][x]
        next_cell = maze[ny][nx]
        remove_walls(current_cell, next_cell, direction)
        x, y = nx, ny
        maze[y][x].visited = True
        print("Nova posição:", x, y)


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