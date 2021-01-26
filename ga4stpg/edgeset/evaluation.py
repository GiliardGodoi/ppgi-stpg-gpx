from ga4stpg.graph.reader import SteinerTreeProblem
from ga4stpg.graph.disjointsets import DisjointSets

class EvaluateEdgeSet:

    def __init__(self, stpg : SteinerTreeProblem, penality_function=None) :
        self.STPG = stpg

        if callable(penality_function):
            self.penality_function = penality_function
        else:
            self.penality_function = lambda k : (k - 1) * 1_00


    def __call__(self, chromosome, **kwargs):
        '''
        Parameters:
        chromosome : is a EdgeSet type or a Bag
        '''
        disjointset = DisjointSets()
        _cost = 0
        GRAPH = self.STPG.graph

        # assert isinstance(chromosome, EdgeSet)

        for v ,u in chromosome:
            if not GRAPH.has_edge(v, u):
                raise RuntimeError("STPG instance has not this edge")
            _cost += GRAPH.weight(v, u)
            if v not in disjointset:
                disjointset.make_set(v)
            if u not in disjointset:
                disjointset.make_set(u)
            disjointset.union(v, u)

        nro_components = len(disjointset.get_disjoint_sets())

        _cost += self.penality_function(nro_components)

        return _cost, nro_components


