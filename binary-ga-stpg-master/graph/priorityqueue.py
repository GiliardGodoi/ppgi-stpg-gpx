# -*- coding: utf-8 -*-
from heapq import heapify, heappop, heappush
import itertools

class PriorityQueue():
    '''
        Priority Queue implementation

        There is a tradeoff between speed and memory.

        In this implementations we've choosed the solution presented in official documentation for heapq module.
        More details in <>

    '''
    def __init__(self):
        self.__queue = list()
        heapify(self.__queue)
        self.REMOVED = '<removed>'
        self.__entry_finder = {}
        self.__counter = itertools.count()

    def push(self, priority, label):
        '''
        Insere um elemento na fila de prioridade.
        @paramns: priority <int> e label <vértice> do grafo
        '''

        if label in self.__entry_finder :
            self.__mark_remove(label)
        count = next(self.__counter)
        entry = [priority, count, label]
        self.__entry_finder[label] = entry
        heappush(self.__queue,entry)

    def pop(self):
        '''
        Retorna o menor <label> elemento da fila de prioridade.
        '''
        while self.__queue :
            # priority, count, label = heappop(self.__queue)
            _, _, label = heappop(self.__queue)
            if label is not self.REMOVED:
                del self.__entry_finder[label]
                return label

    def __mark_remove(self, label):
        entry = self.__entry_finder.pop(label)
        entry[-1] = self.REMOVED ## marca a última posição como REMOVED

    def __contains__(self, label):
        return label in self.__entry_finder

    def __len__(self):
        return len(self.__entry_finder)