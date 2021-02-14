from operator import attrgetter
from random import choice

from ga4stpg.graph import Graph
from ga4stpg.graph.util import compose
from ga4stpg.graph.steiner import prunning_mst

class PrunningCrossover:

    def __init__(self, stpg):
        self.STPG = stpg
        self.terminals = list(stpg.terminals)

    def __call__(self, red : Graph, blue : Graph):

        g_union, _a, _b = compose(red, blue)

        z = choice(self.terminals)

        g_child, _ = prunning_mst(g_union, z, self.STPG.terminals)

        return g_child
