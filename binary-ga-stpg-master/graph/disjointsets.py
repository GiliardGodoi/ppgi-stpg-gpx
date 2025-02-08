# -*- coding: utf-8 -*-
"""
An implementation of Disjoint Set.

@author: Giliard Almeida de Godoi
"""
from collections import defaultdict
from graph import Graph

class Subset():

    def __init__(self, vertice, rank=0):
        self.parent = vertice
        self.rank = rank

class DisjointSets():

    def __init__(self):
        self.subsets = defaultdict()

    def __contains__(self, item):
        return item in self.subsets

    def __len__(self):
        return len(self.subsets)

    def make_set(self, item, ignore_previous=False):
        if item in self.subsets and not ignore_previous:
            raise ValueError(f"Key <{item!r}> already exist")

        self.subsets[item] = Subset(item)

    def find(self, item):
        if item not in self.subsets:
            raise TypeError(f"There is no subset for {item}")

        if self.subsets[item].parent != item :
            self.subsets[item].parent = self.find(self.subsets[item].parent)

        return self.subsets[item].parent

    def union(self, v, u):
        self.__link__(self.find(v), self.find(u))

    def __link__(self, v, u):
        if self.subsets[u].rank > self.subsets[v].rank:
            self.subsets[v].parent = self.subsets[u].parent

        elif self.subsets[v].rank > self.subsets[u].rank:
            self.subsets[u].parent = self.subsets[v].parent

        else :
            self.subsets[v].parent = u
            self.subsets[u].rank += 1

    def get_disjoint_sets(self):

        disjointsets = defaultdict(set)

        for key in self.subsets.keys():
            parent = self.find(key)
            disjointsets[parent].add(key)

        return disjointsets
