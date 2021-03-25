from os import path
from random import choice
import unittest

from ga4stpg.edgeset import EdgeSet
from ga4stpg.edgeset.evaluation import EvaluateEdgeSet
from ga4stpg.edgeset.generate import gen_random_prim
from ga4stpg.edgeset.mutate import MutatitionReplaceByLowerEdge
from ga4stpg.edgeset.mutate import MutationReplaceByRandomEdge
from ga4stpg.graph import UGraph
from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree


class TestMutatitionReplaceByLowerEdge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        filename = path.join('datasets', 'ORLibrary', filename)
        cls.stpg  = ReaderORLibrary().parser(filename)

    def test_simpliest(self):
        stpg  = self.stpg

        mutate = MutatitionReplaceByLowerEdge(stpg)

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

        mutate = MutatitionReplaceByLowerEdge(stpg)
        evaluate = EvaluateEdgeSet(stpg)

        after = gen_random_prim(stpg)
        before = mutate(after)

        after_cost, after_nro_components   = evaluate(after)
        before_cost, before_nro_components = evaluate(before)

        self.assertGreaterEqual(after_cost, before_cost)
        self.assertEqual(after_nro_components,  1)
        self.assertEqual(before_nro_components, 1)


class Test_MutationReplaceByRandomEdge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        print(filename)
        filename = path.join('datasets', 'ORLibrary', filename)
        cls.stpg  = ReaderORLibrary().parser(filename)

    def test_simpliest(self):
        stpg  = self.stpg

        mutate = MutationReplaceByRandomEdge(stpg)

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

    def test_path_like_solution(self):
        filename = path.join('tests', 'data', 'test3.txt')
        stpg  = ReaderORLibrary().parser(filename)

        after = EdgeSet()
        after.add(1, 3)
        after.add(3, 8)
        after.add(8, 5)
        after.add(5, 6)

        evaluate = EvaluateEdgeSet(stpg)
        mutate   = MutationReplaceByRandomEdge(stpg)

        cost_after, _ = evaluate(after)

        self.assertEqual(cost_after, (5+7+7+15))

        before = mutate(after)

        self.assertEqual(after, before)

        cost_before, _ = evaluate(before)
        self.assertEqual(cost_after, cost_before)


if __name__ == "__main__":
    unittest.main()
