# -*- coding: utf-8 -*-
from collections import defaultdict, deque

from graph import Graph
from graph.disjointsets import DisjointSets
from graph.priorityqueue import PriorityQueue

'''
    This module contains the most commons algorithms for work with graphs.
    The graph representation use the class GraphDictionary class define in the 'graph' module
'''

__all__ = [
        "shortest_path_dijkstra",
        "prim",
        "bfs",
        "dfs",
        "find_connected_components"
        ]

def shortest_path_dijkstra(graph, source):
    ''' Dijkstra Algorithm: It computes the lowest distance between a source vertice and
    all the other vertices.

    Parameters
        graph : GraphDictionary
        source : <a vertice from the graph>

    Returns
        dist : dict
            <vertice : distance from source> - distance dictionary from the source to vertice
        prev : dict
            < vertice : previous > - a dictionary representing a previous node

    Notes:
        An early implementation has O(n^2) complexity.
        Many improvements has been proposed across the years.
        They are more complicated, though.

        Based in Chirantan Sharma's code
        <https://github.com/cs-oak/Fibonacci-Heaps/blob/master/dijkstra.py>
        Its use an other Priority Queue implemantation which is not used by Sharma.
    '''
    dist = defaultdict(lambda : float("inf"))
    dist[source] = 0

    prev = {source : None}
    done = {}

    pqueue = PriorityQueue()
    pqueue.push(0, (0, source))

    while len(pqueue):
        dist_u, u = pqueue.pop()

        if u in done :
            continue

        done[u] = True

        for v in graph.edges[u]:
            new_dist_to_v = dist_u + graph.edges[u][v]
            # esse if só da False quando: o vertice ja estiver em dist (visitado) e a distancia ja for a menor
            if (not v in dist) or (dist[v] > new_dist_to_v):
                dist[v] = new_dist_to_v
                prev[v] = u
                pqueue.push(new_dist_to_v,(new_dist_to_v,v))

    return dist, prev


def prim(graph : Graph, start):
    ''' Prim's Algorithm: Compute the Minimum Spanning Tree for the graph.

    Parameters:
        graph : GraphDictionary
        start : <a graph's node>

    Returns:
        dict :

        int :

    TO DO:
        Verificar se para diferentes pontos de inicialização retorna a mesma árvore
        se sim, parece que está funcionando ok.
    '''
    if start not in graph.vertices:
        raise ValueError("start is not in graph vertices")

    mtree = dict()
    total_weight = 0
    queue = PriorityQueue()

    queue.push(0,(start, start))

    while queue :
        node_start, node_end = queue.pop()
        if node_end not in mtree:
            mtree[node_end] = node_start
            total_weight += graph.weight(node_start, node_end)

            for next_node, weight in graph.edges[node_end].items():
                queue.push(weight,(node_end, next_node))

    return mtree, total_weight


def kruskal(graph : Graph):
    '''Kruskal Algorithm to determine a Minimum Spanning Tree froma a Graph

    Parameter
        graph : Graph

    Return
        Graph
    '''

    DS = DisjointSets()
    MST = Graph()

    for v in graph.vertices:
        DS.make_set(v)

    edges = [ {"edge" : (v, u), "weight" : graph.weight(v, u)}  \
                for v, u in graph.gen_undirect_edges()]

    edges = sorted(edges, key=lambda item: item["weight"])

    for item in edges:
        v, u = item["edge"]
        if DS.find(v) != DS.find(u):
            MST.add_edge(v, u, weight=item["weight"])
            DS.union(v,u)

    return MST


def bfs(graph, start=None):
    '''Breadth First Search

    Parameters
        graph : GraphDictonary
        start : a graph's vertice

    Returns
        set
            a set of vertices reached

    Raises
        TypeError
        ValueError
    '''
    if not start:
        raise TypeError("Start is not defined")
    elif not (start in graph.vertices):
        raise ValueError("start node is not in graph")


    visited_nodes = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        visited_nodes.add(node)
        for v in graph.adjacent_to(node):
            if not v in visited_nodes:
                queue.append(v)

    return visited_nodes


def dfs(graph, start = None):
    '''Deep First Search

    Parameters
        graph : GraphDictionary
        start : graph's vertice

    Returns
        set
            vertices visited

    Raises:
        TypeError
        ValueError
    '''

    if not start :
        raise TypeError('Start is not defined')
    elif not (start in graph):
        raise ValueError("Start node is not in graph")

    vertices_done = set()
    stack = deque([start])

    while stack:
        node = stack.pop()
        vertices_done.add(node)
        for v in graph.adjacent_to(node):
            if not v in vertices_done:
                stack.append(v)

    return vertices_done


def find_connected_components(graph):
    '''
    It finds the connected components given a graph.

    Parameter
        graph : Graph

    Returns
        list of set:
            Return a list of connected components.
            Which components is represented by a set.

    Notes:
        This implementation is based in recursion and breadth search.
        By definition the sets must have empty intersection.
    '''
    all_nodes = set(graph.edges.keys())

    if not all_nodes:
        return {}

    def find_by_recursion(graph, start = None, nodes = None):
        if not start:
            return []
        if not nodes :
            return []

        visited = bfs(graph,start=start)

        not_visited = nodes - visited

        components = [visited]

        if len(not_visited):
            n_start = not_visited.pop()
            components += find_by_recursion(graph,start=n_start,nodes=not_visited)

        return components

    start = all_nodes.pop()

    return find_by_recursion(graph,start=start,nodes=all_nodes)
