from mazegen.generator import MazeGenerator
from display import display
from output_writer import write_output
from config_parser import parse_config
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["ENTRY"], config["EXIT"], config["OUTPUT_FILE"], config["PERFECT"], config.get["SEED"])
        maze.generate()
        display(maze)
        write_output(maze, config["OUTPUT_FILE"])
    except TypeError as e:
        print(f"Invalid config.txt {e}")


if __name__ == "__main__":
    main()
