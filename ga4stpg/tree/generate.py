from random import sample, shuffle, randrange, choice
from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets

class GenerateBasedPrimRST:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self):

        result = UGraph()
        terminals = self.stpg.terminals.copy()
        GRAPH = self.stpg.graph
        edges = list() # or is it better a list?
        vi = choice(range(1, self.stpg.nro_nodes+1))
        terminals.discard(vi)

        for w in GRAPH.adjacent_to(vi):
            edges.append((vi, w))

        while terminals and edges:
            idx = randrange(0, len(edges))
            v, w = edges.pop(idx) # need to ensure randomness
            if w not in result:
                terminals.discard(w)
                result.add_edge(v, w)
                for u in GRAPH.adjacent_to(w):
                    if u not in result:
                        edges.append((w, u))
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
                result.add_edge(y, z)
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
