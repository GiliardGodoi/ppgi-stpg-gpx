import unittest

from graph.graph import Graph
from graph.algorithms import shortest_path_dijkstra as dijkstra

class TestDijkstraImplementation(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge('a', 'b', weight=15)
        self.graph.add_edge('a', 'c', weight=25)
        self.graph.add_edge('c', 'd', weight=10)
        self.graph.add_edge('c', 'e', weight=20)
        self.graph.add_edge('e', 'f', weight=10)
        self.graph.add_edge('e', 'g', weight= 5)
        self.graph.add_edge('e', 'b', weight=10)
        self.graph.add_edge('b', 'h', weight= 5)
        self.graph.add_edge('b', 'i', weight=25)
        self.graph.add_edge('h', 'i', weight=15)

    def test_small_graph(self):

        graph = self.graph

        distances, _ = dijkstra(graph, 'a')

        self.assertEqual(distances['a'],  0)
        self.assertEqual(distances['b'], 15)
        self.assertEqual(distances['c'], 25)
        self.assertEqual(distances['d'], 35)
        self.assertEqual(distances['e'], 25)
        self.assertEqual(distances['f'], 35)
        self.assertEqual(distances['g'], 30)
        self.assertEqual(distances['h'], 20)
        self.assertEqual(distances['i'], 35)

    def test_desconnected_graph(self):

        graph = self.graph

        # desconnected edge
        graph.add_edge('z', 'w', weight=40)

        distances, _ = dijkstra(graph, 'a')

        self.assertNotEqual(distances['z'], 40)
        self.assertEqual(distances['z'], float("inf"))

        #mas R nem é um vértice do grafo
        self.assertEqual(distances['R'], float("inf"))


    def test_previous_tree(self):

        graph = self.graph

        _, previous_tree = dijkstra(graph, 'a')

        self.assertEqual(previous_tree['i'], 'h')
        self.assertEqual(previous_tree['b'], 'a')
        self.assertEqual(previous_tree['a'], None)


if __name__ == "__main__" :
    unittest.main()
