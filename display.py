from mazegen.generator import MazeGenerator, N, E, S, W


def display(maze: MazeGenerator,
            show_path: bool = False,
            wall_color: str = "") -> None:
    """Print the maze in the terminal.

    Args:
        maze: a maze that was already generated.
        show_path: if True, draw the shortest path from entry to exit.
        wall_color: ANSI escape code used to color the walls.
    """

    path_cells: set[tuple[int, int]] = set()

    if show_path:
        path = maze.solve()
        x, y = maze.entry
        path_cells.add((x, y))
        for direction in path:
            if direction == "N":
                y -= 1
            elif direction == "E":
                x += 1
            elif direction == "S":
                y += 1
            else:
                x -= 1
            path_cells.add((x, y))

    reset = "\033[0m"
    corner = wall_color + "𖦹" + reset
    h_wall = wall_color + "═══" + reset
    v_wall = wall_color + "║" + reset

    for y in range(maze.height):
        line = ""

        for x in range(maze.width):
            line += corner

            if maze.grid[y][x] & (1 << N):
                line += h_wall
            elif (x, y) in path_cells and (x, y - 1) in path_cells:
                line += "\033[34m███\033[0m"
            else:
                line += "   "

        line += corner
        print(line)

        line = ""
        for x in range(maze.width):
            if maze.grid[y][x] & (1 << W):
                line += v_wall
            elif (x, y) in path_cells and (x - 1, y) in path_cells:
                line += "\033[34m█\033[0m"
            else:
                line += " "

            if (x, y) in maze.cells_42:
                line += "███"
            elif (x, y) == maze.entry:
                line += "\033[35m███\033[0m"
            elif (x, y) == maze.exit_:
                line += "\033[31m███\033[0m"
            elif (x, y) in path_cells:
                line += "\033[34m███\033[0m"
            else:
                line += "   "

        if maze.grid[y][maze.width - 1] & (1 << E):
            line += v_wall
        else:
            line += " "
        print(line)

    line = ""
    for x in range(maze.width):
        line += corner
        if maze.grid[maze.height - 1][x] & (1 << S):
            line += h_wall
        else:
            line += "   "
    line += corner
    print(line)
