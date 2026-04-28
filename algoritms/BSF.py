def get_neighbors(current_cell, maze):
    row, col = current_cell
    results = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]):

            if maze[r][c] == 0:
                results.append((r, c))     
    return results


def recontruct_path(parent_map, start_pos, exit_pos):
    path = []
    current = exit_pos

    while current != start_pos:
        path.append(current)
        current = parent_map[current]
    path.append(start_pos)
    path.reverse()
    return path


def solve_maze(maze, start_pos, exit_pos):
    queue = []
    visited = set()
    parent_map = {}

    queue.append(start_pos)
    visited.add(start_pos)

    while queue:
        current_cell = queue.pop(0)

        if current_cell == exit_pos:
            return recontruct_path(parent_map, start_pos, exit_pos)

        for neighbor in get_neighbors(current_cell, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent_map[neighbor] = current_cell

    return None
