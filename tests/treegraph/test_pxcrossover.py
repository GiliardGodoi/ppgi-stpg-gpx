import unittest
from os import path
from random import sample

from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph import UGraph
from ga4stpg.graph.steiner import shortest_path_with_origin
from ga4stpg.graph.util import is_steiner_tree, gg_total_weight

from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.pxcrossover import PXTree

class TestPXCrossover(unittest.TestCase):

    def test_basic(self):
        filename = path.join("datasets", "ORLibrary", "steinc5.txt")
        stpg = ReaderORLibrary().parser(filename)

        vertices = list(stpg.graph.vertices)
        v, u = sample(vertices, 2)

        crossover = PXTree(stpg)
        evaluator = EvaluateTreeGraph(stpg)

        red, red_cost   = shortest_path_with_origin(stpg.graph, v, stpg.terminals)
        blue, blue_cost = shortest_path_with_origin(stpg.graph, u, stpg.terminals)

        child = crossover(red, blue)

        child_cost, _ = evaluator(child)

        self.assertLessEqual(child_cost, red_cost)
        self.assertLessEqual(child_cost, blue_cost)

        _, response = is_steiner_tree(child, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        self.assertTrue(response['all_leaves_are_terminals'])

    def test_exchange_edges(self):
        filename = path.join('datasets', 'test', 'test3.txt')
        stpg  = ReaderORLibrary().parser(filename)

        red = UGraph()
        edges = [(1, 3), (3, 8), (8, 5), (5, 6)]
        for edge in edges:
            red.add_edge(edge[0], edge[1])

        blue = UGraph()
        edges = [(1, 3), (3, 8), (3, 7), (7, 4), (4, 6)]
        for edge in edges:
            blue.add_edge(edge[0], edge[1])

        crossover = PXTree(stpg)

        child = crossover(red, blue)

        _, response = is_steiner_tree(child, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        self.assertTrue(response['all_leaves_are_terminals'])
