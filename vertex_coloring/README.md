# Vertex Coloring Project

This project is about finding the chromatic number of a graph and checking if a graph can be colored with a given number of colors.

## Installation

This project requires Python 3.6 or later. You can install the required packages with pip:

```bash
pip install -r requirements.txt
```

# Usage

To run the program with a graph file, use the following command:

```bash
python main.py <graph_file>
```

Replace <graph_file> with the filename of your graph file under the graphs directory. The program will calculate and print the chromatic number of the graph.

You can also check if the graph can be colored with a given number of colors using the -k flag:

```bash
python main.py <graph_file> -k <number_of_colors>
```

Replace <number_of_colors> with the number of colors you want to check.

# Graph File Format

The graph file should be a text file. The first line should start with 'p' followed by the number of vertices and the number of edges in the graph. Each subsequent line represents an edge between two vertices in the graph. Each line should start with 'e' followed by the two vertices that form the edge. For example:

```plaintext
p edges 3 3
e 1 2
e 2 3
e 3 1
```

This represents a graph with 3 vertices and 3 edges forming a triangle.

## Adding a New Graph File

To add a new graph file, simply create a new text file in the format described above and place it in the graph directory
