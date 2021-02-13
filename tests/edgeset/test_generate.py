import unittest
from os import path

from ga4stpg.edgeset import EdgeSet
from ga4stpg.edgeset.generate import gen_random_prim, gen_random_kruskal, gen_random_walk
from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.graph import UGraph

class TestGenerateRadomPrimBased(unittest.TestCase):

    def setUp(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb18.txt')
        self.stpg  = ReaderORLibrary().parser(filename)

    def test_returning_edge_set(self):
        stpg = self.stpg
        chromosome = gen_random_prim(stpg)
        self.assertIsInstance(chromosome, EdgeSet)

    def test_terminals_are_in(self):
        stpg = self.stpg
        terminals = set(stpg.terminals)
        individual = gen_random_prim(stpg)
        vertices = set([v for v in individual.vertices])

        self.assertTrue(terminals.issubset(vertices))

    def test_is_steiner_tree(self):
        stpg = self.stpg

        chromosome = gen_random_prim(stpg)
        tree = UGraph()

        for edge in chromosome:
            v, u = edge
            tree.add_edge(v, u)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'

class TestGenerateRadomKruskalBased(unittest.TestCase):

    def setUp(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb18.txt')
        self.stpg  = ReaderORLibrary().parser(filename)

    def test_returning_edge_set(self):
        stpg = self.stpg
        chromosome = gen_random_kruskal(stpg)
        self.assertIsInstance(chromosome, EdgeSet)

    def test_terminals_are_in(self):
        stpg = self.stpg
        terminals = set(stpg.terminals)
        individual = gen_random_kruskal(stpg)
        vertices = set([v for v in individual.vertices])

        self.assertTrue(terminals.issubset(vertices))

    def test_is_steiner_tree(self):
        stpg = self.stpg

        chromosome = gen_random_kruskal(stpg)
        tree = UGraph()

        for edge in chromosome:
            v, u = edge
            tree.add_edge(v, u)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'


class TestGenerateRadoWalkBased(unittest.TestCase):

    def setUp(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb18.txt')
        self.stpg  = ReaderORLibrary().parser(filename)

    def test_returning_edge_set(self):
        stpg = self.stpg
        chromosome = gen_random_walk(stpg)
        self.assertIsInstance(chromosome, EdgeSet)

    def test_terminals_are_in(self):
        stpg = self.stpg
        terminals = set(stpg.terminals)
        individual = gen_random_walk(stpg)
        vertices = set([v for v in individual.vertices])

        self.assertTrue(terminals.issubset(vertices))

    def test_is_steiner_tree(self):
        stpg = self.stpg

        chromosome = gen_random_walk(stpg)
        tree = UGraph()

        for edge in chromosome:
            v, u = edge
            tree.add_edge(v, u)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'

if __name__ == "__main__" :
    unittest.main()
