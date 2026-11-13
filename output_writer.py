from mazegen.generator import MazeGenerator


def write_output(maze: MazeGenerator, filename: str) -> None:
    """Write the maze to a file in the format required by the subject.

    The file has one line per row of the maze, with one hexadecimal digit
    per cell (a bit set to 1 means a closed wall: bit 0 North, bit 1 East,
    bit 2 South, bit 3 West), followed by an empty line, the entry
    coordinates, the exit coordinates and the shortest path. If the file
    cannot be written, an error message is printed.

    Args:
        maze: a maze that was already generated.
        filename: path of the output file.
    """
    path = maze.solve()

    try:
        with open(filename, "w") as f:
            for y in range(maze.height):
                line = ""
                for x in range(maze.width):
                    line += "0123456789ABCDEF"[maze.grid[y][x]]
                f.write(line + "\n")
            f.write("\n")
            f.write(f"{maze.entry[0]},{maze.entry[1]}" + "\n")
            f.write(f"{maze.exit_[0]},{maze.exit_[1]}" + "\n")
            f.write(path + "\n")

    except OSError as e:
        print(f"Error: {e}")
