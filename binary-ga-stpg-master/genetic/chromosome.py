# -*- coding: utf-8 -*-
'''
    Fornece algumas representações básicas para os cromossomos
'''

import reprlib

class BinaryChromosome(object):
    '''Class provides a basic chromosome representation'''

    def __init__(self, genes):
        self.__genes = genes
        self.__cost = 0
        self.__fitness = 0
        self.normalized = False

    @property
    def genes(self):
        return self.__genes

    @genes.setter
    def genes(self, value):
        self.__genes = value

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, value):
        self.__cost = value
        self.__fitness = value
        self.normalized = False

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        self.__fitness = value
        self.normalized = True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}: {reprlib.repr(self.genes)}"

class TreeBasedChromosome(BinaryChromosome):

    def __init__(self, genes):
        super().__init__(genes)

    @property
    def graph(self):
        return self.genes

    @graph.setter
    def graph(self, newgraph):
        self.genes = newgraph

    def __repr__(self):
        return f"{self.__class__.__name__}"
