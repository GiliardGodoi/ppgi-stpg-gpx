import unittest
from os import path
from random import choice

from ga4stpg.graph import UGraph
from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mutate import ReplaceByRandomEdge

class TestMutateReplaceByRandomEdge(unittest.TestCase):

    def test_is_it_work(self):
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        filename = path.join('datasets', 'ORLibrary', filename)
        stpg  = ReaderORLibrary().parser(filename)

        initializer = GenerateBasedRandomWalk(stpg)
        before = initializer()

        mutator = ReplaceByRandomEdge(stpg)

        after = mutator(before)

        self.assertIsInstance(after, UGraph)

        _, response = is_steiner_tree(after, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
