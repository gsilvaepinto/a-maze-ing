RESET  = "\033[0m"
WHITE  = "\033[97m"
RED    = "\033[91m"
PURPLE = "\033[95m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"

W = WHITE + "██" + RESET   
S = "  "                   


def display_maze(maze, entry=None, exit_=None, path=None):
    """
    Desenha o maze no terminal.
    - entry : (x, y) célula de entrada  → roxo
    - exit_ : (x, y) célula de saída   → vermelho
    - path  : list[(x,y)] solução BFS  → amarelo
    """
    path_set = set(path) if path else set()
    height   = len(maze)
    width    = len(maze[0])

    
    print(W * (width * 2 + 1))

    for y in range(height):
        
        mid = W
        for x in range(width):
            cell = maze[y][x]

            if (x, y) == entry:
                mid += PURPLE + "██" + RESET
            elif (x, y) == exit_:
                mid += RED + "██" + RESET
            elif (x, y) in path_set:
                mid += YELLOW + "✧ " + RESET
            else:
                mid += S

            mid += W if cell.walls["E"] else S

        print(mid)


        bot = W
        for x in range(width):
            cell = maze[y][x]
            bot += W if cell.walls["S"] else S
            bot += W   
        print(bot)
