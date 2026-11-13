import random
N, E, S, W = 0, 1, 2, 3
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]
CELLS_42 = [
    # numero 4
    (0, 1), (2, 1),
    (0, 2), (2, 2),
    (0, 3), (1, 3), (2, 3),
    (2, 4),
    (2, 5),
    # numero 2
    (5, 1), (6, 1), (7, 1),
    (7, 2),
    (5, 3), (6, 3), (7, 3),
    (5, 4),
    (5, 5), (6, 5), (7, 5),
]


class MazeGenerator:
    """Generate and solve a rectangular maze.

    The maze is stored in ``grid``: a list of rows (``grid[y][x]``) where
    each cell is an integer from 0 to 15 whose bits are the closed walls
    (bit 0 = North, 1 = East, 2 = South, 3 = West). Every cell starts with
    all four walls closed, and generating the maze opens walls.

    Attributes:
        width: number of columns.
        height: number of rows.
        grid: wall encoding of every cell, indexed as ``grid[y][x]``.
        entry: ``(x, y)`` coordinates of the entry.
        exit_: ``(x, y)`` coordinates of the exit.
        perfect: True for a perfect maze (no loops), False for a braided
            maze (loops, no dead ends outside the "42" pattern).
        rng: seeded random generator, so the same seed gives the same maze.
        cells_42: ``(x, y)`` cells of the closed "42" pattern (empty until
            ``generate`` is called, or if the maze is too small).
    """
    def __init__(
                self, width: int, height: int,
                entry: tuple[int, int], exit_: tuple[int, int],
                perfect: bool = True, seed: int | None = None) -> None:
        """Create a maze with all walls closed.

        The arguments are not validated by this class.

        Args:
            width: number of columns of the maze.
            height: number of rows of the maze.
            entry: ``(x, y)`` coordinates of the entry.
            exit_: ``(x, y)`` coordinates of the exit.
            perfect: if True the maze has a single path between any two
                cells; if False loops are added (braiding).
            seed: seed of the random generator, or None for a different
                maze at every run.
        """
        self.width = width
        self.height = height
        self.grid = [[15] * width for _ in range(height)]
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.cells_42: list[tuple[int, int]] = []

    def open_wall(self, x: int, y: int, direction: int) -> None:
        """Open the wall between a cell and its neighbour.

        Both cells are updated so that the shared wall stays coherent.
        The neighbour must be inside the maze.

        Args:
            x: column of the cell.
            y: row of the cell.
            direction: side of the cell to open (N, E, S or W).
        """
        opposite = [S, W, N, E]

        nx = x + DX[direction]
        ny = y + DY[direction]

        self.grid[y][x] &= ~(1 << direction)
        self.grid[ny][nx] &= ~(1 << opposite[direction])

    def get_cells_42(self) -> list[tuple[int, int]]:
        """Return the cells that draw the "42" pattern.

        The pattern is centred in the maze. If the maze is smaller than
        10x7 cells an error message is printed and no cells are returned.

        Returns:
            List of ``(x, y)`` coordinates of the closed cells, or an empty
            list if the pattern does not fit.
        """
        if self.height < 7 or self.width < 10:
            print("Error: maze too small for the '42' pattern (min 10x7)")
            return []

        start_y = (self.height - 7) // 2
        start_x = (self.width - 8) // 2

        cells = []
        for cell in CELLS_42:
            cells.append((start_x + cell[0], start_y + cell[1]))
        return cells

    def generate(self) -> None:
        """Generate the maze, opening walls in ``grid``.

        Uses a depth-first search (recursive backtracker) with a stack,
        starting at the entry. The cells of the "42" pattern are marked as
        visited beforehand, so they stay fully closed (if the entry or the
        exit is inside the pattern, the pattern is omitted and an error
        message is printed). If ``perfect`` is False, ``braid`` is called
        afterwards to remove the dead ends.

        Call it once per object: the grid is not reset between calls.
        """
        visited = [[False] * self.width for _ in range(self.height)]

        x = self.entry[0]
        y = self.entry[1]
        visited[y][x] = True
        stack = [(x, y)]

        cells42 = self.get_cells_42()
        if self.entry in cells42 or self.exit_ in cells42:
            print("Error: The entry or exit are inside of 42 cells")
            cells42 = []

        self.cells_42 = cells42
        for cell in cells42:
            visited[cell[1]][cell[0]] = True

        while len(stack) > 0:
            current = stack[-1]
            x = current[0]
            y = current[1]

            options = []
            if y > 0 and not visited[y - 1][x]:
                options.append(N)
            if x < self.width - 1 and not visited[y][x + 1]:
                options.append(E)
            if y < self.height - 1 and not visited[y + 1][x]:
                options.append(S)
            if x > 0 and not visited[y][x - 1]:
                options.append(W)

            if len(options) > 0:
                direction = self.rng.choice(options)
                self.open_wall(x, y, direction)

                if direction == N:
                    y = y - 1
                elif direction == E:
                    x = x + 1
                elif direction == S:
                    y = y + 1
                else:
                    x = x - 1

                visited[y][x] = True
                stack.append((x, y))
            else:
                stack.pop()

        if not self.perfect:
            self.braid()

    def solve(self) -> str:
        """Find the shortest path from the entry to the exit.

        Uses a breadth-first search over the open walls. It only reads the
        grid, so the maze is not modified.

        Returns:
            The path as a string of ``N``, ``E``, ``S`` and ``W`` letters,
            or an empty string if the exit cannot be reached.
        """
        visited = [[False] * self.width for _ in range(self.height)]
        queue = [self.entry]
        came_from = {}

        visited[self.entry[1]][self.entry[0]] = True

        while queue:
            current = queue.pop(0)
            x = current[0]
            y = current[1]
            if current == self.exit_:
                break

            for direction in N, E, S, W:
                nx = x + DX[direction]
                ny = y + DY[direction]

                if (
                    0 <= nx < self.width and 0 <= ny < self.height
                    and not self.grid[y][x] & (1 << direction)
                    and not visited[ny][nx]
                ):
                    visited[ny][nx] = True
                    came_from[(nx, ny)] = ((x, y), direction)
                    queue.append((nx, ny))

        if self.exit_ not in came_from:
            return ""

        position = self.exit_
        path = []
        while position != self.entry:
            previous = came_from[position][0]
            direction = came_from[position][1]
            path.append(direction)
            position = previous

        path.reverse()
        result = ""
        for d in path:
            result += "NESW"[d]

        return result

    def count_walls(self, x: int, y: int) -> int:
        """Return how many walls the cell (x, y) has closed."""
        count = 0
        for direction in (N, E, S, W):
            if self.grid[y][x] & (1 << direction):
                count += 1
        return count

    def braid(self) -> None:
        """Open walls in dead ends so that the maze has loops."""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.cells_42:
                    continue
                if self.count_walls(x, y) != 3:
                    continue

                candidates = []
                for direction in (N, E, S, W):
                    nx = x + DX[direction]
                    ny = y + DY[direction]

                    if (
                        0 <= nx < self.width and 0 <= ny < self.height
                        and self.grid[y][x] & (1 << direction)
                        and (nx, ny) not in self.cells_42
                    ):
                        candidates.append(direction)

                if len(candidates) > 0:
                    self.rng.shuffle(candidates)
                for direction in candidates:
                    nx = x + DX[direction]
                    ny = y + DY[direction]
                    old_a = self.grid[y][x]
                    old_b = self.grid[ny][nx]

                    self.open_wall(x, y, direction)
                    if self.has_open_3x3():
                        self.grid[y][x] = old_a
                        self.grid[ny][nx] = old_b
                    else:
                        break

    def has_open_3x3(self) -> bool:
        """Return True if the maze has a fully open 3x3 area."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                all_open = True

                for j in range(3):
                    for i in range(2):
                        if self.grid[y + j][x + i] & (1 << E):
                            all_open = False

                for j in range(2):
                    for i in range(3):
                        if self.grid[y + j][x + i] & (1 << S):
                            all_open = False

                if all_open:
                    return True
        return False
