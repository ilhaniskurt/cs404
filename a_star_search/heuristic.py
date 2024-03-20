from maze import Maze


def inadmissible_heuristic_function(maze: Maze) -> int:
    return maze.empty_cells + 2 * maze.extra_cells_traversed


def monotonic_heuristic_function(maze: Maze) -> int:
    return maze.empty_cells


def heuristic(maze: Maze) -> int:
    # Estimate the distance to the nearest uncolored cell
    nearest_uncolored_distance = float("inf")
    for x, row in enumerate(maze.map):
        for y, cell in enumerate(row):
            if cell == "0":  # Found an uncolored cell
                dist = abs(x - maze.agent_pos[0]) + abs(y - maze.agent_pos[1])
                nearest_uncolored_distance = min(nearest_uncolored_distance, dist)

    # If there are no uncolored cells, the heuristic value is 0
    if nearest_uncolored_distance == float("inf"):
        nearest_uncolored_distance = 0

    # The heuristic value is the nearest distance plus the number of remaining uncolored cells
    # This is admissible since moving to color a cell and the number of cells left to color are both underestimates
    # of the actual remaining cost.
    remaining_uncolored_cells = maze.empty_cells
    return nearest_uncolored_distance + remaining_uncolored_cells
