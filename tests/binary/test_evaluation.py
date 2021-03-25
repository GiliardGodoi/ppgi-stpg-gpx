import unittest
from os import path

from ga4stpg.binary.coder import Coder
from ga4stpg.binary.evaluation import EvaluateKruskalBased
from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.algorithms import prim, kruskal
from ga4stpg.graph.graph import UndirectedGraph as UGraph
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.util import is_steiner_tree

class TestEvaluateBinary(unittest.TestCase):

    def setUp(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb11.txt')
        self.stpg  = ReaderORLibrary().parser(filename)

    def test_basicEvaluateKruskalBasedProperties(self):

        evaluator = EvaluateKruskalBased(self.stpg)

        self.assertIsInstance(evaluator, EvaluateKruskalBased)
        self.assertTrue(callable(evaluator))
        self.assertTrue(hasattr(evaluator, 'vertices_from_chromosome'))

        self.assertTrue(callable(evaluator.penality_function))
        self.assertEqual(evaluator.penality_function(1), 0)
        self.assertEqual(evaluator.penality_function(7), 6_000)

    def test_vertices_from_chromossome_all_nodes(self):

        stpg = self.stpg
        graph_vertices = set(self.stpg.graph.vertices)

        evaluator = EvaluateKruskalBased(self.stpg)
        expected_lenght = stpg.nro_nodes - stpg.nro_terminals
        chromosome = '1' * expected_lenght

        evaluator_vertices = evaluator.vertices_from_chromosome(chromosome)

        self.assertEqual(graph_vertices, evaluator_vertices)

    def test_compare_with_prim(self):
        stpg  = self.stpg
        graph = self.stpg.graph

        expected_lenght = stpg.nro_nodes - stpg.nro_terminals
        chromosome = '1' * expected_lenght

        evaluator = EvaluateKruskalBased(stpg)

        evaluator_cost, qtd_partitions = evaluator(chromosome)

        dict_tree, prim_cost = prim(graph,1)

        self.assertIsInstance(dict_tree, dict)
        self.assertIsInstance(qtd_partitions, int)
        self.assertEqual(qtd_partitions, 1)
        self.assertEqual(evaluator_cost, prim_cost)

    def test_compare_with_kruskal(self):
        stpg  = self.stpg
        graph = self.stpg.graph

        mst_kruskal = kruskal(graph=graph)

        expected_lenght = stpg.nro_nodes - stpg.nro_terminals
        chromosome = '1' * expected_lenght

        evaluator = EvaluateKruskalBased(stpg)
        evaluator_cost, qtd_partitions = evaluator(chromosome)

        mst_cost = 0
        for v, u in mst_kruskal.gen_undirect_edges():
            mst_cost += mst_kruskal.weight(v, u)

        self.assertIsInstance(qtd_partitions, int)
        self.assertEqual(qtd_partitions, 1)

        self.assertEqual(evaluator_cost, mst_cost)

    def test_vertices_from_chromossome_random_chromosome(self):
        filename = path.join('tests', 'data', 'test1.txt')
        stpg  = ReaderORLibrary().parser(filename)

        self.assertIsNotNone(stpg)
        self.assertEqual(stpg.nro_nodes, 7)
        self.assertEqual(stpg.nro_edges, 11)
        self.assertEqual(stpg.nro_terminals, 2)
        self.assertEqual(stpg.terminals, set([1, 5]))

        evaluator = EvaluateKruskalBased(stpg)

        chromosome = '11110'
        vertices_from = evaluator.vertices_from_chromosome(chromosome)
        expected_vertices = set([1, 2, 3, 4, 5, 6])
        self.assertEqual(vertices_from, expected_vertices)

        chromosome = '11111'
        vertices_from = evaluator.vertices_from_chromosome(chromosome)
        expected_vertices = set([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(vertices_from, expected_vertices)


        chromosome = '10101'
        vertices_from = evaluator.vertices_from_chromosome(chromosome)
        expected_vertices = set([1, 5, 2, 4, 7])
        self.assertEqual(vertices_from, expected_vertices)

    def test_decoder_random_chromosome(self):
        filename = path.join('tests', 'data', 'test1.txt')
        stpg  = ReaderORLibrary().parser(filename)

        evaluator = EvaluateKruskalBased(stpg)

        chromosome = '11110'
        vertices_from = evaluator.vertices_from_chromosome(chromosome)
        expected_vertices = set([1, 2, 3, 4, 5, 6])
        self.assertEqual(vertices_from, expected_vertices)

        coder = Coder(stpg)
        subgraph = coder.binary2treegraph(chromosome)

        for v, u in subgraph.gen_undirect_edges():
            self.assertTrue(stpg.graph.has_edge(v, u))

        self.assertFalse(subgraph.has_edge(1, 2))
        self.assertFalse(subgraph.has_edge(6, 4))

        self.assertTrue(subgraph.has_edge(1, 3))
        self.assertTrue(subgraph.has_edge(3, 2))
        self.assertTrue(subgraph.has_edge(5, 4))
        self.assertTrue(subgraph.has_edge(6, 5))
        self.assertTrue(subgraph.has_edge(2, 5))

        self.assertFalse(subgraph.has_node(7))
        #não existe mesmo
        self.assertFalse(subgraph.has_edge(7, 1))
        self.assertFalse(subgraph.has_edge(7, 5))
        self.assertFalse(subgraph.has_edge(3, 4))

        # não existe no subgrafo
        self.assertFalse(subgraph.has_edge(7, 2))
        self.assertFalse(subgraph.has_edge(7, 3))
        self.assertFalse(subgraph.has_edge(7, 4))
        self.assertFalse(subgraph.has_edge(7, 6))

    def test_evaluate_test1(self):
        filename = path.join('tests', 'data', 'test1.txt')
        stpg  = ReaderORLibrary().parser(filename)

        evaluator = EvaluateKruskalBased(stpg)
        chromosome = '11110'
        evaluator_cost, qtd_partitions = evaluator(chromosome)

        self.assertEqual(qtd_partitions, 1)
        self.assertEqual(evaluator_cost, 33)

    def test_evaluate_test2(self):
        filename = path.join('tests', 'data', 'test2.txt')
        stpg  = ReaderORLibrary().parser(filename)

        evaluator = EvaluateKruskalBased(stpg)
        chromosome = '11110'
        evaluator_cost, qtd_partitions = evaluator(chromosome)

        self.assertEqual(qtd_partitions, 2)
        self.assertEqual(evaluator_cost, 1021)

    def test_evaluate_steinb1(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb1.txt')

        stpg  = ReaderORLibrary().parser(filename)
        evaluator = EvaluateKruskalBased(stpg, penality_function=lambda k : (k-1) * 100)

        chromosomes =[
            ("00000010000000001011000110001100010100010", 82),
            ("00011100101110110011011111001110111000111", 362),
            ("11111111001011010111100110001101111110011", 209),
            ("10011010001011001111111111101101110111011", 166),
            ("10000010000000001011000111001100010101011", 100),
            ("00000010000010011011000111001100010101010", 97),
            ("00000010001000000011000111001100010001010", 95),
            ("00000010000011001011000111001100010100010", 92)
        ]

        for chromosome, expected_value in chromosomes:
            evaluator_cost, _ = evaluator(chromosome)
            self.assertEqual(expected_value, evaluator_cost)

    def test_best_solution_is_steiner_tree(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb1.txt')
        stpg  = ReaderORLibrary().parser(filename)
        coder = Coder(stpg)
        chromosome = "00000010000000001011000110001100010100010"

        subgraph = coder.binary2treegraph(chromosome)

        result, _ = is_steiner_tree(subgraph, stpg)

        self.assertTrue(result)


    def test_EvaluateZeroChromossome(self):
        stpg  = self.stpg
        graph = self.stpg.graph
        nro_terminals = stpg.nro_terminals
        terminals = stpg.terminals

        disset = DisjointSets()
        for v in terminals:
            disset.make_set(v)

        edges_sum = 0
        done = set()
        for t in terminals:
            done.add(t)
            for v in graph.adjacent_to(t):
                if v in terminals and v not in done:
                    disset.union(t, v)
                    edges_sum += graph.weight(t, v)

        qtd_disjoint_sets = len(disset.get_disjoint_sets())

        expected_lenght = stpg.nro_nodes - stpg.nro_terminals
        chromosome = '0' * expected_lenght

        evaluator = EvaluateKruskalBased(stpg)

        evaluator_cost, qtd_partitions = evaluator(chromosome)

        self.assertEqual(evaluator_cost, ((qtd_partitions - 1) * 1_000) + edges_sum)
        self.assertEqual(evaluator_cost, ((qtd_disjoint_sets - 1) * 1_000) + edges_sum)
        self.assertEqual(qtd_partitions, qtd_disjoint_sets)

if __name__ == "__main__" :
    unittest.main()