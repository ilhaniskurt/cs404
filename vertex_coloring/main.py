import argparse

from color import get_chromatic_number, vertex_k_coloring
from reader import read_graph_file


def main(graph_path: str, k: int | None):
    graph = read_graph_file(graph_path)
    if k is None:
        chromatic_number = get_chromatic_number(graph)
        print(
            f"The chromatic number of the graph is \033[36m{chromatic_number}\033[0m."
        )
    else:
        vertex_count = len(graph)
        if k >= vertex_count:
            print(
                f"\033[36mK ({k}) is greater than or equal to the number of vertices ({vertex_count}) in the graph. Without computation we can say that the graph can be colored using at most k colors.\033[0m",
            )
        elif k == 0:
            print(
                "\033[36mBy definition graph cannot be colored using 0 colors.\033[0m"
            )
        else:
            if vertex_k_coloring(graph, k):
                print(
                    f"\033[32mThe graph can be colored using at most {k} colors.\033[0m"
                )
            else:
                print(
                    f"\033[31mThe graph cannot be colored using at most {k} colors.\033[0m"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "graph_path", nargs="?", default="graph0.txt", help="Path to the graph file"
    )
    parser.add_argument(
        "-k", "--k-color", type=int, help="Number of colors to use for vertex coloring"
    )
    args = parser.parse_args()

    main(args.graph_path, args.k_color)
