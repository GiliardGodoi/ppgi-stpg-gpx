# -*- coding: utf-8 -*-
from collections import defaultdict

class _VerticeView(object):

    def __init__(self, edges : dict):
        self.__vertices = edges.keys()

    def __len__(self):
        return len(self.__vertices)

    def __contains__(self, item):
        return item in self.__vertices

    def __iter__(self):
        return iter(self.__vertices)

    def __and__(self, other):
        return self.__vertices & other.__vertices

    def __or__(self, other):
        return self.__vertices | other.__vertices

    def __xor__(self, other):
        return self.__vertices ^ other.__vertices

class UndirectedGraph:
    '''Base class to represent an Undirected Graph

        Note:
        -----

        Robert Sedgewick; Kevin Wayne; Robert Dondero
        **Introduction to Programming in Python**
        <https://introcs.cs.princeton.edu/python/home/>
        <https://introcs.cs.princeton.edu/python/45graph/graph.py.html>
    '''
    def __init__(self, edges=None):

        if edges is None:
            self.__edges = defaultdict(set)

        elif isinstance(edges, defaultdict) and (edges.default_factory is set):
            self.__edges.update(edges)

        else :
            raise AttributeError(f"Edges is not the correct type. Type:{type(edges)}")


    def __getitem__(self, key):
        return self.__edges.get(key, set())

    def __contains__(self, item):
        return item in self.__edges

    @property
    def edges(self):
        return self.__edges

    @property
    def vertices(self):
        vv = _VerticeView(self.__edges)
        return vv

    def get(self, key, std = set()):
        return self.__edges.get(key, std)

    def size(self):
        return len(self.__edges)

    def add_edge(self, v, u):
        if v != u :
            self.__edges[v].add(u)
            self.__edges[u].add(v)

    def add_node(self, v : 'vertice'):
        _ = self.__edges[v]

    def remove_edge(self, v, u):
        if self.has_edge(v,u):
            self.__edges[v].remove(u)
            self.__edges[u].remove(v)

    def remove_node(self, w : 'vertice'):
        if self.has_node(w):
            adjacents = self.__edges.pop(w)
            for v in adjacents:
                self.__edges[v].remove(w)

    def adjacent_to(self, v : 'vertice', lazy = True):
        if lazy :
            return iter(self.get(v))
        else :
            return set(self.get(v))

    def has_node(self, v):
        ''' Verifica se um vértice existe no grafo'''
        return (v in self.__edges)

    def has_edge(self, v, w):
        ''' Verifica se uma aresta existe no grafo'''
        return (w in self.get(v)) and (v in self.get(w))

    def degree(self, v):
        '''Retorna o grau de conexões de um vértice'''
        return len(self.get(v))

    def weight(self, v, w):
        raise NotImplementedError()

    def W(self, v, w):
        '''
        A short call to weight method
        '''
        return self.weight(v,w)

    def gen_direct_edges(self):
        for v in self.__edges.keys():
            for u in self.adjacent_to(v):
                yield (v,u)

    def gen_undirect_edges(self):
        visited = set()
        for v in self.__edges.keys():
            for u in self.adjacent_to(v):
                if not u in visited :
                    yield (v,u)
            visited.add(v)

