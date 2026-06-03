from __future__ import annotations
import random
from collections import deque
from typing import Optional
import sys


class Cell:
    """Represents a single cell in the maze grid."""

    def __init__(self) -> None:
        """Initialize a cell with all four walls closed."""
        self.walls: dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
        self.visited: bool = False
        self.is_42: bool = False


class MazeGenerator:
    """Generates a maze using the recursive backtracker (DFS) algorithm."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Number of columns.
            height: Number of rows.
            seed: Optional random seed for reproducibility.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]
        if seed is not None:
            random.seed(seed)

    def _get_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        """Return valid cardinal neighbours as (direction, nx, ny) tuples."""
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
        """Remove the shared wall between two adjacent cells."""
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
        """Generate the maze using recursive backtracker (DFS).

        Args:
            perfect: If True, produces a perfect maze (one path between any two
                     cells). If False, extra walls are removed to create loops.
        """
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
        """Remove random walls to introduce loops and alternative paths.

        Args:
            count: Number of walls to remove.
        """
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

    def _path_exists(self,
                     entry: tuple[int, int],
                     exit_: tuple[int, int]) -> bool:
        """Return True if a path exists between entry and exit."""
        queue = deque([entry])
        visited = {entry}

        while queue:
            x, y = queue.popleft()
            if (x, y) == exit_:
                return True

            for direction, nx, ny in self._get_neighbors(x, y):
                if not self.grid[y][x].walls[direction]:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        return False

    def embed_42(self,
                 entry: tuple[int, int],
                 exit_: tuple[int, int]) -> tuple[bool, Optional[str]]:
        """Stamp the '42' pattern onto the maze as fully closed cells.

        Args:
            entry: Entry cell coordinates (x, y).
            exit_: Exit cell coordinates (x, y).

        Returns:
            Tuple of (success, error_message).
            error_message is None on success.
        """
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

        if self.width < 10 or self.height < 8:
            return (False, "Error: Maze too small for '42' pattern."
                    " Omitting pattern.")

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for nx, ny in offsets:
            sx, sy = start_x + nx, start_y + ny

            overlap = False
            for dx, dy in pattern:
                if (sx + dx, sy + dy) in [entry, exit_]:
                    overlap = True
                    break

            if not overlap:
                for dx, dy in pattern:
                    cx, cy = sx + dx, sy + dy
                    cell = self.grid[cy][cx]
                    cell.is_42 = True
                    cell.visited = True
                    cell.walls = {k: True for k in "NESW"}

                    if cy > 0:
                        self.grid[cy-1][cx].walls["S"] = True
                    if cy < self.height - 1:
                        self.grid[cy+1][cx].walls["N"] = True
                    if cx > 0:
                        self.grid[cy][cx-1].walls["E"] = True
                    if cx < self.width - 1:
                        self.grid[cy][cx+1].walls["W"] = True
                return (True, None)

        return (False, "Error: Could not find a safe spot for '42' pattern."
                " Omitting.")

    def _reconstruct_path(
        self,
        parent: dict[tuple[int, int], tuple[int, int] | None],
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Reconstruct the path from BFS parent map from start to end.

        Args:
            parent: Dict mapping each cell to its predecessor.
            end: The destination cell.

        Returns:
            List of (x, y) coordinates from start to end.
        """
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
        """Find the shortest path from entry to exit using BFS.

        Args:
            entry: Start cell coordinates (x, y).
            exit_: End cell coordinates (x, y).

        Returns:
            List of (x, y) tuples from entry to exit, or None if unreachable.
        """
        queue: deque[tuple[int, int]] = deque([entry])
        visited: set[tuple[int, int]] = {entry}
        parent: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == exit_:
                return self._reconstruct_path(parent, exit_)

            try:
                for direction, nx, ny in self._get_neighbors(x, y):
                    if self.grid[y][x].walls[direction]:
                        continue
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
            except (IndexError, KeyError):
                print("Error: Entry point out off Maze boundaries")
                sys.exit(1)
        return None
