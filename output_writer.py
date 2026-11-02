from mazegen.generator import MazeGenerator


def write_output(maze: MazeGenerator, filename: str) -> None:
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
