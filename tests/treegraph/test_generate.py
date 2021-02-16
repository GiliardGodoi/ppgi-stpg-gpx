import unittest
from collections import Counter
from statistics import pvariance
from os import path
from random import choice

from ga4stpg.graph import ReaderORLibrary, UGraph
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedRandomWalk

class TestGenerateBasedRandomWalk(unittest.TestCase):


    def setUp(self) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        print(filename)
        filename = path.join('datasets', 'ORLibrary', filename)
        self.stpg = ReaderORLibrary().parser(filename)

    def test_return_an_ugraph(self):
        stpg = self.stpg

        initialization = GenerateBasedRandomWalk(stpg)
        tree = initialization()

        self.assertTrue(isinstance(tree, UGraph))

    def test_is_steiner_tree(self):
        stpg = self.stpg

        initialization = GenerateBasedRandomWalk(stpg)
        tree = initialization()

        _, response = is_steiner_tree(tree, stpg)

        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])

    def test_generate_differents_individuals(self):

        nro_individuals = 100

        stpg = self.stpg
        initialization = GenerateBasedRandomWalk(stpg)

        population = [initialization() for _ in range(nro_individuals)]

        self.assertEqual(len(population), nro_individuals)

        c_edges = Counter((min(v, u), max(v, u))
                            for tree in population
                                for v, u in tree.gen_undirect_edges() )

        self.assertFalse(all(value == 100 for value in c_edges.values()))

    def test_evaluation_from_differents_individuals(self):

        nro_individuals = 100
        stpg = self.stpg
        initializator = GenerateBasedRandomWalk(stpg)
        evaluator = EvaluateTreeGraph(stpg)

        population = [initializator() for _ in range(nro_individuals)]

        pop_cost = [ evaluator(tree)[0] for tree in population ]

        p_var = pvariance(pop_cost)

        self.assertEqual(len(pop_cost), nro_individuals)
        self.assertNotAlmostEqual(p_var, 0.0)
