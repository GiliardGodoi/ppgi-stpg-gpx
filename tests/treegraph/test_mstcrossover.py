import unittest
from os import path
from random import choice

from ga4stpg.graph import ReaderORLibrary, UGraph
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mstcrossover import (CrossoverPrimRST,
                                        CrossoverKruskalRST,
                                        CrossoverRandomWalkRST)

class TestCrossoverPrimRSTBased(unittest.TestCase):

    def setUp(self) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        print(filename)
        filename = path.join('datasets', 'ORLibrary', filename)
        self.stpg = ReaderORLibrary().parser(filename)

    def test_crossover(self):

        stpg = self.stpg

        initializator = GenerateBasedRandomWalk(stpg)
        evaluator = EvaluateTreeGraph(stpg)
        crossover = CrossoverPrimRST(stpg)

        red = initializator()
        blue = initializator()

        red_cost, _  = evaluator(red)
        blue_cost, _ = evaluator(blue)

        self.assertTrue(isinstance(red, UGraph))
        self.assertTrue(isinstance(blue, UGraph))

        self.assertGreater(red_cost, 0)
        self.assertGreater(blue_cost, 0)

        child = crossover(red, blue)
        cc_cost, _ = evaluator(child)
        self.assertGreater(cc_cost, 0)

        _, response = is_steiner_tree(child, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # self.assertTrue(response['all_leaves_are_terminals'])


class TestCrossoverKruskalRSTBased(unittest.TestCase):

    def setUp(self) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        print(filename)
        filename = path.join('datasets', 'ORLibrary', filename)
        self.stpg = ReaderORLibrary().parser(filename)

    def test_crossover(self):

        stpg = self.stpg

        initializator = GenerateBasedRandomWalk(stpg)
        evaluator = EvaluateTreeGraph(stpg)
        crossover = CrossoverKruskalRST(stpg)

        red = initializator()
        blue = initializator()

        red_cost, _  = evaluator(red)
        blue_cost, _ = evaluator(blue)

        self.assertTrue(isinstance(red, UGraph))
        self.assertTrue(isinstance(blue, UGraph))

        self.assertGreater(red_cost, 0)
        self.assertGreater(blue_cost, 0)

        child = crossover(red, blue)
        cc_cost, _ = evaluator(child)
        self.assertGreater(cc_cost, 0)

        _, response = is_steiner_tree(child, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # self.assertTrue(response['all_leaves_are_terminals'])

class TestCrossoverRandomWalkRSTBased(unittest.TestCase):

    def setUp(self) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        print(filename)
        filename = path.join('datasets', 'ORLibrary', filename)
        self.stpg = ReaderORLibrary().parser(filename)

    def test_crossover(self):

        stpg = self.stpg

        initializator = GenerateBasedRandomWalk(stpg)
        evaluator = EvaluateTreeGraph(stpg)
        crossover = CrossoverRandomWalkRST(stpg)

        red = initializator()
        blue = initializator()

        red_cost, _  = evaluator(red)
        blue_cost, _ = evaluator(blue)

        self.assertTrue(isinstance(red, UGraph))
        self.assertTrue(isinstance(blue, UGraph))

        self.assertGreater(red_cost, 0)
        self.assertGreater(blue_cost, 0)

        child = crossover(red, blue)
        cc_cost, _ = evaluator(child)
        self.assertGreater(cc_cost, 0)

        _, response = is_steiner_tree(child, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # self.assertTrue(response['all_leaves_are_terminals'])
