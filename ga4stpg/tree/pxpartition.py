import random
from ga4stpg.graph import UGraph
from ga4stpg.graph.disjointsets import DisjointSets

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

def _dict_matches_from(partitions, disjoint):
    matches = dict()
    for partition in partitions:
        key = frozenset(disjoint.find(v) for v in partition.portal)
        matches[key] = partition
    return matches

def select_partition_and_union(selected, red_dict, blue_dict, disjoint, matches):
    for key in matches:
        red_p  = red_dict.pop(key)
        blue_p = blue_dict.pop(key)

        choosed = None
        if red_p.cost == blue_p.cost:
            choosed = random.choice([red_p, blue_p])
            # print(red_p, blue_p)
            # print("Random ", choosed)
        elif red_p.cost < blue_p.cost:
            choosed = red_p
            # print("Red: ", choosed)
        elif blue_p.cost < red_p.cost:
            choosed = blue_p
            # print("Blue: ", choosed)

        selected.append(choosed)

        g_portals = iter(choosed.portal)
        last_p = next(g_portals)
        for p in g_portals:
            disjoint.union(last_p, p)
            last_p = p

    return selected, red_dict, blue_dict, disjoint

class Partition:
    def __init__(self):
        self.edges = set()
        self.cost = 0
        self.portal = set()

    def __len__(self):
        return len(self.edges)

    def __str__(self):
        return f'Partition <{self.portal}>'

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.edges)

    @property
    def bounds(self):
        return frozenset(self.portal)

    def add(self, v, u):
        self.edges.add((v, u))

class PartitionCrossoverSteinerTree:

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
        stack_outter = list(specific_nodes)
        result = list()

        def search(start, neighbor):
            partition = Partition()
            partition.portal.add(start)
            partition.add(start, neighbor)
            partition.cost += f_weight(start, neighbor)

            stack_inner = [neighbor]

            while stack_inner:
                u = stack_inner.pop()
                visited.add(u)
                if u not in specific_nodes:
                    counter = 0
                    for w in subgraph.adjacent_to(u):
                        if w not in visited:
                            stack_inner.append(w)
                            partition.add(u, w)
                            partition.cost += f_weight(u, w)
                            counter += 1
                    if counter == 0:
                        partition.portal.add(u)
                else:
                    stack_outter.append(u)
                    partition.portal.add(u)
            # end while
            return partition
            # end search

        while stack_outter:
            s = stack_outter.pop()

            visited.add(s)
            for v in subgraph.adjacent_to(s):
                if v not in visited:
                    seg = search(s, v)
                    result.append(seg)

        return result

    def __call__(self, red : UGraph, blue : UGraph):

        red_only  = UGraph()
        blue_only = UGraph()

        common_vertices = set(red.vertices) & set(blue.vertices)
        common_edges = set()

        for v, u in red.gen_undirect_edges():
            if blue.has_edge(v, u):
                common_edges.add((v, u))
            else:
                red_only.add_edge(v, u)

        for v, u in blue.gen_undirect_edges():
            if not red.has_edge(v, u):
                blue_only.add_edge(v, u)


        for v in red_only.vertices:
            if (red.degree(v) == 1) and (v not in self.STPG.terminals):
                common_vertices.add(v)
        for v in blue_only.vertices:
            if blue.degree(v) == 1 and (v not in self.STPG.terminals):
                common_vertices.add(v)

        disjoint = DisjointSets()
        for v in common_vertices:
            disjoint.make_set(v)
        for v, u in common_edges:
            disjoint.union(v, u)

        common_nodes_red = set(red_only.vertices) & common_vertices
        common_nodes_blue = set(blue_only.vertices) & common_vertices

        red_partitions  = self.find_partitions(red_only, common_nodes_red)
        blue_partitions = self.find_partitions(blue_only, common_nodes_blue)

        red_dict  = _dict_matches_from(red_partitions, disjoint)
        blue_dict = _dict_matches_from(blue_partitions, disjoint)
        matches   = red_dict.keys() & blue_dict.keys()

        selected = list()

        while matches:
            selected, red_dict, blue_dict, disjoint = select_partition_and_union(selected, red_dict, blue_dict, disjoint, matches)
            red_dict  = _dict_matches_from(red_dict.values(), disjoint)
            blue_dict = _dict_matches_from(blue_dict.values(), disjoint)
            matches = red_dict.keys() & blue_dict.keys()

        red_child  = UGraph()
        blue_child = UGraph()

        for v, u in common_edges:
            red_child.add_edge(v, u)
            blue_child.add_edge(v, u)

        for partition in selected:
            for v, u in partition:
                red_child.add_edge(v, u)
                blue_child.add_edge(v, u)

        for partition in red_dict.values():
            for v, u in partition:
                red_child.add_edge(v, u)

        for partition in blue_dict.values():
            for v, u in partition:
                blue_child.add_edge(v, u)

        return red_child, blue_child

if __name__ == "__main__":
    pass