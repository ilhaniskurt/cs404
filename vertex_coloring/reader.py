from pathlib import Path
from sys import stderr

GRAPH_DIR = "graphs"


def GraphException(message: str):
    print("GraphException:", message, file=stderr)
    exit(1)


def p_line(line: str) -> tuple[int, int]:
    line = line.strip()
    components = line.split(" ")
    if (
        len(components) != 4
        or not components[1] == "edge"
        or not components[2].isdigit()
        or not components[3].isdigit()
    ):
        GraphException(
            f"Invalid file format. The first line '{line}' should be formatted as 'p edge a b', where 'a' and 'b' are integers."
        )
    edges = int(components[3])
    vertices = int(components[2])

    limit = vertices * (vertices - 1) / 2
    if edges > limit:
        GraphException(
            f"Invalid graph description. The number of edges ({edges}) cannot be greater than the number of edges ({int(limit)}) in a complete graph (with {vertices} vertices)."
        )

    return vertices, edges


def e_line(line: str, vertex_count: int) -> tuple[int, int]:
    line = line.strip()
    components = line.split(" ")
    if (
        len(components) != 3
        or not components[0] == "e"
        or not components[1].isdigit()
        or not components[2].isdigit()
    ):
        GraphException(
            f"Invalid file format. The line '{line}' should be formatted as 'e a b', where 'a' and 'b' are integers."
        )
    a = int(components[1])
    b = int(components[2])
    if a < 0 or a > vertex_count or b < 0 or b > vertex_count:
        GraphException(
            f"Invalid vertex indices. The vertex indices in the line '{line}' should be between 0 and {vertex_count + 1}."
        )
    return a - 1, b - 1  # 0-based indexing


def read_graph_file(file_name: str) -> dict[int, list[int]]:
    file_path = Path(GRAPH_DIR) / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        first_line = next(line for line in file if not line.startswith("c "))
        if not first_line.startswith("p"):
            GraphException(
                "Invalid file format. The first (non-comment) line should start with 'p'."
            )

        vertex_count, edge_count = p_line(first_line)
        graph = {i: [] for i in range(vertex_count)}
        count = 0
        for line in file:
            if line.startswith("c"):
                continue
            if line.startswith("p"):
                GraphException(
                    "Invalid file format. There should be only one 'p' line."
                )
            if not line.startswith("e"):
                GraphException(
                    "Invalid file format. The (non-comment) lines after the 'p' line should start with 'e'."
                )
            a, b = e_line(line, vertex_count)
            if a == b:
                GraphException(
                    f"Invalid graph description. The edge ({a + 1}, {b + 1}) is a self-loop."
                )
            if b in graph[a]:
                GraphException(
                    f"Invalid graph description. The edge ({a + 1}, {b + 1}) is duplicated."
                )
            graph[a].append(b)
            graph[b].append(a)  # undirected graph
            count += 1

        if count != edge_count:
            GraphException(
                f"Invalid graph description. The number of edges ({edge_count}) does not match the number of lines in the file ({count - 1})."
            )

        return graph
