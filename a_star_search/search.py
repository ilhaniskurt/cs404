import heapq
from copy import deepcopy
from typing import Callable

from maze import Direction, Maze


class Successor:
    def __init__(
        self,
        maze: Maze,
        direction: Direction,
        heuristic_function: Callable[[Maze], int],
    ):
        self.maze = (
            deepcopy(maze) if direction else maze
        )  # No deepcopy for the initial state
        self.direction = direction
        self.heuristic_function = heuristic_function
        self.cost = (
            0 if direction is None else self.apply_action()
        )  # Apply action if not the initial state

    def apply_action(self) -> int:
        """Apply the action to the maze, if valid, and return the updated cost."""
        if self.direction and self.maze.take_action(self.direction):
            # If the action is valid, update the cost based on the heuristic function
            return self.maze.cost + self.heuristic_function(self.maze)
        return float(
            "inf"
        )  # Return infinite cost for invalid actions to ensure they're not chosen

    def generate_successors(self) -> list["Successor"]:
        """Generate successors for each possible direction from the current state."""
        successors = []
        for direction in Direction:
            # Create a new successor for each direction and evaluate its validity and cost
            new_successor = Successor(self.maze, direction, self.heuristic_function)
            if new_successor.cost < float("inf"):  # If the action led to a valid state
                successors.append(new_successor)
        return successors


class Frontier:
    def __init__(self):
        self.elements = []
        self.entry_finder = {}  # map from item to entries
        self.counter = 0  # unique sequence count

    def add_or_update(self, node: Successor, priority: int):
        if node in self.entry_finder:
            self.remove(node)
        entry = [priority, self.counter, node]
        self.entry_finder[node] = entry
        heapq.heappush(self.elements, entry)
        self.counter += 1

    def remove(self, node: Successor):
        entry = self.entry_finder.pop(node)
        entry[-1] = None

    def pop(self) -> Successor:
        while self.elements:
            priority, _, node = heapq.heappop(self.elements)
            if node is not None:
                del self.entry_finder[node]
                return node
        raise KeyError("pop from an empty priority queue")

    def is_empty(self):
        return not self.elements


def a_star_search(
    maze: Maze,
    heuristic_function: Callable[[Maze], int],
    verbose: bool = False,
) -> tuple[Successor, int, int, int]:
    frontier = Frontier()
    start = Successor(
        maze, None, heuristic_function
    )  # Start state with no initial direction

    frontier.add_or_update(
        start, start.cost
    )  # Initial priority based on start state cost

    visited: dict[Maze, int] = {}
    searches_done = 0
    final_frontier_size = 0
    max_frontier_size = 1
    if verbose:
        print("\n---------- START OF THE SEARCH ALGORITHM -------------\n")

    while not frontier.is_empty():
        current_successor = frontier.pop()

        if verbose:
            print("-----------------------------")
            if searches_done == 0:
                print("Inital node")
            else:
                print("Searched node", searches_done)
                print(
                    "Estimated cost of finishing maze through this node:",
                    current_successor.cost,
                )
            current_successor.maze.display_info()

        if current_successor.maze.goal_reached:
            if verbose:
                print("---------- END OF THE SEARCH ALGORITHM -------------")
            final_frontier_size = len(frontier.elements)
            return (
                current_successor,
                searches_done,
                max_frontier_size,
                final_frontier_size,
            )  # Goal state reached

        if (
            current_successor.maze not in visited
            or current_successor.maze.cost < visited[current_successor.maze]
        ):
            visited[current_successor.maze] = current_successor.maze.cost
            searches_done += 1
            successors = current_successor.generate_successors()
            for successor in successors:
                frontier.add_or_update(successor, successor.cost)
            max_frontier_size = max(
                max_frontier_size, len(frontier.elements)
            )  # Update max frontier size

            if verbose:
                print("Nodes in the frontier:", len(frontier.elements), end="\n\n")
        elif verbose:
            print("-----------------------------")
            print("\033[96mSkipping already visited node..\033[0m")

    raise ValueError("Goal state not reached")
