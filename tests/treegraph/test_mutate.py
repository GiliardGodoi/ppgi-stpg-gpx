import unittest
from os import path
from random import choice

from ga4stpg.graph import UGraph, UWGraph
from ga4stpg.graph.algorithms import prim
from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mutate import ReplaceByRandomEdge, PrimBasedMutation, Prunning

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


class TestPrimBasedMutation(unittest.TestCase):

    def test_if_works(self):
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        filename = path.join('datasets', 'ORLibrary', filename)
        stpg  = ReaderORLibrary().parser(filename)

        generator = GenerateBasedRandomWalk(stpg)
        mutator = PrimBasedMutation(stpg)
        prunner = Prunning(stpg)

        before = generator()

        self.assertIsInstance(before, UGraph)
        _, response = is_steiner_tree(before, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])

        after = mutator(before)

        self.assertIsInstance(after, UGraph)
        after_after = prunner(after)

        _, response = is_steiner_tree(after_after, stpg)
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_leaves_are_terminals'])
        self.assertTrue(response['all_terminals_in'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])

    def test_evaluation_cost(self):
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        filename = path.join('datasets', 'ORLibrary', filename)
        stpg  = ReaderORLibrary().parser(filename)

        generator = GenerateBasedRandomWalk(stpg)
        mutator = PrimBasedMutation(stpg)
        evaluator = EvaluateTreeGraph(stpg)

        before = generator()
        after = mutator(before)
        eval_cost, partitions = evaluator(after)

        self.assertEqual(partitions, 1)
        self.assertGreater(eval_cost, 0)

        subgraph = UWGraph()
        vertices = set(before.vertices)
        graph = stpg.graph

        for v in vertices:
            for u in graph.adjacent_to(v):
                if u in vertices:
                    subgraph.add_edge(v, u, weight=graph.weight(v, u))


        _, prim_cost = prim(subgraph, choice(tuple(stpg.terminals)))

        self.assertEqual(prim_cost, eval_cost)


class TestPrunningMutation(unittest.TestCase):

    def test_if_works(self):
        possibles = [ f'steinb{ii}.txt' for ii in range(10, 19)]
        filename = choice(possibles)
        filename = path.join('datasets', 'ORLibrary', filename)
        stpg  = ReaderORLibrary().parser(filename)

        generator = GenerateBasedRandomWalk(stpg)
        prunner = Prunning(stpg)

        before = generator()
        after = prunner(before)

        test, response = is_steiner_tree(after, stpg)
        self.assertTrue(test)
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_leaves_are_terminals'])
        self.assertTrue(response['all_terminals_in'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
