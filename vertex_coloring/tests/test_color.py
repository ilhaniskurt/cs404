import unittest

from color import get_chromatic_number, vertex_k_coloring
from reader import read_graph_file


class TestGraphColoring(unittest.TestCase):
    def test_get_chromatic_number(self):
        graph = read_graph_file("graph1.txt")
        self.assertEqual(get_chromatic_number(graph), 3)

    def test_vertex_k_coloring(self):
        graph = read_graph_file("graph1.txt")
        self.assertTrue(vertex_k_coloring(graph, 3))
        self.assertFalse(vertex_k_coloring(graph, 2))
