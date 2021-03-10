from random import sample, shuffle

from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets

class GenerateBasedPrimRST:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self):

        result = UGraph()
        terminals = self.stpg.terminals.copy()
        GRAPH = self.stpg.graph
        edges = set() # or is it better a list?
        vi = sample(range(1, self.stpg.nro_nodes+1), k=1)[0]

        terminals.discard(vi)
        for w in GRAPH.adjacent_to(vi):
            edges.add((vi, w))

        while terminals and edges:
            edge = sample(edges, k=1)[0] # need to ensure randomness
            v, w = edge
            if w not in result:
                terminals.discard(w)
                result.add_edge(v, w)
                for u in GRAPH.adjacent_to(w):
                    if u not in result:
                        edges.add((w, u))
            edges.remove(edge) # to remove from a list it can take O(n)

        return result


class GenerateBasedKruskalRST:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self):
        result = UGraph()
        done = DisjointSets()
        edges = [(u, v) for u, v in self.stpg.graph.gen_undirect_edges()]

        shuffle(edges)

        for v in self.stpg.terminals:
            done.make_set(v)

        while edges and len(done.get_disjoint_sets()) > 1:
            edge = edges.pop()
            y, z = edge[0], edge[1]
            if y not in done: done.make_set(y)
            if z not in done: done.make_set(z)
            if done.find(y) != done.find(z):
                result.add(y, z)
                done.union(y, z)

        return result


class GenerateBasedRandomWalk:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self):

        GRAPH = self.stpg.graph
        terminals = self.stpg.terminals.copy()
        result = UGraph()

        v = terminals.pop()
        while terminals:
            adjacents = GRAPH.adjacent_to(v, lazy=False)
            u = sample(adjacents, k=1)[0]
            if u not in result:
                result.add_edge(v, u)
                terminals.discard(u)
            v = u

        return result
