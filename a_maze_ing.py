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