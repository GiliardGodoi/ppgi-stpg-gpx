from random import randint, sample

from ga4stpg.edgeset import EdgeSet
from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.priorityqueue import PriorityQueue

class MutateRemovingCycle:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, chromosome : EdgeSet):
        assert isinstance(chromosome, EdgeSet), f'Chromosome must be EdgeSet type: Given was <{type(chromosome)}>'
        vertices = set(list(chromosome.vertices))
        assert len(vertices) == len(chromosome) + 1

        graph = self.stpg.graph
        vi = sample(vertices, k=1)[0]

        tree = UGraph()
        for edge in chromosome:
            u, v = edge[0], edge[1]
            tree.add_edge(u, v)

        candidates = set()
        for w in graph.adjacent_to(vi):
            if w in vertices:
                candidates(w)


class MutateReconectingComponents:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, chromosome : EdgeSet):
        assert isinstance(chromosome, EdgeSet), f'Chromosome must be EdgeSet type: Given was <{type(chromosome)}>'
        graph = self.stpg.graph

        disjoints = DisjointSets()
        candidates = PriorityQueue()
        result = EdgeSet()

        for v in chromosome.vertices:
            disjoints.make_set(v)

        index = randint(0, len(chromosome))
        for i, edge in enumerate(chromosome):
            u, v = edge
            if i == index:
                candidates.push(graph.weight(u,v), (u,v))
            else:
                disjoints.union(u, v)
                result.add(u, v)

        components = disjoints.get_disjoint_sets()

        assert len(components) == 2, ""
        lesser_idx  = min(components, key=lambda item: components[item])
        greater_idx = max(components, key=lambda item: components[item])

        for v in components[lesser_idx]:
            for w in graph.adjacent_to(v):
                if w in components[greater_idx]:
                    candidates.push(graph.weight(w,v), (w,v))

        w, v = candidates.pop()
        result.add(w, v)

        return result















