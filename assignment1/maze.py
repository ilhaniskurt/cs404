from enum import Enum
from pathlib import Path

MAZE_DIR = Path("mazes")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)

    def __str__(self):
        return self.name


class Maze:
    map: list[list]
    agent_pos: tuple[int, int]
    empty_cells: int
    colored_cells: int
    extra_cells_traversed: int
    color_goal: int
    actions: list[Direction]

    @property
    def cost(self) -> int:
        return self.extra_cells_traversed + self.colored_cells - 1

    @property
    def goal_reached(self) -> bool:
        return self.color_goal == self.colored_cells

    def __init__(self, level: int) -> None:
        self.map = []
        self.agent_pos = (-1, -1)
        self.empty_cells = 0
        self.colored_cells = 0
        self.extra_cells_traversed = 0
        self.color_goal = 0
        self.actions: list[Direction] = []

        maze_path = MAZE_DIR / f"lvl{level}.txt"
        with maze_path.open("r", encoding="utf-8") as file:
            for x, row in enumerate(file):
                self.map.append([])
                for y, column in enumerate(row.strip().split(" ")):
                    match column:
                        case "S":
                            if self.agent_pos != (-1, -1):
                                raise ValueError("Multiple agent symbol detected.")
                            self.agent_pos = (x, y)
                            self.map[x].append("C")
                            self.colored_cells += 1
                        case "C":
                            self.map[x].append("C")
                            self.colored_cells += 1
                        case "0":
                            self.map[x].append("0")
                            self.empty_cells += 1
                        case "X":
                            self.map[x].append("X")
                        case _:
                            raise ValueError("Unexpected maze symbol.")
        self.color_goal = self.empty_cells + self.colored_cells
        if self.agent_pos == (-1, -1):
            raise ValueError("No agent (S) is found at the maze")

    def display_snapshot(self) -> None:
        print("Red colored cell denotes the agent.\n")
        for x, row in enumerate(self.map):
            for y, column in enumerate(row):
                if (x, y) == self.agent_pos:
                    print(f"\033[91m{column}\033[0m", end=" ")
                else:
                    match column:
                        case "X":
                            print(f"\033[97m{column}\033[0m", end=" ")
                        case "C":
                            print(f"\033[92m{column}\033[0m", end=" ")
                        case "0":
                            print(f"\033[93m{column}\033[0m", end=" ")
            print()
        print()

    def take_action(self, direction: Direction, get_colored: bool = False) -> None:
        dx, dy = direction.value
        x, y = self.agent_pos
        try:
            while True:
                if x + dx < 0 or y + dy < 0:
                    raise IndexError
                match self.map[x + dx][y + dy]:
                    case "X":
                        raise IndexError
                    case "C":
                        self.extra_cells_traversed += 1
                    case "0":
                        self.empty_cells -= 1
                        self.colored_cells += 1
                        self.map[x + dx][y + dy] = "C"
                    case _:
                        raise ValueError
                x += dx
                y += dy
        except IndexError:
            self.agent_pos = (x, y)
            self.actions.append(direction)

    def get_action_cost(self, direction: Direction, get_colored: bool = False) -> int:
        dx, dy = direction.value
        x, y = self.agent_pos
        cost = 0
        cells_to_be_colored = 0
        try:
            while True:
                if x + dx < 0 or y + dy < 0:
                    raise IndexError
                match self.map[x + dx][y + dy]:
                    case "X":
                        raise IndexError
                    case "C":
                        pass
                    case "0":
                        cells_to_be_colored += 1
                        pass
                    case _:
                        raise ValueError
                x += dx
                y += dy
                cost += 1
        except IndexError:
            pass
        return cost if not get_colored else cells_to_be_colored

    def display_info(self):
        self.display_snapshot()
        print("Total cells to be colored:", self.color_goal)
        print("Colored cells so far:", self.colored_cells)
        print("Empty cells remaining:", self.empty_cells)
        print("Extra cells visited:", self.extra_cells_traversed)
        print("Cost of current state:", self.cost)
        print()
