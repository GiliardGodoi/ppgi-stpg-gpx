import unittest
from collections import defaultdict
from os import path

from ga4stpg.graph.graph import UndirectedWeightedGraph as Graph
from ga4stpg.graph.graph import _VerticeView
from ga4stpg.graph import ReaderORLibrary


class TestGraphDictionaryDataStructure(unittest.TestCase):

    def test_instanceVerticesEmpty(self):

        graph = Graph()

        self.assertIsInstance(graph,Graph)
        self.assertIsInstance(graph.vertices,_VerticeView)
        self.assertEqual(len(graph.vertices),0)

        self.assertIsInstance(graph.edges,defaultdict)
        self.assertEqual(len(graph.edges),0)

        self.assertFalse(graph.has_node(10))
        self.assertFalse(graph.has_edge(30,45))

        self.assertEqual(graph.weight(40, 40), float("inf"))
        self.assertEqual(graph.weight(5,20),float("inf"))

    def test_verticesAndEdgeInsertion(self):

        graph = Graph()
        self.assertEqual(len(graph.vertices),0)
        self.assertEqual(len(graph.edges),0)

        graph.add_node(4)
        self.assertIn(4, graph.vertices)
        # self.assertNotIn(4,graph.edges)

        graph.add_edge(4,5,weight=30)
        self.assertTrue(graph.has_edge(5,4))
        self.assertTrue(graph.has_node(4))
        self.assertTrue(graph.has_node(5))
        self.assertFalse(graph.has_node(100))

        self.assertIn(5,graph.vertices)
        self.assertIn(4, graph.vertices)
        self.assertIn(4,graph.edges)
        self.assertIn(5,graph.edges)
        self.assertNotIn(100, graph.vertices)
        self.assertNotIn(100,graph.edges)

        self.assertEqual(graph[4][5], 30)
        self.assertEqual(graph[4][5],graph[5][4])
        # self.assertEqual(graph.vertices.count(4), 1)

        self.assertEqual(graph.size(),2)
        self.assertIsInstance(graph[5],dict)
        self.assertIsInstance(graph[4],dict)

        graph.add_edge(6,4,weight=29)
        self.assertTrue(graph.has_edge(4,6))
        self.assertTrue(graph.has_node(6))
        self.assertIn(6,graph.vertices)
        self.assertIn(6,graph.edges)
        self.assertEqual(graph[4][6], 29)
        self.assertEqual(graph[4][6],graph[6][4])
        # self.assertEqual(graph.vertices.count(4), 1)

        graph.add_node(6) # inserting again
        # self.assertEqual(graph.vertices.count(6), 1)

        self.assertFalse(graph.has_edge(4,7))
        self.assertEqual(graph.weight(4,7),float("inf"))

        self.assertEqual(graph.weight(4,4),0)

        self.assertEqual(graph.degree(4),2)
        self.assertEqual(graph.degree(5),1)
        self.assertEqual(graph.degree(6),1)

        graph.add_edge(150, 134, weight=9)
        self.assertEqual(graph[150][134], 9)
        self.assertEqual(graph.weight(134,150), 9)


    def test_ErrorHandle(self):

        graph = Graph()
        graph.add_edge(49, 57, weight=50)
        graph.add_edge(78, 57, weight=41)
        graph.add_edge(49, 8, weight=97)
        graph.add_edge(49, 26, weight=42)

        self.assertEqual(graph[49][26], 42)
        self.assertEqual(graph.weight(49,26), 42)
        self.assertEqual(graph[49][26], graph.edges[49][26])
        self.assertEqual(graph.get(78),{57 : 41})

        self.assertEqual(graph.get(34), dict())
        self.assertEqual(graph[34], dict())
        self.assertNotIn(34, graph)

        with self.assertRaises(KeyError) :
            graph[49][90]


        graph.add_edge(49, 57, weight=78)
        self.assertEqual(graph[49][57],78)
        self.assertEqual(graph.weight(49,57),78, msg="Deveria deixar atualizar?")

        graph.add_edge(49, 49, weight=96)
        self.assertEqual(graph.weight(49,49),0)

        with self.assertRaises(KeyError) :
            graph[49][49]


    def test_Adjacents(self):
        graph = Graph()
        graph.add_edge(49, 57, weight=50)
        graph.add_edge(78, 57, weight=41)
        graph.add_edge(49, 8, weight=97)
        graph.add_edge(49, 26, weight=42)

        adj = [ v for v in graph.adjacent_to(49)]
        self.assertEqual(sorted(adj),[8, 26, 57])

        self.assertIn(49, graph.adjacent_to(adj[1]))

        self.assertEqual(set(graph.adjacent_to(49)), set(graph.edges[49].keys()))
        self.assertIn(26, graph.edges[49].keys())
        self.assertIn(26, graph.adjacent_to(49))
        self.assertNotIn(56,graph.adjacent_to(49))

        from _collections_abc import dict_keys
        self.assertIsInstance(graph.adjacent_to(49, lazy=False), set)
        self.assertNotIsInstance(graph.adjacent_to(49),list)
        self.assertNotIsInstance(graph.adjacent_to(49),dict)
        self.assertNotIsInstance(graph.adjacent_to(49),set)
        self.assertIsInstance(graph.adjacent_to(49, lazy=False),set)

        self.assertEqual(graph.degree(49), 3)
        self.assertEqual(graph.degree(8), 1)
        self.assertEqual(graph.degree(10), 0)

    # @unittest.expectedFailure
    def test_AcessErrors(self):
        '''
        Note that graph[49][90] throw an exception.
        '''
        graph = Graph()
        graph.add_edge(49, 57, weight=50)
        graph.add_edge(78, 57, weight=41)
        graph.add_edge(49, 8, weight=97)
        graph.add_edge(49, 26, weight=42)

        # self.assertIsNone(graph[34],msg="Retorna um dict como default")
        # Esse comportamento é desejavel ?
        # with self.assertRaises(KeyError, msg = "Retorna dict como default") :
        #     graph[34]


    def test_TheSameVerticesInsertion(self):

        graph = Graph()

        self.assertEqual(len(graph.vertices),0)
        self.assertEqual(len(graph.edges),0)

        graph.add_edge(5,5, weight=1)
        self.assertEqual(len(graph.vertices),0)
        self.assertEqual(len(graph.edges),0)
        self.assertFalse(graph.has_node(5))
        self.assertFalse(graph.has_edge(5,5))

    def test_GenerateUndirectEdges(self):
        diretorio_dados = path.join("datasets", "ORLibrary")
        arquivo_dados = "steinb1.txt"
        arquivo = path.join(diretorio_dados, arquivo_dados)

        reader = ReaderORLibrary()

        stp = reader.parser(arquivo)

        graph = stp.graph

        edges = set()

        for e in graph.gen_undirect_edges():
            edges.add(e)

        self.assertEqual(len(edges),stp.nro_edges)

    def test_read_b01(self):
        diretorio_dados = path.join("datasets", "ORLibrary")
        arquivo_dados = "steinb1.txt"
        arquivo = path.join(diretorio_dados, arquivo_dados)

        reader = ReaderORLibrary()

        stp = reader.parser(arquivo)
        terminais = [48, 49, 22, 35, 27, 12, 37, 34, 24]

        self.assertEqual(stp.nro_nodes,50)
        self.assertEqual(stp.nro_edges,63)
        self.assertEqual(stp.nro_terminals,9)
        self.assertEqual(sorted(stp.terminals),sorted(terminais))

        self.assertEqual(stp.graph[17][42],6)
        self.assertEqual(stp.graph[20][40],10)
        #Ordem inversa ao que aparece no arquivo
        self.assertEqual(stp.graph[6][42],9)
        self.assertEqual(stp.graph[13][50],1)

        self.assertIsInstance(stp.nro_nodes,int)
        self.assertIsInstance(stp.nro_edges,int)
        self.assertIsInstance(stp.nro_terminals,int)
        self.assertIsInstance(stp.terminals,set)
        self.assertIsInstance(stp.graph,Graph)

        self.assertEqual(len(stp.graph.vertices), stp.nro_nodes)

        self.assertEqual(stp.name,'B1')
        self.assertEqual(stp.remark,'Sparse graph with random weights')
        self.assertEqual(stp.creator,'J. E. Beasley')
        self.assertEqual(stp.file_name, arquivo_dados)

if __name__ == "__main__":
    unittest.main()
