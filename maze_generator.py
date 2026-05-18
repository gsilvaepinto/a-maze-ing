import random
from collections import deque


class Cell:
    def __init__(self):
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int = False):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        if seed is not None:
            random.seed(seed)

    def _get_neighbors(self, x, y):
        neighbors = []
        if y > 0:
            neighbors.append(("N", x, y - 1))
        if y < self.height - 1:
            neighbors.append(("S", x, y + 1))
        if x > 0:
            neighbors.append(("W", x - 1, y))
        if x < self.width - 1:
            neighbors.append(("E", x + 1, y))
        return neighbors

    def _remove_walls(self, current_cell, next_cell, direction):
        if direction == "N":
            current_cell.walls["N"] = False
            next_cell.walls["S"] = False
        elif direction == "S":
            current_cell.walls["S"] = False
            next_cell.walls["N"] = False
        elif direction == "E":
            current_cell.walls["E"] = False
            next_cell.walls["W"] = False
        elif direction == "W":
            current_cell.walls["W"] = False
            next_cell.walls["E"] = False

    def generate(self, perfect: bool = True):

        for row in self.grid:
            for cell in row:
                cell.visited = False

        x, y = 0, 0
        self.grid[y][x].visited = True
        stack = [(x, y)]

        while stack:
            x, y = stack[-1]
            unvisited_neighbors = [
                (direction, nx, ny)
                for direction, nx, ny in self._get_neighbors(x, y)
                if not self.grid[ny][nx].visited
            ]
            if unvisited_neighbors:
                direction, nx, ny = random.choice(unvisited_neighbors)
                current_cell = self.grid[y][x]
                next_cell = self.grid[ny][nx]
                self._remove_walls(current_cell, next_cell, direction)
                next_cell.visited = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not perfect:
            pass
            # self.non_perfect_maze()

    def non_perfect_maze(self):
        for row in self.grid:
            direction, nx, ny = random.choice(self.unvisited_neighbors)
            current_cell = self.grid[y][x]
            next_cell = self.grid[ny][nx]
            if random() < 10:
                self._remove_walls(current_cell, next_cell, direction)