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
    def __init__(self, level: int) -> None:
        self.map: list[list[str]] = []
        self.agent_pos: tuple[int, int] = (-1, -1)
        self.empty_cells: int = 0
        self.colored_cells: int = 0
        self.extra_cells_traversed: int = 0
        self.color_goal: int = 0
        self.actions: list[Direction] = []
        self.movement_history: list[
            tuple[tuple[int, int], list]
        ] = []  # Track movements for undoing actions

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

    def take_action(self, direction: Direction, get_colored: bool = False) -> bool:
        dx, dy = direction.value
        x, y = self.agent_pos
        initial_pos = self.agent_pos
        path_taken = []  # Track the path taken during this action
        action_valid = False
        try:
            while True:
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or self.map[nx][ny] == "X":
                    break
                action_valid = True
                if self.map[nx][ny] == "0":
                    self.empty_cells -= 1
                    self.colored_cells += 1
                    path_taken.append(((nx, ny), "0"))  # Record changes
                    self.map[nx][ny] = "C"
                elif self.map[nx][ny] == "C":
                    self.extra_cells_traversed += 1
                    path_taken.append(((nx, ny), "C"))
                x, y = nx, ny
        finally:
            if action_valid:
                self.agent_pos = (x, y)
                self.actions.append(direction)
                self.movement_history.append(
                    (initial_pos, path_taken)
                )  # Record movement
            return action_valid

    def undo_action(self) -> bool:
        if not self.movement_history:
            return False  # No actions to undo

        self.agent_pos, path_taken = self.movement_history.pop()
        for (x, y), cell_type in reversed(path_taken):
            if cell_type == "0":  # Revert colored cells to empty
                self.map[x][y] = cell_type
                self.empty_cells += 1
                self.colored_cells -= 1
            elif cell_type == "C":
                # If reverting a cell that had been colored (i.e., it was "C" before and was traversed),
                # then decrement extra_cells_traversed as this traversal is being undone.
                self.extra_cells_traversed -= 1
        self.actions.pop()
        return True

    @property
    def cost(self) -> int:
        return self.extra_cells_traversed + self.colored_cells - 1

    @property
    def goal_reached(self) -> bool:
        return self.color_goal == self.colored_cells

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

    def display_info(self) -> None:
        self.display_snapshot()
        print("Total cells to be colored:", self.color_goal)
        print("Colored cells so far:", self.colored_cells)
        print("Empty cells remaining:", self.empty_cells)
        print("Extra cells visited:", self.extra_cells_traversed)
        print("Cost of current state:", self.cost)
        print()

    def __eq__(self, other: "Maze"):
        # Check if all relevant attributes are equal
        return (
            self.map == other.map
            and self.agent_pos == other.agent_pos
            and self.empty_cells == other.empty_cells
            and self.colored_cells == other.colored_cells
            and self.extra_cells_traversed == other.extra_cells_traversed
            # Include any other attributes here
        )

    def __hash__(self) -> int:
        # Hash tuple of all relevant attributes
        return hash(
            (
                tuple(
                    tuple(row) for row in self.map
                ),  # Convert list of lists to tuple of tuples for hashing
                self.agent_pos,
                self.empty_cells,
                self.colored_cells,
                self.extra_cells_traversed,
                # Include any other attributes here
            )
        )
