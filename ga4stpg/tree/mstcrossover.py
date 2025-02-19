from random import choice, randrange, sample

from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.priorityqueue import PriorityQueue

class CrossoverPrimRST:

    def __init__(self, stpg):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red : UGraph, blue : UGraph):
        assert isinstance(red, UGraph), f'red parent must be UGraph. Given {type(red)}'
        assert isinstance(blue, UGraph), f'blue parent must be UGraph. Given {type(blue)}'

        union_g = UGraph()
        for v, u in red.gen_undirect_edges():
            union_g.add_edge(v ,u)
        for v, u in blue.gen_undirect_edges():
            union_g.add_edge(v, u)

        terminals = self.terminals.copy()
        done = set()
        result = UGraph()
        candidates_edges = list()

        vi = terminals.pop()
        done.add(vi)
        for u in union_g.adjacent_to(vi):
            candidates_edges.append((vi, u))

        while candidates_edges and terminals:
            idx = randrange(0, len(candidates_edges))
            v, w = candidates_edges.pop(idx)
            if w not in done:
                done.add(w)
                result.add_edge(v, w)
                terminals.discard(w)
                for u in union_g.adjacent_to(w):
                    if u not in done:
                        candidates_edges.append((w, u))

        return result


class CrossoverGreedyPrim:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, red : UGraph, blue : UGraph):

        f_weight = lambda v, u : self.stpg.graph.weight(v, u)

        union_g = UGraph()
        for v, u in red.gen_undirect_edges():
            union_g.add_edge(v ,u)

        for v, u in blue.gen_undirect_edges():
            union_g.add_edge(v, u)

        queue = PriorityQueue()
        start = choice(tuple(self.stpg.terminals))

        for u in union_g.adjacent_to(start):
            queue.push(f_weight(start, u), (start, u))

        result = UGraph()
        while queue:
            start, end = queue.pop()
            if end not in result:
                result.add_edge(start, end)
                for w in union_g.adjacent_to(end):
                    queue.push(f_weight(end, w), (end, w))

        return result


class CrossoverRelativeGreedyPrim:

    def __init__(self, stpg):
        self.GRAPH = stpg.graph

    def __call__(self, red : UGraph, blue : UGraph):

        f_weight = lambda v, u : self.GRAPH.weight(v, u)

        g_union = UGraph()
        for v, u in red.gen_undirect_edges():
            g_union.add_edge(v, u)
        for v, u in blue.gen_undirect_edges():
            g_union.add_edge(v, u)

        vertices = set(g_union.vertices)
        queue = PriorityQueue()
        start = choice(tuple(vertices))
        for u in g_union.adjacent_to(start):
            queue.push(f_weight(start, u), (start, u))

        leftover_edges = set()
        result = UGraph()
        while queue:

            if len(queue) > 1:
                s = choice([1, 2])
            else:
                s = 1

            i = 0
            while i != s:
                start, end = queue.pop()
                i += 1
                if i < s:
                    leftover_edges.add((start, end))

            if end not in result:
                result.add_edge(start, end)
                for w in g_union.adjacent_to(end):
                    queue.push(f_weight(end, w), (end, w))

            if not queue and leftover_edges:
                for v, u in leftover_edges:
                    if (v not in result) or (u not in result):
                        queue.push(f_weight(v, u), (v, u))

        return result


class CrossoverKruskalRST:
    def __init__(self, stpg):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red, blue):
        assert isinstance(red, UGraph), f'red parent must be UGraph. Given {type(red)}'
        assert isinstance(blue, UGraph), f'blue parent must be UGraph. Given {type(blue)}'

        done = DisjointSets()

        union_g = UGraph()
        for v, u in red.gen_undirect_edges():
            union_g.add_edge(v ,u)
        for v, u in blue.gen_undirect_edges():
            union_g.add_edge(v, u)

        for v in union_g.vertices:
            done.make_set(v)

        all_edges = list()
        for edge in union_g.gen_undirect_edges():
            all_edges.append(edge)

        result = UGraph()
        while all_edges and len(done.get_disjoint_sets()) > 1:
            idx = randrange(0, len(all_edges))
            v, u = all_edges.pop(idx)
            if done.find(v) != done.find(u):
                result.add_edge(v, u)
                done.union(v, u)

        return result


class CrossoverRandomWalkRST:

    def __init__(self, stpg):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red : UGraph, blue : UGraph):
        assert isinstance(red, UGraph), f'red parent must be UGraph. Given {type(red)}'
        assert isinstance(blue, UGraph), f'blue parent must be UGraph. Given {type(blue)}'

        terminals = self.terminals.copy()
        union_g = UGraph()
        for v, u in red.gen_undirect_edges():
            union_g.add_edge(v ,u)
        for v, u in blue.gen_undirect_edges():
            union_g.add_edge(v, u)

        done = set()
        result = UGraph()

        v = terminals.pop()
        while terminals:
            done.add(v)
            adjacents = union_g.adjacent_to(v, lazy=False)
            u = sample(adjacents, k=1)[0]
            if u not in done:
                result.add_edge(v, u)
            terminals.discard(u)
            v = u

        return result
