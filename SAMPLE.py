import random

def generate_maze(maze):
    height = len(maze)
    width = len(maze[0])

    # começar no (0,0)
    x, y = 0, 0
    maze[y][x].visited = True

    stack = [(x, y)]

    while stack:
        x, y = stack[-1]

        # vizinhos não visitados
        neighbors = [
            (direction, nx, ny)
            for direction, nx, ny in get_neighbors(maze, x, y)
            if not maze[ny][nx].visited
        ]

        if neighbors:
            # escolhe um aleatório
            direction, nx, ny = random.choice(neighbors)

            current_cell = maze[y][x]
            next_cell = maze[ny][nx]

            # remove parede
            remove_walls(current_cell, next_cell, direction)

            # marca visitado
            next_cell.visited = True

            # avança
            stack.append((nx, ny))

        else:
            # voltar atrás
            stack.pop()
