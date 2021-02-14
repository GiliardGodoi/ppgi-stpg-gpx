from collections import deque
from operator import attrgetter
from random import choice

from ga4stpg.graph import Graph
from ga4stpg.util import compose
from ga4stpg.graph.disjointsets import DisjointSets


class Component:

    def __init__(self, first, second, initialcost=0):
        self.edges = {first : None, second : first}
        self.portal = set()
        self.cost = initialcost

    def add(self, first, second):
        self.edges[second] = first

def connected(g_union : Graph, red : Graph, blue : Graph, start : 'node'):

    linkedlist = deque([start])
    visited = set()
    parents = DisjointSets()

    for v in g_union.vertices:
        parents.make_set(v)

    def chase(main, node, component):

        if (node in red) and (node in blue):
            if node not in visited and node not in linkedlist:
                linkedlist.appendleft(node)

            component.portal.add(node)
            return

        for w in main.adjacent_to(node):
            if w in component.edges:
                continue
            component.add(node, w)
            component.cost += main.W(node, w)
            chase(main, w, component)
        # end for loop
        visited.add(node)

    components_red  = list()
    components_blue = list()

    while linkedlist:
        u = linkedlist.pop()
        visited.add(u)
        for v in g_union.adjacent_to(u):
            if v in visited:
                continue
            if red.has_edge(u,v) and blue.has_edge(u,v):
                linkedlist.append(v)
                parents.union(u, v)

            elif red.has_edge(u,v):
                component = Component(u, v, initialcost=g_union.W(u,v))
                chase(red, v, component)
                chase(red, u, component)
                components_red.append(component)

            elif blue.has_edge(u,v):
                component = Component(u, v, initialcost=g_union.W(u,v))
                chase(blue, v, component)
                chase(blue, u, component)
                components_blue.append(component)
        # end for loop
    # end while loop
    return components_red, components_blue, parents


class PXtree:

    def __init__(self, stpg):
        self.STPG = stpg
        self.terminals = list(stpg.terminals)

    def __call__(self, red : Graph, blue : Graph):

        start = choice(self.terminals)

        g_union, g_common, g_star = compose(red, blue)
        first, second, previous = connected(g_union, red, blue, start)

        matches = dict()

        for component in first:
            ss = frozenset(previous.find(v) for v in component.portal)
            matches[ss] = [component]

        non_second = list()

        for component in second:
            ss = frozenset(previous.find(v) for v in component.portal)
            if ss in matches:
                matches[ss].append(component)
            else:
                non_second.append(component)


        get_cost = attrgetter('cost')

        success = 0
        fail = 0

        non_first = list()
        minimum_cost = list()

        for key, components in matches.items():
            if len(components) >= 2:
                minimum_cost.append(min(components, key=get_cost))
                success += 1
            else:
                non_first.append(components.pop())
                fail += 1

        total_first = 0
        for c in non_first:
            total_first += c.cost

        total_second = 0
        for c in non_second:
            total_second += c.cost

        if total_second < total_first:
            selected = non_second
        else:
            selected = non_first

        for component in minimum_cost:
            for v, u in component.edges.items():
                if u is None:
                    continue
                w = self.STPG.graph.W(v,u)
                g_common.add_edge(v,u,weight=w)

        for component in selected:
            for v, u in component.edges.items():
                if u is None:
                    continue
                w = self.STPG.graph.W(v,u)
                g_common.add_edge(v,u,weight=w)

        return g_common, success, fail


def test_0():

    aa = Graph(edges={
        'A' : {'B' : 1, 'C' : 1},
        'B' : {'A' : 1, 'D' : 1, 'E' : 1},
        'D' : {'B' : 1},
        'C' : {'A' : 1},
        'E' : {'B' : 1, 'G' : 1},
        'G' : {'E' : 1, 'H' : 1},
        'H' : {'G' : 1}
    })

    bb = Graph(edges={
        'A' : {'B' : 1, 'C' : 1},
        'B' : {'A' : 1, 'D' : 1},
        'D' : {'B' : 1},
        'C' : {'A' : 1, 'F' : 1},
        'F' : {'C' : 1, 'G' : 1},
        'G' : {'F' : 1, 'H' : 1},
        'H' : {'G' : 1}
    })

    g_union, g_common, g_star = compose(aa, bb)

    first, second, previous = connected(g_union, aa, bb, 'A')

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

    crossover = PXtree(stpg)
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
    test_1()