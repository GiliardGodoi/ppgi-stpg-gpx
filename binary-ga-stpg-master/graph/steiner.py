# -*- coding: utf-8 -*-
from collections import defaultdict

from graph import Graph
from graph.priorityqueue import PriorityQueue
from graph.algorithms import shortest_path_dijkstra as dijkstra
from graph.algorithms import prim


def shortest_path(graph, start, terminals):

    dist, prev = dijkstra(graph,start)

    distancias = defaultdict(dict)
    distancias[start] = dist

    previos = defaultdict(dict)
    previos[start] = prev

    pqueue = PriorityQueue()

    for t in terminals:
        pqueue.push(distancias[start][t], (start,t))

    subtree = Graph()

    while pqueue:
        source, target = pqueue.pop()
        t = target

        if target not in distancias:
                dist, prev = dijkstra(graph,target)
                distancias[target] = dist
                previos[target] = prev
                for tmp in terminals:
                    pqueue.push(distancias[target][tmp], (target,tmp))

        if target not in subtree.vertices :
            while distancias[source][t]:
                u = previos[source][t]
                w = graph[u][t]
                subtree.add_edge(t,u,weight=w)
                t = u

                if u not in distancias:
                    dist, prev = dijkstra(graph,u)
                    distancias[u] = dist
                    previos[u] = prev
                    for tmp in terminals:
                        pqueue.push(distancias[u][tmp], (u,tmp))

    gg, custo = prunning_mst(subtree, start, terminals)

    return gg, custo


def shortest_path_with_origin(graph, start, terminals):
    '''
    Adaptação para o algortimo Shortest Path with Origin Heuristic

    A Árvore solução Tspoh é contruida iterativamente: um vertice terminal é incluido por vez.

    Determina-se a árvore de caminhos mínimos de um ponto inicial <start> até os demais vértices;
    A partir de cada vértice terminal incluí-se o menor caminho até <start>
    Um vértice terminal ou está nas folhas da árvore formada, ou está no caminho de outro nó terminal.
    '''

    dist, prev = dijkstra(graph,start)
    custo = 0

    stree = Graph()

    for u in terminals:
        while dist[u] :
            v = prev[u]
            if not stree.has_edge(u,v):
                w = graph[u][v]
                stree.add_edge(u,v,weight=w)
                custo += w
            else:
                break
            u = v

    return stree, custo


def shortest_path_origin_prim(graph, start, terminals):
    '''
    Determinar a árvore de caminhos mínimos <T> dos vértices terminais até o nó <start>
    Define um subgrafo formado pelos vértices presentes em T
    com as correspondentes arestas do grafo G <graph>.
    Calcula a MST do subgrafo considerado e realiza a poda da MST.
    '''

    dist, prev = dijkstra(graph, start)

    selectedNodes = set([start])

    for t in terminals:
        selectedNodes.add(t)
        u = t
        while dist[u]:
            v = prev[u]
            selectedNodes.add(v)
            u = v

    subgraph = Graph()

    for v in selectedNodes:
        for u in graph.adjacent_to(v):
            if (u in selectedNodes):
                w = graph.edges[v][u]
                subgraph.add_edge(v, u, weight=w)

    subtree, cost = prunning_mst(subgraph, start, terminals)

    return subtree, cost


def prunning_mst(graph, start, terminals):
    '''
    Determina a MST do grafo por meio do algoritmo de Prim.
    Realiza a poda considerando os nós terminais como os nós folhas até a raiz <start>
    Considera-se um algoritmo determinístico dado os mesmos parâmetros.

    Resulta sempre na mesma árvore para qualquer vértice <start> considerado.
    '''
    mst, _ = prim(graph,start)

    mst[start] = False

    mst_trim = Graph()

    total_weight = 0

    for t in terminals:
        node = t
        while mst[node]:
            prev = mst[node]
            if mst_trim.has_edge(prev,node):
                break # já foi inserido esse ramo
            weight = graph[prev][node]
            total_weight += weight
            mst_trim.add_edge(prev,node,weight=weight)
            node = prev

    return mst_trim, total_weight
