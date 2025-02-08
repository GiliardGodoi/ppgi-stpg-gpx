import unittest

from graph.graph import Graph
from graph.util import has_cycle, gg_total_weight, gg_edges_number
from graph.algorithms import kruskal
from graph.disjointsets import DisjointSets, Subset

class TestDisjointSets(unittest.TestCase):

    def tree_example(self):

        tree = Graph()

        tree.add_edge('a', 'b')
        tree.add_edge('a', 'c')
        tree.add_edge('a', 'd')
        tree.add_edge('b', 'e')
        tree.add_edge('b', 'f')
        tree.add_edge('c', 'g')
        tree.add_edge('d', 'h')
        tree.add_edge('d', 'i')
        tree.add_edge('d', 'j')
        tree.add_edge('j', 'k')
        tree.add_edge('j', 'l')

        return tree

    def test_attributes(self):
        obj = Subset(10)
        self.assertTrue(hasattr(obj,"rank"))
        self.assertTrue(hasattr(obj,"parent"))

        DS = DisjointSets()

        self.assertEqual(len(DS), 0)

        for item in range(3,50, 10):
            DS.make_set(item)

        self.assertTrue(hasattr(DS, "make_set"))
        self.assertTrue(hasattr(DS, "find"))
        self.assertTrue(hasattr(DS, "union"))
        self.assertTrue(hasattr(DS, "get_disjoint_sets"))

    def test_inserting_item(self):

        DS = DisjointSets()

        for item in range(3,50, 10):
            DS.make_set(item)

        self.assertEqual(len(DS), 5)
        self.assertEqual(len(DS), len(DS.get_disjoint_sets()))

        with self.assertRaises(ValueError):
            DS.make_set(13)
        ## check ignore_previous
        self.assertTrue(33 in DS)
        DS.make_set(33, ignore_previous=True)

        self.assertTrue(not 171 in DS)
        self.assertFalse(171 in DS)


    def test_no_cycle(self):
        tree = self.tree_example()
        self.assertFalse(has_cycle(tree))

    def test_has_cycle(self):
        tree = self.tree_example()
        tree.add_edge('g', 'a') ## has a cycle
        self.assertTrue(has_cycle(tree))

    def teste_kruskal_mst_algorithm(self):
        '''Kruskal's algorithm uses Disjoint Set under the hook'''
        edges = [
                ('a', 'b', 4), ('a', 'h', 8), ('h', 'b', 11),
                ('h', 'i', 7), ('h', 'g', 1), ('i', 'g', 6),
                ('i', 'c', 2), ('b', 'c', 8),
                ('c', 'f', 4), ('g', 'f', 2),
                ('d', 'f', 14), ('c', 'd', 7),
                ('d', 'e', 9), ('e', 'f', 10),
            ]

        graph = Graph()
        for v, u, w in edges:
            graph.add_edge(v, u, weight=w)

        tree = kruskal(graph)

        nro_edges = gg_edges_number(tree)
        cost = gg_total_weight(tree)

        self.assertEqual(nro_edges, 8)
        self.assertEqual(cost, 37)
        self.assertFalse(has_cycle(graph))


if __name__ == "__main__":
    unittest.main()