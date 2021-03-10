from collections import deque

from ga4stpg.graph import Graph, SteinerTreeProblem
from ga4stpg.util import record_parents

class SimpliestPX:
    '''
    Operação de Cruzamento baseado em avaliação das partições.
    1. Identifica as arestas comuns e as arestas não comuns, formando componentes conexas.
    2. Arestas comuns são transmitidas para os descendentes.
    3. Arestas não comuns formam partições (componentes conexas) que serão avaliadas isoladamente.
    4. Para cada partição (passo 3) compara o peso das arestas de cada um dos pais.
    O subconjunto de arestas de menor peso (custo) será transmitido ao descendente.
    Notes:
    Este procedimento não garante que todos os descendentes serão factíveis.
    '''

    def __init__(self, STPG : SteinerTreeProblem):
        self.STPG = STPG
        self.GRAPH = STPG.graph

    def __call__(self, subtree_a : Graph, subtree_b : Graph, **kwargs):
        return self.operator(subtree_a, subtree_b)


    def operator(self, subtree_a : Graph, subtree_b : Graph):
        '''Implementa um operador de crossover simplificado'''

        graph_child = Graph()
        graph_partition = Graph()

        A_vertices = set()
        B_vertices = set()

        for v, u in subtree_a.gen_undirect_edges():
            weight = subtree_a.weight(v,u)
            if subtree_b.has_edge(v,u):
                graph_child.add_edge(v, u, weight=weight)
            else:
                A_vertices.add(v)
                A_vertices.add(u)
                graph_partition.add_edge(v, u, weight=weight)

        for v, u in subtree_b.gen_undirect_edges():
            weight = subtree_b.weight(v, u)
            if not subtree_a.has_edge(v, u):
                B_vertices.add(v)
                B_vertices.add(u)
                graph_partition.add_edge(v, u, weight=weight)

        AandB_vertices = A_vertices.intersection(B_vertices)
        partitions = list()

        while AandB_vertices:
            start = AandB_vertices.pop()
            partition, visited = self.__dfs__(graph_partition,subtree_a, subtree_b, start)

            if partition["A"]["cost"] <= partition["B"]["cost"] :
                partitions.append(partition["A"])
            else :
                partitions.append(partition["B"])

            AandB_vertices = AandB_vertices.difference(visited) # estao em AandB_vertices mas não estão em visited O(n + m)


        for partition in partitions :
            for v, u in partition["edges"]:
                graph_child.add_edge(v, u, weight=self.GRAPH.weight(v, u))

        return graph_child

    def __dfs__(self, uncommon_graph : Graph, Atree : Graph, Btree : Graph, start : 'Node'):

        vertices_done = set()
        stack = deque([start])

        partition = {
                "A" : {"edges": set(), "cost" : 0 },
                "B" : {"edges": set(), "cost" : 0 }
            }

        while stack:
            node = stack.pop()
            vertices_done.add(node)

            for adj in uncommon_graph.adjacent_to(node):

                if adj not in vertices_done:
                    if Atree.has_edge(node, adj):
                        partition["A"]["edges"].add((node, adj))
                        partition["A"]["cost"] += uncommon_graph.weight(node, adj)
                    elif Btree.has_edge(node, adj):
                        partition["B"]["edges"].add((node, adj))
                        partition["B"]["cost"] += uncommon_graph.weight(node, adj)

                    stack.append(adj)

        return partition, vertices_done