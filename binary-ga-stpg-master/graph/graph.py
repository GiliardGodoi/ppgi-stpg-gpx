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

class Graph(object):
    '''
        Classe para representar um grafo.

        Baseado nos trabalhos de:

        Robert Sedgewick; Kevin Wayne; Robert Dondero
        **Introduction to Programming in Python**
        <https://introcs.cs.princeton.edu/python/home/>
        <https://introcs.cs.princeton.edu/python/45graph/graph.py.html>
    '''
    def __init__(self, vertices=None, edges=None):

        if isinstance(edges,defaultdict):
            self.__edges = edges
        elif edges is None:
            self.__edges = defaultdict(dict)
        else :
            raise AttributeError("Edges isnt a dict")

        if isinstance(vertices,int):
            nodes = range(1,vertices+1)
        elif isinstance(vertices,(list,set,tuple)):
            nodes = vertices
        else:
            nodes = list()

        for v in nodes: # ainda está estranha essa forma de inicialização do grafo
            if not v in self.__edges:
                self.__edges[v] = dict()

    def __getitem__(self,key):
        return self.__edges[key]

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

    def get(self,key,std = None):
        return self.__edges.get(key,std)

    def size(self):
        ''' Retorna o número de vértices no grafo '''
        return len(self.__edges)

    def add_edge(self,v,u, weight = 1):
        '''Insere um arestas no grafo.

        @params <vértice v, vértice w, peso entre (v,w)>

        Se os vértices não existem previamente no grafo, então eles são inseridos.
        Não permite a inserção de loços, isto é, quando v == w.
        Se o parâmetro peso não é definido, é tomado como sendo de valor 1 (um)
        '''
        if v == u :
            return
        
        self.__edges[v][u] = weight
        self.__edges[u][v] = weight

    def add_node(self,v):
        ''' @param <vértice>
        Insere um novo vértice ao conjunto de vértices. Não permite a inserção de um vértice pré-existente
        '''
        if not self.has_node(v):
            self.__edges[v] = dict()

    def remove_edge(self, v, u):
        if self.has_edge(v,u):
            self.__edges[v].pop(u)
            self.__edges[u].pop(v)

    def remove_node(self,w):
        if self.has_node(w):
            adjacents = self.__edges.pop(w)
            for v in adjacents.keys():
                self.__edges[v].pop(w)

    def adjacent_to(self,v):
        ''' @param <vértice>
        Retorna um objeto <iterator> com os vértices adjacentes ao vértice passado como parâmetro.
        Se não existe arestas com o vértice informado, um <KeyError> é lançado. Não faz essa verificação.
        '''
        return self.__edges[v].keys()

    def has_node(self, v):
        ''' Verifica se um vértice existe no grafo'''
        return (v in self.__edges)

    def has_edge(self, v, w):
        ''' Verifica se uma aresta existe no grafo '''
        if self.has_node(v) :
            return (w in self.__edges[v])
        return False

    def degree(self, v):
        ''' Retorna o grau de conexões de um vértice '''
        adj = self.__edges[v]
        return len(adj.keys())

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