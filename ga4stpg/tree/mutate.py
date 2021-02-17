from random import choice, randint, sample, shuffle

from ga4stpg.graph import UGraph
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
    pass