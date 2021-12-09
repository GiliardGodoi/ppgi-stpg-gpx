import unittest
from os import path
from random import choice

from ga4stpg.graph import ReaderORLibrary, UGraph
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mstcrossover import (CrossoverGreedyPrim,
                                       CrossoverKruskalRST, CrossoverPrimRST,
                                       CrossoverRandomWalkRST,
                                       CrossoverRelativeGreedyPrim)


class BaseTestCaseMSTCrossovers(unittest.TestCase):

    def setUp(self) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        print(filename)
        filename = path.join('datasets', 'ORLibrary', filename)
        self.stpg = ReaderORLibrary().parser(filename)

        self.evaluator = EvaluateTreeGraph(self.stpg)
        self.initializator = GenerateBasedRandomWalk(self.stpg)

    def get_crossover(self):

        def whatever(red, blue):
            red_cost, _  = self.evaluator(red)
            blue_cost, _ = self.evaluator(blue)

            if red_cost < blue_cost:
                return red
            else:
                return blue

        return whatever

    def test_crossover(self):

        initializator = self.initializator
        evaluator = self.evaluator
        crossover = self.get_crossover()

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

        _, response = is_steiner_tree(child, self.stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # self.assertTrue(response['all_leaves_are_terminals'])


class TestCrossoverPrimRSTBased(BaseTestCaseMSTCrossovers):

    def get_crossover(self):
        return CrossoverPrimRST(self.stpg)


class TestCrossoverGreedyPrim(BaseTestCaseMSTCrossovers):

   def get_crossover(self):
       return CrossoverGreedyPrim(self.stpg)


class TestCrossoverRelativeGreedyPrim(BaseTestCaseMSTCrossovers):

    def get_crossover(self):
        return CrossoverRelativeGreedyPrim(self.stpg)

class TestCrossoverKruskalRSTBased(BaseTestCaseMSTCrossovers):

    def get_crossover(self):
        return CrossoverKruskalRST(self.stpg)


class TestCrossoverRandomWalkRSTBased(BaseTestCaseMSTCrossovers):

    def get_crossover(self):
        return CrossoverRandomWalkRST(self.stpg)


