from maze_generator import Cell


def cell_to_hex(cell: Cell) -> str:
    """Encode a cell's wall state as a single uppercase hex digit.

    Each bit represents a closed wall: bit 0 = N, 1 = E, 2 = S, 3 = W.

    Args:
        cell: The Cell to encode.

    Returns:
        A single uppercase hex character ('0'–'F').
    """
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


def write_maze_file(maze: list[list[Cell]], output_file: str,
                    entry: tuple[int, int],
                    exit: tuple[int, int],
                    path: list[tuple[int, int]] | None = None) -> None:
    """Write the maze to a file in hex format with entry, exit, and path.

    Args:
        maze: 2-D grid of Cell objects indexed as maze[y][x].
        output_file: Path to the output file.
        entry: Entry coordinates (x, y).
        exit: Exit coordinates (x, y).
        path: Solution path as a list of (x, y) tuples, or None.
    """
    with open(output_file, 'w') as file:
        for row in maze:
            line = ''
            for cell in row:
                line += cell_to_hex(cell)
            file.write(line + '\n')
        file.write('\n')
        file.write(f'{entry[0]},{entry[1]}\n')
        file.write(f'{exit[0]},{exit[1]}\n')

        if path:
            path_str = ""
            for i in range(len(path) - 1):
                curr_x, curr_y = path[i]
                next_x, next_y = path[i+1]

                if next_y < curr_y:
                    path_str += "N"
                elif next_y > curr_y:
                    path_str += "S"
                elif next_x > curr_x:
                    path_str += "E"
                elif next_x < curr_x:
                    path_str += "W"
            file.write(path_str + '\n')
