from __future__ import annotations
import random
from collections import deque
from typing import Optional
import sys


class Cell:
    def __init__(self) -> None:
        self.walls: dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
        self.visited: bool = False
        self.is_42: bool = False


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]
        if seed is not None:
            random.seed(seed)

    def _get_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        neighbors: list[tuple[str, int, int]] = []
        if y > 0:
            neighbors.append(("N", x, y - 1))
        if y < self.height - 1:
            neighbors.append(("S", x, y + 1))
        if x > 0:
            neighbors.append(("W", x - 1, y))
        if x < self.width - 1:
            neighbors.append(("E", x + 1, y))
        return neighbors

    def _remove_walls(
        self,
        current_cell: Cell,
        next_cell: Cell,
        direction: str,
    ) -> None:
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

    def generate(self, perfect: bool = True) -> None:

        x, y = 0, 0
        self.grid[y][x].visited = True
        stack: list[tuple[int, int]] = [(x, y)]

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
            self.non_perfect_maze(self.width // 2)

    def non_perfect_maze(self, count: int) -> None:
        removed = 0
        attempts = 0
        max_attempts = count * 10

        while removed < count and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.grid[y][x].is_42:
                continue

            neighbors = self._get_neighbors(x, y)
            direction, nx, ny = random.choice(neighbors)

            if self.grid[ny][nx].is_42:
                continue

            if not self.grid[y][x].walls[direction]:
                continue

            self._remove_walls(self.grid[y][x], self.grid[ny][nx], direction)
            removed += 1

    def embed_42(self, entry: tuple[int, int], exit_: tuple[int, int]) -> bool:
        # 1. Define the pattern (7x5 area)
        pattern = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (6, 2),
            (5, 2),
            (4, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        ]

        # 2. MANDATORY SIZE CHECK
        if self.width < 10 or self.height < 8:
            print("Error: Maze too small for '42' pattern. Omitting pattern.")
            return False

        # 3. Centering Logic
        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        # 4. Safety Nudge (if it hits entry/exit)
        offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for nx, ny in offsets:
            sx, sy = start_x + nx, start_y + ny

            # Check if this position overlaps entry or exit
            overlap = False
            for dx, dy in pattern:
                if (sx + dx, sy + dy) in [entry, exit_]:
                    overlap = True
                    break

            if not overlap:
                # 5. Stamp the pattern
                for dx, dy in pattern:
                    cx, cy = sx + dx, sy + dy
                    cell = self.grid[cy][cx]
                    cell.is_42 = True
                    cell.visited = True
                    cell.walls = {k: True for k in "NESW"}

                    # 6. COHERENCY: Close neighbor walls
                    if cy > 0:
                        self.grid[cy-1][cx].walls["S"] = True
                    if cy < self.height - 1:
                        self.grid[cy+1][cx].walls["N"] = True
                    if cx > 0:
                        self.grid[cy][cx-1].walls["E"] = True
                    if cx < self.width - 1:
                        self.grid[cy][cx+1].walls["W"] = True
                return True

        print("Error: Could not find a safe spot for '42' pattern. Omitting.")
        return False

    def _reconstruct_path(
        self,
        parent: dict[tuple[int, int], tuple[int, int] | None],
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = end
        while current is not None:
            path.append(current)
            current = parent[current]
        return path[::-1]  # Reverse to go from Start -> End

    def solve_bfs(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> list[tuple[int, int]] | None:
        queue: deque[tuple[int, int]] = deque([entry])
        visited: set[tuple[int, int]] = {entry}
        parent: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == exit_:
                return self._reconstruct_path(parent, exit_)

            # Use your existing helper!
            # It returns a list of (direction, nx, ny)
            try:
                for direction, nx, ny in self._get_neighbors(x, y):
                    # 1. Check if there is a wall in that direction
                    if self.grid[y][x].walls[direction]:
                        continue
                # 2. Check if we've already been to this neighbor
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
            except (IndexError, KeyError):
                print("Error: Entry point out off Maze boundaries")
                sys.exit(1)
        return None
