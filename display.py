from mazegen.generator import MazeGenerator, N, E, S, W


def display(maze: MazeGenerator) -> None:
    path = maze.solve()
    path_cells = set()

    if path or maze.entry == maze.exit_:
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

    for y in range(maze.height):
        line = ""

        for x in range(maze.width):
            line += "𖦹"

            if maze.grid[y][x] & (1 << N):
                line += "═══"

            else:
                line += "   "

        line += "𖦹"
        print(line)

        line = ""
        for x in range(maze.width):
            if maze.grid[y][x] & (1 << W):
                line += "║"
            else:
                line += " "

            if (x, y) in maze.cells_42:
                line += "███"
            elif (x, y) in path_cells:
                line += " x "
            else:
                line += "   "

        if maze.grid[y][maze.width - 1] & (1 << E):
            line += "║"
        else:
            line += " "
        print(line)

    line = ""
    for x in range(maze.width):
        line += "𖦹"
        if maze.grid[maze.height - 1][x] & (1 << S):
            line += "═══"
        else:
            line += "   "
    line += "𖦹"
    print(line)
