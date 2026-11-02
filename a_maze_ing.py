from mazegen.generator import MazeGenerator
from display import display
from output_writer import write_output


def main() -> None:
    maze = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42)
    maze.generate()
    display(maze)
    write_output(maze, "maze.txt")


if __name__ == "__main__":
    main()
