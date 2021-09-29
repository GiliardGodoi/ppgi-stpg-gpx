from random import choice, randint, shuffle
from collections import deque

from ga4stpg.graph import UGraph, UndirectedWeightedGraph as UWGraph
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.priorityqueue import PriorityQueue

class ReplaceByRandomEdge:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, treegraph : UGraph):

        GRAPH = self.stpg.graph
        disjointset = DisjointSets()
        result = UGraph()

        for v in treegraph.vertices:
            disjointset.make_set(v)

        # remove edge
        edges = [edge for edge in treegraph.gen_undirect_edges()]
        index = randint(0, len(edges))
        for i, edge in enumerate(edges):
            if index != i:
                result.add_edge(*edge)
                disjointset.union(*edge)

        candidates = list()
        components = disjointset.get_disjoint_sets()

        lesser_idx = min(components, key=lambda key: len(components[key]))
        keys = components.keys() - set([lesser_idx])

        # replace edge
        lesser_component = components[lesser_idx]
        for key in keys:
            other_component = components[key]
            for v in lesser_component:
                for w in GRAPH.adjacent_to(v):
                    if w in other_component:
                        candidates.append((v, w))

            shuffle(candidates)
            while candidates:
                v, w = candidates.pop()
                if disjointset.find(v) != disjointset.find(w):
                    result.add_edge(v, w)
                    disjointset.union(v, w)
                    break

        return result


class PrimBasedMutation:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, treegraph : UGraph):

        GRAPH = self.stpg.graph
        vertices = set(treegraph.vertices)

        # Build the subgraph induced by the nodes in treegraph
        subgraph = UWGraph()
        for v in vertices:
            for u in GRAPH.adjacent_to(v):
                if u in vertices:
                    weigth = GRAPH.weight(v, u)
                    subgraph.add_edge(v, u, weight=weigth)

        # Compute the Prim MST for the subgraph
        mst = UGraph()
        queue = PriorityQueue()

        start = choice(tuple(vertices))

        for next_node, weight in subgraph.edges[start].items():
            queue.push(weight,(start, next_node))

        while queue:
            node_start, node_end = queue.pop()
            if node_end not in mst:
                mst.add_edge(node_start, node_end)

                for next_node, weight in subgraph.edges[node_end].items():
                    queue.push(weight,(node_end, next_node))

        return mst


class Prunning:

    def __init__(self, stpg):
        self.terminals = stpg.terminals.copy()

    def __call__(self, treegraph : UGraph):

        terminals = self.terminals
        result = UGraph()
        for v, u in treegraph.gen_undirect_edges():
            result.add_edge(v, u)

        leaves = deque([v for v in result.vertices if (v not in terminals) and (result.degree(v) == 1)])

        while leaves:
            v = leaves.pop()
            for w in result.adjacent_to(v):
                if (w not in terminals) and (result.degree(w) == 2):
                    leaves.appendleft(w)
            result.remove_node(v)

        return result

class InsertRandomVertice:

    def __init__(self, stpg):
        self.stpg = stpg


    def __call__(self, treegraph : UGraph):
        pass

class ReplaceMultiplusEdges:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, treegraph : UGraph):
        pass