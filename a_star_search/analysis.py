from maze import Maze
from search import Successor


def get_maze_difficulty_score(maze: Maze) -> float:
    row_n = len(maze.map)
    col_n = len(maze.map[0])
    open_cells = 0  # Cells with no wall adjacent

    for i, row in enumerate(maze.map):
        for j, col in enumerate(row):
            if col != "X":
                adjacent_walls = 0
                # Check each adjacent cell for walls, considering boundaries
                if i > 0 and maze.map[i - 1][j] == "X":
                    adjacent_walls += 1
                if i < row_n - 1 and maze.map[i + 1][j] == "X":
                    adjacent_walls += 1
                if j > 0 and maze.map[i][j - 1] == "X":
                    adjacent_walls += 1
                if j < col_n - 1 and maze.map[i][j + 1] == "X":
                    adjacent_walls += 1

                # If there are no adjacent walls, increment the count of open cells
                if adjacent_walls == 0:
                    open_cells += 1

    openness_ratio = open_cells / max(maze.color_goal, 1)  # Avoid division by zero

    # Normalize the difficulty score to a range of 0 - 10
    difficulty_score = 10 * openness_ratio  # Scale the openness ratio

    return format(difficulty_score, ".3f")


def search_analysis(
    successor: Successor,
    searches_done: int,
    final_frontier_size: int,
    max_frontier_size: int,
    cpu_time: float,
    memory_used: int,
) -> None:
    maze = successor.maze
    solution_true_cost = maze.cost
    is_admissible = True
    is_monotonic = True

    print("\nGoal state has been reached.\n")
    print("Practical time and space complexity of the search:")
    print("CPU time taken:\033[96m", format(cpu_time, ".3f"), "\033[0mseconds")
    print("Memory used:\033[96m", format(memory_used, ".3f"), "\033[0mMB\n")

    print("Actions taken from initial node to goal state:\n")
    for i, action in enumerate(maze.actions, 1):
        print(f"Action {i}: \033[92m{action}\033[0m")

    print(f"\nNumber of cells in the maze: {maze.color_goal}")
    print(f"Difficulty score of the maze: {get_maze_difficulty_score(maze)}")
    print(f"Total distance traveled by the agent: {solution_true_cost}")
    print(f"Number of search steps: {searches_done}")
    print(f"Maximum number of nodes in the frontier at any time: {max_frontier_size}")
    print(f"Number of nodes in the frontier at the end: {final_frontier_size}")

    heuristic_prime = 0
    cost_prime = solution_true_cost
    while maze.undo_action():
        heuristic = successor.heuristic_function(maze)
        if heuristic + maze.cost > solution_true_cost:
            is_admissible = False
        if heuristic > cost_prime - maze.cost + heuristic_prime:
            is_monotonic = False
        heuristic_prime = heuristic
        cost_prime = maze.cost

    print("\nAnalysis of the heuristic function for this solution:\n")
    print(
        f"Is it admissible: {"\033[92mYES" if is_admissible else "\033[91mNO"}\033[0m"
    )
    print(f"Is it monotonic: {"\033[92mYES" if is_monotonic else "\033[91mNO"}\033[0m")
