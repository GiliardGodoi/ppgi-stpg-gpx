import unittest
from os import path

from ga4stpg.graph import UGraph
from ga4stpg.graph import ReaderORLibrary

from ga4stpg.tree.evaluation import EvaluateTreeGraph


class TestEvaluateTreeGraph(unittest.TestCase):

    def test_example_solution_one(self):

        filename = path.join("datasets", "test", "test4.txt")
        stpg = ReaderORLibrary().parser(filename)

        tree = UGraph()
        edges = [(1, 3), (3, 8), (3, 7), (7, 4), (4 ,6)]
        for edge in edges:
            v, u = edge
            tree.add_edge(v, u)

        evaluator = EvaluateTreeGraph(stpg)
        self.assertTrue(callable(evaluator))

        cost, nro_partition = evaluator(tree)
        self.assertEqual(nro_partition, 1)
        self.assertEqual(cost, (5+7+4+4+6))

    def test_example_solution_two_components(self):
        filename = path.join("datasets", "test", "test4.txt")
        stpg = ReaderORLibrary().parser(filename)

        tree = UGraph()
        edges = [(1, 3), (3, 8), (8, 5), (5, 6), (2,4)]
        for edge in edges:
            v, u = edge
            tree.add_edge(v, u)

        evaluator = EvaluateTreeGraph(stpg)
        self.assertTrue(callable(evaluator))

        cost, nro_partition = evaluator(tree)

        self.assertEqual(nro_partition, 2)
        self.assertEqual(cost, (5+7+7+15+16))

    def test_penality_function(self):

        filename = path.join("datasets", "test", "test4.txt")
        stpg = ReaderORLibrary().parser(filename)

        tree = UGraph()
        edges = [(1, 3), (3, 8), (8, 5), (5, 6), (2,4)]
        for edge in edges:
            v, u = edge
            tree.add_edge(v, u)

        evaluator = EvaluateTreeGraph(stpg, penality_function=lambda nro: (nro - 1)*100)
        self.assertTrue(callable(evaluator))

        cost, nro_partition = evaluator(tree)

        self.assertEqual(nro_partition, 2)
        self.assertEqual(cost, (5+7+7+15+16+100))

    def test_edge_non_exist_in_stpg_instance(self):
        filename = path.join("datasets", "test", "test4.txt")
        stpg = ReaderORLibrary().parser(filename)

        tree = UGraph()
        edges = [(1, 3), (3, 8), (8, 5), (5, 6), (8 ,9)]
        for edge in edges:
            v, u = edge
            tree.add_edge(v, u)

        evaluator = EvaluateTreeGraph(stpg)
        self.assertTrue(callable(evaluator))

        with self.assertRaises(ValueError):
            cost , __ = evaluator(tree)
