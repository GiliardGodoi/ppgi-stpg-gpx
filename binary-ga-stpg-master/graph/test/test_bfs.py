import unittest
import random

from graph import Graph
from graph.algorithms import bfs, find_connected_components

class TestBreadthFirstSearch(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        del self.graph

    def add_component(self, vertices):

        for v in vertices :
            qtdAdj = random.randint(1,10)
            adjacents = random.sample(vertices,qtdAdj)
            for a in adjacents :
                if a != v :
                    self.graph.add_edge(v,a)

    def test_findOneComponent(self):
        self.add_component(range(1,51))

        components = find_connected_components(self.graph)
        qtd_components = len(components)
        self.assertEqual(qtd_components,1)

    def test_findTwoComponent(self):
        self.add_component(range(1,51))
        self.add_component(range(100,151))

        components = find_connected_components(self.graph)
        qtd_components = len(components)
        self.assertEqual(qtd_components,2)

    def test_bsf(self):
        vertices = random.sample(range(1,500),50)
        start = random.sample(vertices,1)

        self.add_component(vertices)
        visited = bfs(self.graph,start=start[0])
        visited = list(visited)

        self.assertEqual(len(vertices),len(visited))
        self.assertEqual(sorted(vertices),sorted(visited))


if __name__ == "__main__" :
    unittest.main()