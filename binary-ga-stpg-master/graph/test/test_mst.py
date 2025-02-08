import unittest
from os import path

from graph import Graph
from graph.algorithms import prim
from graph.reader import Reader

class TestMinimumSpanningTree(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        arquivo = path.join("datasets", "osti", "b01.stp")

        reader = Reader()

        self.stp = reader.parser(arquivo)

        self.graph = Graph(vertices=self.stp.nro_nodes,edges=self.stp.graph)

    def test_mst_cost(self):
        start_node = 34
        _, cost = prim(self.graph,start_node)

        self.assertGreater(cost,0)
        self.assertEqual(cost,238)


if __name__ == "__main__" :
    unittest.main()