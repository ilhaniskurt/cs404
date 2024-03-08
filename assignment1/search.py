import heapq
from copy import deepcopy
from typing import Callable

from maze import Direction, Maze


class Successor:
    maze: Maze
    cost: int
    direction: Direction
    cost_log: list[tuple[int, int, int]]
    __heuristic_function: Callable[[Maze, Direction], int]

    def __init__(
        self,
        maze: Maze,
        cost: int,
        direction: Direction,
        cost_log: list[tuple[int, int, int]],
        heuristic_function: Callable[[Maze, Direction], int],
    ) -> None:
        self.maze = maze
        self.cost = cost
        self.direction = direction
        self.cost_log = cost_log
        self.__heuristic_function = heuristic_function

    def get_successors(self) -> list["Successor"]:
        successors: list[Successor] = []
        for direction in Direction:
            cost = self.maze.get_action_cost(direction)
            if cost > 0:  # If action is valid
                maze_copy = deepcopy(self.maze)
                cost_log_copy = deepcopy(self.cost_log)
                heuristic = self.__heuristic_function(self.maze, direction)
                total_cost = cost + self.maze.cost + heuristic
                cost_log_copy.append((self.maze.cost, cost, heuristic))
                successors.append(
                    Successor(
                        maze_copy,
                        total_cost,
                        direction,
                        cost_log_copy,
                        self.__heuristic_function,
                    )
                )
        return successors

    def travel_node(self):
        if self.cost == 0:  # For skipping the initial node
            return
        self.maze.take_action(self.direction)


class Frontier:
    elements: list[Successor]
    entry_finder: dict[Successor, list[int, int, Successor]]
    counter: int

    def __init__(self):
        self.elements = []
        self.entry_finder = {}  # To keep track of entries and enable updating priorities
        self.counter = 0  # To resolve ties in priority

    def add_or_update(self, node: Successor, priority: int) -> None:
        """Add a new node or update the priority of an existing node"""
        if node in self.entry_finder:
            self.remove(node)
        entry = [priority, self.counter, node]
        self.entry_finder[node] = entry
        heapq.heappush(self.elements, entry)
        self.counter += 1

    def remove(self, node: Successor):
        """Mark an existing node as REMOVED"""
        entry = self.entry_finder.pop(node)
        entry[-1] = None  # Invalidate the entry

    def pop(self) -> Successor:
        """Remove and return the lowest priority node"""
        while self.elements:
            priority, _, node = heapq.heappop(self.elements)
            if node is not None:
                del self.entry_finder[node]
                return node
        raise KeyError("pop from an empty priority queue")

    def is_empty(self):
        """Check if the frontier is empty"""
        return not self.elements


def admissible_heuristic_function(maze: Maze, direction: Direction) -> int:
    estimation = (
        maze.color_goal
        - maze.colored_cells
        - maze.get_action_cost(direction, get_colored=True)
    )
    return estimation


def algorithm_analysis(successor: Successor):
    print(
        f"\nGoal state has been reached.\n({len(successor.maze.actions)}) Actions taken from inital node to goal state:\n"
    )
    is_admissible = True
    is_monotone = True
    for no, action in enumerate(successor.maze.actions, start=1):
        node_cost, action_cost, heuristic = successor.cost_log[no]
        if heuristic > successor.maze.color_goal:
            is_admissible = False
        if successor.cost_log[no - 1][2] - heuristic > action_cost:
            is_monotone = False
        print(
            f"Cost of getting to node \033[91m{no - 1}\033[0m from inital node:",
            node_cost,
        )
        print(
            f"Cost of going \033[92m{action}\033[0m from node \033[91m{no - 1}\033[0m to node \033[96m{no}\033[0m:",
            action_cost,
        )
        print(
            f"Estimated cost of getting to goal state from node \033[96m{no}\033[0m:",
            heuristic,
        )
        print("----------------------------")

    print("\nAnalysis of the heuristic function for this solution: ")
    print("Is it admissible:", end=" ")
    if is_admissible:
        print("\033[92mYES\033[0m")
    else:
        print("\033[91mNO\033[0m")
    print("Is it monotonic:", end=" ")
    if is_monotone:
        print("\033[92mYES\033[0m")
    else:
        print("\033[91mNO\033[0m")


def run_algorithm(maze: Maze, verbose: bool = False):
    start = Successor(
        maze,
        maze.cost,
        Direction.UP,  # Dummy value
        [(0, 0, maze.color_goal - 1)],
        admissible_heuristic_function,
    )  # Direction does not matter for this one
    frontier = Frontier()
    frontier.add_or_update(start, start.cost)

    if verbose:
        count = -1
        print("\n---------- START OF THE SEARCH ALGORITHM -------------\n")
    while not frontier.is_empty():
        current = frontier.pop()

        current.travel_node()

        if verbose:
            print("-----------------------------")
            count += 1
            if count == 0:
                print("Inital node")
            else:
                print("Searched node", count)
                print(
                    "Estimated cost of finishing maze through this node:", current.cost
                )
            current.maze.display_info()

        if current.maze.goal_reached:
            break

        for next in current.get_successors():
            frontier.add_or_update(next, next.cost)

        if verbose:
            print("Nodes in the frontier:", len(frontier.elements), end="\n\n")

    if verbose:
        print("---------- END OF THE SEARCH ALGORITHM -------------")

    algorithm_analysis(current)
