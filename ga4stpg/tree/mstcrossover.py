from random import sample

from ga4stpg.graph import UGraph

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
        candidates_edges = set()

        vi = terminals.pop()
        done.add(vi)
        for u in union_g.adjacent_to(vi):
            candidates_edges.add((vi, u))

        while candidates_edges and terminals:
            edge = sample(candidates_edges, k=1)[0]
            v, w = edge
            if w not in done:
                done.add(w)
                result.add_edge(v, w)
                terminals.discard(w)
                for u in union_g.adjacent_to(w):
                    if u not in done:
                        candidates_edges.add((w, u))
            candidates_edges.discard((v, w))

        return result


class CrossoverKruskalRST:
    def __init__(self, stpg):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red, blue):
        assert isinstance(red, UGraph), f'red parent must be UGraph. Given {type(red)}'
        assert isinstance(blue, UGraph), f'blue parent must be UGraph. Given {type(blue)}'

        terminals = self.terminals.copy()

        union_g = UGraph()
        for v, u in red.gen_undirect_edges():
            union_g.add_edge(v ,u)
        for v, u in blue.gen_undirect_edges():
            union_g.add_edge(v, u)

        all_edges = set()
        for v, u in union_g.gen_undirect_edges():
            all_edges.add((min(v, u), max(v, u)))

        result = UGraph()
        while all_edges and terminals :
            edge = sample(all_edges, k=1)[0]
            v, u = edge[0], edge[1]
            if v in result and u in result:
                continue # do not add the edge
            else:
                result.add_edge(v, u)
                terminals.discard(v)
                terminals.discard(u)
            all_edges.discard(edge)

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
            w = sample(adjacents, k=1)[0]
            if u not in done:
                result.add_edge(v, u)
            terminals.discard(u)
            v = u

        return result
