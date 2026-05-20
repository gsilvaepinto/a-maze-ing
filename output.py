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


def write_maze_file(maze, output_file: str, entry: tuple[int, int],
                    exit: tuple[int, int]) -> None:
    with open(output_file, 'w') as file:
        for row in maze:
            line = ''
            for cell in row:
                line += cell_to_hex(cell)
            file.write(line + '\n')
        file.write('\n')
        file.write(f'{entry[0]},{entry[1]}\n')
        file.write(f'{exit[0]},{exit[1]}\n')
        file.write('\n')  # ADD PATH
