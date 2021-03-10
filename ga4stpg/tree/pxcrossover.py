from collections import deque
from operator import attrgetter
from random import choice

from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets


class Component:

    def __init__(self, first, second, initialcost=0):
        self.edges = {first : None, second : first}
        self.portal = set()
        self.cost = initialcost

    def add(self, first, second):
        self.edges[second] = first

def compose(red : UGraph, blue : UGraph):
    '''
    Parameters:
    ----------
        red, blue : Graph

    Return:
    -------
        g_union, g_common, g_star : Graph
    '''

    g_union  = UGraph()
    g_common = UGraph()
    g_star   = UGraph()

    for v, u in red.gen_undirect_edges():
        g_union.add_edge(v, u)

        if not blue.has_edge(v,u):
            g_star.add_edge(v,u)

    for v, u in blue.gen_undirect_edges():
        g_union.add_edge(v, u)

        if red.has_edge(v,u):
            g_common.add_edge(v, u)
        else:
            g_star.add_edge(v,u)


    return g_union, g_common, g_star

class PXTree:

    def __init__(self, stpg):
        self.STPG = stpg
        self.terminals = list(stpg.terminals)
        self.f_weight = lambda x, y: self.STPG.graph.weight(x, y)

    def connected(self, g_union : UGraph, red : UGraph, blue : UGraph, start : 'node'):

        linkedlist = deque([start])
        visited = set()
        parents = DisjointSets()
        f_weight = self.f_weight

        for v in g_union.vertices:
            parents.make_set(v)

        def chase(main, node, component):

            if (node in red) and (node in blue):
                if node not in visited and node not in linkedlist:
                    linkedlist.appendleft(node)

                component.portal.add(node)
                return

            for w in main.adjacent_to(node):
                if w in component.edges:
                    continue
                component.add(node, w)
                component.cost += f_weight(node, w)
                chase(main, w, component)
            # end for loop
            visited.add(node)

        components_red  = list()
        components_blue = list()

        while linkedlist:
            u = linkedlist.pop()
            visited.add(u)
            for v in g_union.adjacent_to(u):
                if v in visited:
                    continue
                if red.has_edge(u,v) and blue.has_edge(u,v):
                    linkedlist.append(v)
                    parents.union(u, v)

                elif red.has_edge(u,v):
                    component = Component(u, v, initialcost=f_weight(u,v))
                    chase(red, v, component)
                    chase(red, u, component)
                    components_red.append(component)

                elif blue.has_edge(u,v):
                    component = Component(u, v, initialcost=f_weight(u,v))
                    chase(blue, v, component)
                    chase(blue, u, component)
                    components_blue.append(component)
            # end for loop
        # end while loop
        return components_red, components_blue, parents

    def __call__(self, red : UGraph, blue : UGraph):

        start = choice(self.terminals)

        g_union, g_common, g_star = compose(red, blue)
        first, second, previous = self.connected(g_union, red, blue, start)

        matches = dict()

        for component in first:
            ss = frozenset(previous.find(v) for v in component.portal)
            matches[ss] = [component]

        non_second = list()

        for component in second:
            ss = frozenset(previous.find(v) for v in component.portal)
            if ss in matches:
                matches[ss].append(component)
            else:
                non_second.append(component)


        get_cost = attrgetter('cost')

        success = 0
        fail = 0

        non_first = list()
        minimum_cost = list()

        for key, components in matches.items():
            if len(components) >= 2:
                minimum_cost.append(min(components, key=get_cost))
                success += 1
            else:
                non_first.append(components.pop())
                fail += 1

        total_first = 0
        for c in non_first:
            total_first += c.cost

        total_second = 0
        for c in non_second:
            total_second += c.cost

        if total_second < total_first:
            selected = non_second
        else:
            selected = non_first

        for component in minimum_cost:
            for v, u in component.edges.items():
                if u is None:
                    continue
                g_common.add_edge(v,u)

        for component in selected:
            for v, u in component.edges.items():
                if u is None:
                    continue
                g_common.add_edge(v,u)

        return g_common
