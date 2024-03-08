from maze import Maze
from search import run_algorithm

if __name__ == "__main__":
    print("Welcome to A* search algorithm for color maze")
    print(
        "Difficulty levels range from \033[92measy (1-5)\033[0m, \033[93mnormal (6-10)\033[0m, \033[91mhard (11-15)\033[0m\n"
    )
    user_input = input("Please select a maze level: ")
    level = int(user_input[0])

    if level < 0 or level > 15:
        raise ValueError("Maze level should be between 1 and 15.")

    maze = Maze(level)

    verbose = False
    if len(user_input) > 1 and user_input[1] == "v":
        verbose = True

    run_algorithm(maze, verbose=verbose)
