import sys
from typing import Any
import os
from config_parser import parse_config
from display import display
from mazegen.generator import MazeGenerator
from output_writer import write_output


def build_maze(config: dict[str, Any], seed: int | None) -> MazeGenerator:
    """Create a maze from the config and generate it."""
    maze = MazeGenerator(
        config["WIDTH"], config["HEIGHT"],
        config["ENTRY"], config["EXIT"],
        config["PERFECT"], seed,
    )
    maze.generate()
    return maze


def main() -> None:
    """Generate a maze from a configuration file and show a menu."""
    colors = [
        "\033[37m",
        "\033[33m",
        "\033[32m",
        "\033[36m",
    ]
    color_index = 0
    show_path = False

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    maze = build_maze(config, config.get("SEED"))
    write_output(maze, config["OUTPUT_FILE"])

    while True:
        display(maze, show_path, colors[color_index])
        print("1 - Re-generate a new maze")
        print("2 - Show / Hide the shortest path")
        print("3 - Rotate the wall colours")
        print("4 - Quit")

        try:
            choice = input("Choice? (1-4) ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        os.system("clear")
        if choice == "1":
            if "SEED" in config:
                maze = build_maze(config, config["SEED"])
            else:
                maze = build_maze(config, None)
            write_output(maze, config["OUTPUT_FILE"])
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(colors)
        elif choice == "4":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
