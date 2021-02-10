from os import path
from random import choice
import unittest

from ga4stpg.edgeset import EdgeSet
from ga4stpg.edgeset.evaluation import EvaluateEdgeSet
from ga4stpg.edgeset.generate import gen_random_prim
from ga4stpg.edgeset.mutate import MutateReconectingComponents
from ga4stpg.graph import UGraph
from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree


class TestMutateReconectingComponents(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        filename = path.join('datasets', 'ORLibrary', filename)
        cls.stpg  = ReaderORLibrary().parser(filename)

    def test_simpliest(self):
        stpg  = self.stpg

        mutate = MutateReconectingComponents(stpg)

        after = gen_random_prim(stpg)

        self.assertIsInstance(after, EdgeSet)

        before = mutate(after)

        self.assertIsInstance(before, EdgeSet)

        tree = UGraph()

        for edge in before:
            v, u = edge
            tree.add_edge(v, u)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'

    def test_resultant_cost(self):
        stpg  = self.stpg

        mutate = MutateReconectingComponents(stpg)
        evaluate = EvaluateEdgeSet(stpg)

        after = gen_random_prim(stpg)
        before = mutate(after)

        after_cost, after_nro_components   = evaluate(after)
        before_cost, before_nro_components = evaluate(before)

        self.assertGreaterEqual(after_cost, before_cost)
        self.assertEqual(after_nro_components,  1)
        self.assertEqual(before_nro_components, 1)

if __name__ == "__main__":
    unittest.main()
