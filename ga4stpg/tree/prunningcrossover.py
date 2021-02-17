from collections import deque
from random import choice

from ga4stpg.graph import UGraph
from ga4stpg.graph.priorityqueue import PriorityQueue

class PrunningMSTCrossover:

    def __init__(self, stpg):
        self.STPG = stpg
        self.terminals = list(stpg.terminals)
        self.f_weight = lambda v, u : self.STPG.graph.weight(v,u)

    def __call__(self, red : UGraph, blue : UGraph):

        g_union = UGraph()
        for v, u in red.gen_undirect_edges():
            g_union.add_edge(v, u)
        for v, u in blue.gen_undirect_edges():
            g_union.add_edge(v, u)

        p_queue = PriorityQueue()
        vertices = list(g_union.vertices)
        v = choice(vertices)
        for u in g_union.adjacent_to(v):
            weight = self.f_weight(v, u)
            p_queue.push(weight, (v, u))

        g_child = UGraph()
        done = set()
        done.add(v)
        while len(p_queue):
            v, u = p_queue.pop()
            if u not in done:
                g_child.add_edge(v,u)
                done.add(u)

            for w in g_union.adjacent_to(u):
                if w not in done:
                    p_queue.push(self.f_weight(u, w), (u, w))

        terminals = self.STPG.terminals

        prunne_leaves = deque([v for v in g_child.vertices
                            if ((g_child.degree(v) == 1) and (v not in terminals))])

        while prunne_leaves:
            v = prunne_leaves.pop()
            prev = g_child.adjacent_to(v, lazy=False)
            g_child.remove_node(v)
            for w in prev:
                if g_child.degree(w) == 1 and w not in terminals:
                    prunne_leaves.appendleft(w)

        return g_child
