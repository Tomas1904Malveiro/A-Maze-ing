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
    def __init__(self, width: int, height: int,
                entry: tuple[int, int], exit_: tuple[int, int],
                perfect: bool = True, seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.grid = [[15] * width for _ in range(height)]
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.cells_42: list[tuple[int, int]] = []

    def open_wall(self, x: int, y: int, direction: int) -> None:
        opposite = [S, W, N, E]

        nx = x + DX[direction]
        ny = y + DY[direction]

        self.grid[y][x] &= ~(1 << direction)
        self.grid[ny][nx] &= ~(1 << opposite[direction])

    def get_cells_42(self) -> list[tuple[int, int]]:
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


    def solve(self) -> str:
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

                if 0 <= nx < self.width and 0 <= ny < self.height and not self.grid[y][x] & (1 << direction) and not visited[ny][nx]:
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
