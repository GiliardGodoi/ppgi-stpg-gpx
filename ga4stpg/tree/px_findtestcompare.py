from collections import defaultdict, deque
from operator import attrgetter
from random import choice

from ga4stpg.graph import Graph
from ga4stpg.graph.disjointsets import DisjointSets

def compose(red : Graph, blue : Graph):
    '''
    Parameters:
    ----------
        red, blue : Graph

    Return:
    -------
        g_union : Graph
        g_common : Graph
        g_star : Graph
    '''

    g_union  = Graph()
    g_common = Graph()
    g_star   = Graph()

    for v, u in red.gen_undirect_edges():
        g_union.add_edge(v,u)

        if not blue.has_edge(v,u):
            g_star.add_edge(v,u)

    for v, u in blue.gen_undirect_edges():
        g_union.add_edge(v,u)

        if red.has_edge(v,u):
            w = red.W(v,u)
            g_common.add_edge(v,u,weight=w)
        else:
            g_star.add_edge(v,u)


    return g_union, g_common, g_star

class Component:

    def __init__(self):
        self.edges = set()
        self.portal = set()
        self.cost = 0

    def add(self, v, u):
        self.edges.add((v, u))

class PX_FindTestCompare:
    '''
    Class: PX_FindTestCompare
        Find a partition in g_star graph.
        Test if a partition is recombinant.
        Compare each subtree in a partition and chose that with the smallest cost.
    '''
    def __init__(self, stpg):
        self.STPG = stpg

    def _merge(self, child : Graph, component : Component):

        for v, u in component.edges:
            child.add_edge(v,u, weight=self.STPG.graph.W(v,u))

    def __call__(self, red : Graph, blue : Graph):

        visited = set()
        partition_graph = {'red' : Component(), 'blue' : Component() }

        g_union, g_child, g_star = compose(red, blue)

        def belong_both(node):
            return red.has_node(node) and blue.has_node(node)

        def chase(node, previous, red_component, blue_component):

            if node in visited:
                return

            else:
                visited.add(node)

                for v in g_star.adjacent_to(node):
                    if v == previous:
                        continue

                    if red.has_edge(node, v):
                        red_component.add(node, v)
                        red_component.cost += self.STPG.graph.W(node, v)

                    elif blue.has_edge(node, v):
                        blue_component.add(node, v)
                        blue_component.cost += self.STPG.graph.W(node, v)

                    chase(v, node, red_component, blue_component)

        for s in g_star.vertices:
            if belong_both(s) and (s not in visited):
                red_one = Component()
                blue_one = Component()

                print('one component')

                chase(s, None, red_one, blue_one)

                if red_one.portal == blue_one.portal:
                    # ambas as partições possuem os mesmos vértices portais
                    if red_one.cost < blue_one.cost:
                        self._merge(g_child, red_one)

                    elif blue_one.cost < red_one.cost:
                        self._merge(g_child, blue_one)

                    # if blue_one.cost == red_one.cost
                    elif len(red_one.edges) < len(blue_one.edges):
                        self._merge(g_child, red_one)

                    # same cost and same number of edges
                    else :
                        self._merge(g_child, blue_one)

                else:
                # the components have different portals vertices
                # add to the graph partition
                    partition_graph['red'].edges.update(red_one.edges)
                    partition_graph['red'].cost += red_one.cost

                    partition_graph['blue'].edges.update(blue_one.edges)
                    partition_graph['blue'].cost += blue_one.cost

        if partition_graph['red'].cost < partition_graph['blue'].cost:
            self._merge(g_child, partition_graph['red'])

        elif partition_graph['blue'].cost < partition_graph['red'].cost:
            self._merge(g_child, partition_graph['blue'])

        elif len(partition_graph['red'].edges) < len(partition_graph['blue'].edges):
            self._merge(g_child, partition_graph['red'])

        else:
            self._merge(g_child, partition_graph['blue'])

        return g_child


def test_1():
    from os import path
    from random import sample
    from ga4stpg.graph import ReaderORLibrary

    from ga4stpg.graph.steiner import (prunning_mst, shortest_path,
                            shortest_path_origin_prim,
                            prunning_kruskal_mst,
                            shortest_path_with_origin)
    from ga4stpg.graph.util import (is_steiner_tree,
                                has_cycle,
                                gg_total_weight)
    dataset_file = 'steinc5.txt'

    csv_output = 'resultado.csv'
    graphs_output = 'grafos.pickle'

    file = path.join('datasets','ORLibrary', dataset_file)

    assert path.exists(file), "Arquivo especificado não existe"

    reader = ReaderORLibrary()
    stpg = reader.parser(file)
    vertices = list(stpg.graph.vertices)

    crossover = PX_FindTestCompare(stpg)
    v, u = sample(vertices, 2)

    aa, a_cost = shortest_path_with_origin(stpg.graph, v, stpg.terminals)
    bb, b_cost = shortest_path_with_origin(stpg.graph, u, stpg.terminals)

    child = crossover(bb, aa)
    c_cost = gg_total_weight(child)

    print(a_cost, b_cost, c_cost)

    print(is_steiner_tree(aa, stpg))
    print(is_steiner_tree(bb, stpg))
    print(is_steiner_tree(child, stpg))

    return aa, bb, child

if __name__ == "__main__":
    from graph.util import (is_steiner_tree, has_cycle)

    aa, bb, cc = test_1()
