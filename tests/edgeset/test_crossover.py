import unittest
from os import path

from ga4stpg.edgeset import EdgeSet
from ga4stpg.edgeset.crossover import (CrossoverKruskalRST,
                                       CrossoverPrimRST,
                                       CrossoverRandomWalkRST)
from ga4stpg.edgeset.generate import (gen_random_kruskal,
                                      gen_random_prim,
                                      gen_random_walk)
from ga4stpg.graph import ReaderORLibrary, UGraph
from ga4stpg.graph.util import is_steiner_tree


class TestCrossoverKruskalRSTBased(unittest.TestCase):

    def test_if_return_an_edgeset(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)

        crossover = CrossoverKruskalRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)

        self.assertIsInstance(parent_a, EdgeSet)
        self.assertIsInstance(parent_b, EdgeSet)

        offspring = crossover(parent_a, parent_b)

        self.assertIsInstance(offspring, EdgeSet)
        self.assertFalse(offspring is parent_a)
        self.assertFalse(offspring is parent_b)

        self.assertNotEqual(offspring, parent_a)
        self.assertNotEqual(offspring, parent_b)

    def test_if_has_all_terminals(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)
        terminals = stpg.terminals

        crossover = CrossoverKruskalRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)
        offspring = crossover(parent_a, parent_b)

        vertices = set([v for v in offspring.vertices])
        self.assertTrue(terminals.issubset(vertices))

    def test_if_is_it_a_tree(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)

        crossover = CrossoverKruskalRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)
        offspring = crossover(parent_a, parent_b)

        tree = UGraph()
        for edge in offspring:
            u, v = edge[0], edge[1]
            tree.add_edge(u, v)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'


class TestCrossoverPrimRSTBased(unittest.TestCase):

    def test_if_return_an_edgeset(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)

        crossover = CrossoverPrimRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)

        self.assertIsInstance(parent_a, EdgeSet)
        self.assertIsInstance(parent_b, EdgeSet)

        offspring = crossover(parent_a, parent_b)

        self.assertIsInstance(offspring, EdgeSet)
        self.assertFalse(offspring is parent_a)
        self.assertFalse(offspring is parent_b)

        self.assertNotEqual(offspring, parent_a)
        self.assertNotEqual(offspring, parent_b)

    def test_if_has_all_terminals(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)
        terminals = stpg.terminals

        crossover = CrossoverPrimRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)
        offspring = crossover(parent_a, parent_b)

        vertices = set([v for v in offspring.vertices])
        self.assertTrue(terminals.issubset(vertices))

    def test_if_is_it_a_tree(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)

        crossover = CrossoverPrimRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)
        offspring = crossover(parent_a, parent_b)

        tree = UGraph()
        for edge in offspring:
            u, v = edge[0], edge[1]
            tree.add_edge(u, v)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'


class TestCrossoverRandomWalkBased(unittest.TestCase):

    def test_if_return_an_edgeset(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)

        crossover = CrossoverRandomWalkRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)

        self.assertIsInstance(parent_a, EdgeSet)
        self.assertIsInstance(parent_b, EdgeSet)

        offspring = crossover(parent_a, parent_b)

        self.assertIsInstance(offspring, EdgeSet)
        self.assertFalse(offspring is parent_a)
        self.assertFalse(offspring is parent_b)

        self.assertNotEqual(offspring, parent_a)
        self.assertNotEqual(offspring, parent_b)

    def test_if_has_all_terminals(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)
        terminals = stpg.terminals

        crossover = CrossoverRandomWalkRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)
        offspring = crossover(parent_a, parent_b)

        vertices = set([v for v in offspring.vertices])
        self.assertTrue(terminals.issubset(vertices))

    def test_if_is_it_a_tree(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        stpg  = ReaderORLibrary().parser(filename)

        crossover = CrossoverRandomWalkRST(stpg)

        parent_a = gen_random_walk(stpg)
        parent_b = gen_random_walk(stpg)
        offspring = crossover(parent_a, parent_b)

        tree = UGraph()
        for edge in offspring:
            u, v = edge[0], edge[1]
            tree.add_edge(u, v)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'



if __name__ == "__main__" :
    unittest.main()
