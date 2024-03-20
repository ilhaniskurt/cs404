# ---------------------------------
# Author: Ilhan Yavuz Iskurt
# Date: 14/03/2024
# ---------------------------------

import argparse
from os import getpid
from time import process_time

from psutil import Process

from analysis import search_analysis
from heuristic import inadmissible_heuristic_function
from maze import Maze
from search import a_star_search

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase output verbosity"
    )
    args = parser.parse_args()

    print("Welcome to A* search algorithm for color maze")
    print(
        "Difficulty levels range from \033[92measy (1-5)\033[0m, \033[93mnormal (6-10)\033[0m, \033[91mhard (11-15)\033[0m\n"
    )
    level = int(input("Please select a maze level: "))

    if level < 1 or level > 15:
        raise ValueError("Maze level should be between 1 and 15.")

    maze = Maze(level)

    process = Process(getpid())
    mem_before = process.memory_info().rss
    start_cpu = process_time()

    (
        successor,
        searches_done,
        max_frontier_size,
        final_frontier_size,
    ) = a_star_search(maze, inadmissible_heuristic_function, verbose=args.verbose)

    cpu_time = process_time() - start_cpu
    mem_used = (
        (process.memory_info().rss - mem_before) / 1024 / 1024
    )  # Convert bytes to megabytes

    search_analysis(
        successor,
        searches_done,
        final_frontier_size,
        max_frontier_size,
        cpu_time,
        mem_used,
    )
