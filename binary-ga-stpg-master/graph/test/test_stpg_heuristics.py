import random
import unittest
from collections import deque
from os import path

from graph.graph import Graph
from graph.reader import Reader
from graph.steiner import (prunning_mst, shortest_path,
                           shortest_path_origin_prim,
                           shortest_path_with_origin)


class TestSTPGHeuristicas(unittest.TestCase):

    def setUp(self):
        reader = Reader()
        self.stpg_instance = reader.parser(path.join("datasets", "osti", "b13.stp"))

        self.graph = Graph(vertices = self.stpg_instance.nro_nodes,
                            edges=self.stpg_instance.graph)

        random.seed()


    def test_instance_reading(self):

        stpg = self.stpg_instance

        self.assertEqual(stpg.nro_edges, 125)
        self.assertEqual(stpg.nro_nodes, 100)
        self.assertEqual(stpg.nro_terminals, 17)

        self.assertEqual(stpg.nro_terminals, len(stpg.terminals))
        self.assertEqual(stpg.nro_nodes, len(stpg.graph))

    def test_shortest_path(self):
        graph = self.graph
        stpg = self.stpg_instance

        terminal = random.choice(stpg.terminals)
        gg, cost = shortest_path(graph, terminal, stpg.terminals)

        self.common_cases(gg, cost)

    def test_shortest_path_with_origin(self):

        graph = self.graph
        stpg = self.stpg_instance

        terminal = random.choice(stpg.terminals)
        gg, cost = shortest_path_with_origin(graph, terminal, stpg.terminals)

        self.common_cases(gg, cost)

    def test_shortest_path_origin_prim(self):

        graph = self.graph
        stpg = self.stpg_instance

        terminal = random.choice(stpg.terminals)
        gg, cost = shortest_path_origin_prim(graph, terminal, stpg.terminals)

        self.common_cases(gg, cost)

    def test_prunning_mst(self):

        graph = self.graph
        stpg = self.stpg_instance

        terminal = random.choice(stpg.terminals)
        gg, cost = prunning_mst(graph, terminal, stpg.terminals)

        self.common_cases(gg, cost)


    def common_cases(self, steiner_tree : Graph, cost : int):

        self.assertIsInstance(steiner_tree, Graph)
        self.assertIsInstance(cost, int)
        self.assertGreater(cost,0)

        terminals = set(self.stpg_instance.terminals)

        ## Se o vértice possui grau 1 então é terminal. Mas se for terminal possui grau 1?
        degrees = { k : len(steiner_tree[k]) for k in steiner_tree.edges.keys() }
        for k, v in degrees.items() :
            if v == 1 :
                is_terminal = (k in terminals)
                self.assertTrue(is_terminal)

        all_vertices = set(steiner_tree.vertices)

        self.assertIsInstance(all_vertices, set)
        self.assertEqual(len(all_vertices), len(steiner_tree.vertices))

        ## todos os vertices terminais estao contidos na solução
        tt = terminals - all_vertices
        self.assertFalse(tt)

        ## Existe algum ponto de steiner na solução. Mas sempre isso vai acontecer?
        ss = all_vertices - terminals
        self.assertTrue(ss)

        stpg = self.stpg_instance
        has_cycles = self.check_cycles_dfs(steiner_tree, stpg.terminals[8])
        self.assertFalse(has_cycles)


    def check_cycles_dfs(self, graph, start):
        '''
            Verifica se existe um ciclo em um grafo a partir de um vértice.
            É claro, essa função não foi testada.
        '''
        stack = deque()

        visited = set([start])
        prev = dict()

        stack.append(start)

        has_circle = False

        while stack:
            v = stack.pop()
            visited.add(v)
            for u in graph.adjacent_to(v):
                if u not in visited :
                    stack.append(u)
                    prev[u] = v
                elif not prev[v] == u :
                    has_circle = True

        return has_circle


if __name__ == "__main__" :
    unittest.main()
