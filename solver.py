from collections import deque

DIRS = {
    "N": ( 0, -1),
    "S": ( 0,  1),
    "E": ( 1,  0),
    "W": (-1,  0),
}


OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}


def solve_bfs(maze, entry, exit_):
    """
    Resolve o maze com BFS.
    Retorna a lista de células [(x,y), ...] do caminho,
    ou None se não houver solução.
    """
    queue   = deque([entry])
    visited = {entry}
    parent  = {entry: None}   

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