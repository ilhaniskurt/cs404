from pysat.solvers import Solver


def vertex_k_coloring(graph: dict[int, list[int]], k: int) -> bool:
    """
    Determines if a given graph can be colored using at most k colors, such that no two adjacent vertices have the same color.

    Args:
        graph (dict[int, list[int]]): A dictionary representing the graph, where the keys are the vertices and the values are lists of adjacent vertices.
        k (int): The maximum number of colors that can be used.

    Returns:
        bool: True if the graph can be colored using at most k colors, False otherwise.
    """

    solver = Solver()
    n = len(graph)  # Number of vertices
    vars = {}

    # Create variables
    for v in range(n):
        for c in range(1, k + 1):
            vars[(v, c)] = v * k + c  # Unique variable for each vertex-color pair

    # Condition (i): Every vertex must have at least one color
    for v in range(n):
        solver.add_clause([vars[(v, c)] for c in range(1, k + 1)])

    # Condition (ii): No vertex can have more than one color
    for v in range(n):
        for c1 in range(1, k):
            for c2 in range(c1 + 1, k + 1):
                solver.add_clause([-vars[(v, c1)], -vars[(v, c2)]])

    # Condition (iii): Adjacent vertices cannot have the same color
    for v in range(n):
        for u in graph[v]:
            if u > v:  # To avoid adding the same clause twice
                for c in range(1, k + 1):
                    solver.add_clause([-vars[(v, c)], -vars[(u, c)]])

    # Check for satisfiability
    if solver.solve():
        return True
        # To get the coloring
        # solution = solver.get_model()
        # coloring = {}
        # for v in range(n):
        #     for c in range(1, k + 1):
        #         if vars[(v, c)] in solution:
        #             coloring[v] = c
        #             break
        # return coloring
    else:
        return False


def get_chromatic_number(graph: dict[int, list[int]]) -> int:
    """
    Calculates the chromatic number of a given graph.

    Args:
        graph (dict[int, list[int]]): A dictionary representing the graph, where the keys are the vertices and the values are lists of adjacent vertices.

    Returns:
        int: The chromatic number of the graph.
    """
    vertex_count = len(graph)
    for k in range(1, vertex_count + 1):
        if vertex_k_coloring(graph, k):
            return k
