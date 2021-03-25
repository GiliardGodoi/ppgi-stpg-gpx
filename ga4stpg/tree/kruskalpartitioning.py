from collections import deque
from random import randrange

from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.priorityqueue import PriorityQueue

def check_portals(portals, disjoint):
    '''Verifica se os vértices portais de um segmento
    se conectam à mesma partição de vértices comuns.

    Faz essa verificação em tempo O(n)
    '''
    f_check = set()

    for p in portals:
        if p not in disjoint:
            return False
        k = disjoint.find(p)
        if k in f_check:
            return False
        f_check.add(k)

    return True

class Partition:
    def __init__(self):
        self.edges = set()
        self.cost = 0
        self.portal = set()

    def __len__(self):
        return len(self.edges)

    def __str__(self):
        return f'Segment <{len(self.edges)}>'

    def __iter__(self):
        return iter(self.edges)

    @property
    def bounds(self):
        return frozenset(self.portal)

    def add(self, v, u):
        self.edges.add((v, u))

class KruskalBasedPartitioning:

    def __init__(self, stpg) -> None:
        self.STPG = stpg
        self.GRAPH = stpg.graph

    def f_weight(self, v, u):
        if self.GRAPH is None:
            raise AttributeError("GRAPH shouldn't be None")
        return self.GRAPH.weight(v, u)

    def find_partitions(self, subgraph, specific_nodes):
        visited = set()
        f_weight = self.f_weight
        # start = None
        # index = randrange(0, len(common_nodes))
        # for i, nro in enumerate(common_nodes):
        #     if i == index:
        #         start = nro
        #         break
        # assert start is not None
        # stack_outter = [start]
        stack_outter = list(specific_nodes)
        result = list()

        def search(start, neighbor):
            segment = Partition()
            segment.portal.add(start)
            segment.add(start, neighbor)
            segment.cost += f_weight(start, neighbor)

            stack_inner = [neighbor]

            while stack_inner:
                u = stack_inner.pop()
                visited.add(u)
                if u not in specific_nodes:
                    counter = 0
                    for w in subgraph.adjacent_to(u):
                        if w not in visited:
                            stack_inner.append(w)
                            segment.add(u, w)
                            segment.cost += f_weight(u, w)
                            counter += 1
                    if counter == 0:
                        segment.portal.add(u)
                else:
                    stack_outter.append(u)
                    segment.portal.add(u)
            # end while
            return segment
            # end search

        while stack_outter:
            s = stack_outter.pop()

            visited.add(s)
            for v in subgraph.adjacent_to(s):
                if v not in visited:
                    seg = search(s, v)
                    result.append(seg)

        return result


    def __call__(self, red: UGraph, blue: UGraph):
        child     = UGraph()
        red_only  = UGraph()
        blue_only = UGraph()

        for v, u in red.gen_undirect_edges():
            if blue.has_edge(v, u):
                child.add_edge(v, u)
            else:
                red_only.add_edge(v, u)

        for v, u in blue.gen_undirect_edges():
            if not red.has_edge(v, u):
                blue_only.add_edge(v, u)

        common_nodes_red = set(red_only.vertices) & set(blue.vertices)
        common_nodes_blue = set(blue_only.vertices) & set(red.vertices)

        red_partitions  = self.find_partitions(red_only, common_nodes_red)
        blue_partitions = self.find_partitions(blue_only, common_nodes_blue)

        queue = PriorityQueue()

        for partition in red_partitions:
            queue.push(partition.cost, partition)

        for partition in blue_partitions:
            queue.push(partition.cost, partition)

        common_nodes = set(red.vertices) | set(blue.vertices)
        dset = DisjointSets()

        for v in common_nodes:
            dset.make_set(v)

        for v, u in child.gen_undirect_edges():
            dset.union(v, u)

        while queue:
            partition = queue.pop()

            if check_portals(partition.portal, dset):

                # add edges
                for v, u in partition:
                    child.add_edge(v, u)

                # update dset
                portals = iter(partition.portal)

                p_last = next(portals)
                for p in portals:
                    dset.union(p_last, p)
                    p_last = p

        return child