class UndirectedWeightedGraph:
    '''
    '''
    def __init__(self, edges=None):

        if edges is None:
            self.__edges = defaultdict(dict)

        elif isinstance(edges, defaultdict) and (edges.default_factory is dict):
            self.__edges = edges

        else :
            raise AttributeError(f"Edges is not the correct type. Type:{type(edges)}")

    def __getitem__(self,key):
        return self.__edges.get(key, dict())

    def __contains__(self, item):
        return item in self.__edges

    @property
    def edges(self):
        ''' Retorna a estrutura de dados utilizada para representar as arestas, neste caso: defaultdict(dict)'''
        return self.__edges

    @property
    def vertices(self):
        ''' Retorna um iterator para iterar sobre o cojunto de vértices '''
        vv = _VerticeView(self.__edges)
        return vv

    def get(self, key, std = dict()):
        return self.__edges.get(key, std)

    def size(self):
        ''' Retorna o número de vértices no grafo '''
        return len(self.__edges)

    def add_edge(self, v, u, weight = None):
        '''Insere um arestas no grafo.

        @params <vértice v, vértice w, peso entre (v,w)>

        Se os vértices não existem previamente no grafo, então eles são inseridos.
        Não permite a inserção de loços, isto é, quando v == w.
        Se o parâmetro peso não é definido, é tomado como sendo de valor 1 (um)
        '''
        if weight is None:
            raise AttributeError("Weight must be given")

        if v != u :
            self.__edges[v][u] = weight
            self.__edges[u][v] = weight

    def add_node(self, v : 'vertice'):
        ''' @param <vértice>
        Insere um novo vértice ao conjunto de vértices. Não permite a inserção de um vértice pré-existente
        '''
        _ = self.__edges[v]

    def remove_edge(self, v, u):
        if self.has_edge(v,u):
            self.__edges[v].pop(u)
            self.__edges[u].pop(v)

    def remove_node(self, w : 'vertice'):
        if self.has_node(w):
            adjacents = self.__edges.pop(w)
            for v in adjacents.keys():
                self.__edges[v].pop(w)

    def adjacent_to(self, v : 'vertice', lazy = True):
        if lazy:
            return iter(self.__edges.get(v, dict()).keys())
        else :
            return set(self.__edges.get(v, dict()).keys())

    def has_node(self, v):
        ''' Verifica se um vértice existe no grafo'''
        return (v in self.__edges)

    def has_edge(self, v, w):
        ''' Verifica se uma aresta existe no grafo'''
        return (v in self.get(w)) and (w in self.get(v))

    def degree(self, v):
        ''' Retorna o grau de conexões de um vértice '''
        return len(self.get(v).keys())

    def weight(self, v, w):
        ''' Retorna o peso de uma aresta. Se a aresta não existe é retornado o valor 0 '''
        if self.has_edge(v,w):
            return self.__edges[v][w]
        elif (v == w) and self.has_node(v):
            return 0
        else:
            return float("inf")

    def W(self,v,w):
        '''
        A short call to weight method
        '''
        return self.weight(v,w)

    def gen_direct_edges(self):
        for v in self.__edges.keys():
            for u in self.__edges[v].keys():
                yield (v,u)

    def gen_undirect_edges(self):
        visited = set()
        for v in self.__edges.keys():
            for u in self.__edges[v].keys():
                if not u in visited :
                    yield (v,u)
            visited.add(v)


class SpecialGraph:

    def __init__(self, edges):
        self.__edges = defaultdict(dict)

    def __getitem__(self,key):
        return self.__edges.get(key, dict())

    def __contains__(self, item):
        return item in self.__edges

    @property
    def edges(self):
        ''' Retorna a estrutura de dados utilizada para representar as arestas, neste caso: defaultdict(dict)'''
        return self.__edges

    @property
    def vertices(self):
        ''' Retorna um iterator para iterar sobre o cojunto de vértices '''
        vv = _VerticeView(self.__edges)
        return vv

    def get(self, key, std = dict()):
        return self.__edges.get(key, std)

    def size(self):
        ''' Retorna o número de vértices no grafo '''
        return len(self.__edges)

    def add_edge(self, v, u, keep_previous=True, **kwargs):
        if not keep_previous:
            self.__edges[v][u].clear()
            self.__edges[u][v].clear()
        # talvez, exista uma situação que seja permitido laços nesses grafos.
        # por isso retirei a condição v != v
        # quais são essas condições
        self.__edges[v][u].update(kwargs)
        self.__edges[u][v].update(kwargs)

    def add_node(self, v : 'vertice'):
        _ = self.__edges[v]

    def remove_edge(self, v, u):
        if self.has_edge(v,u):
            self.__edges[v].pop(u)
            self.__edges[u].pop(v)

    def remove_node(self, w : 'vertice'):
        if self.has_node(w):
            adjacents = self.__edges.pop(w)
            for v in adjacents.keys():
                self.__edges[v].pop(w)

    def adjacent_to(self, v : 'vertice', lazy = True):
        if lazy:
            return iter(self.__edges.get(v, dict()).keys())
        else :
            return set(self.__edges.get(v, dict()).keys())

    def has_node(self, v):
        ''' Verifica se um vértice existe no grafo'''
        return (v in self.__edges)

    def has_edge(self, v, w):
        ''' Verifica se uma aresta existe no grafo'''
        return (v in self.get(w)) and (w in self.get(v))

    def degree(self, v):
        ''' Retorna o grau de conexões de um vértice '''
        return len(self.get(v).keys())

    def weight(self, v, w):
        raise NotImplementedError()

    def W(self,v,w):
        return self.weight(v,w)
