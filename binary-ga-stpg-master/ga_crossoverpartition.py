# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 21:59:09 2020

@author: Giliard Almeida de Godoi
"""
import csv
import json
import os
import random
from collections import defaultdict, deque
from operator import attrgetter

from graph import Graph, ReaderORLibrary
from graph.steiner import shortest_path, shortest_path_with_origin
from graph.util import gg_rooted_tree, gg_total_weight

from genetic.base import Operator
from genetic.chromosome import BinaryChromosome


class Chromossome(BinaryChromosome):

    def __init__(self, subtree : Graph, start_node, cost=0):
        super().__init__(None)
        self.subtree = subtree
        self.start_node = start_node


class PartitionCrossover(Operator):

    def __init__(self, graph_data : Graph):
        self.graph = graph_data
        self.counter = defaultdict()

    def operation(self, parent_1 : Chromossome, parent_2 : Chromossome):

        subtree_1 = parent_1.subtree
        subtree_2 = parent_2.subtree

        # Primeiro uma das soluções será transformada na sua forma enraizada
        s1 = parent_1.start_node

        rooted_tree_1 = gg_rooted_tree(subtree_1, s1)

        disjoint_edges_2, GGsub2 = self.disjoints_edges_and_subgraph(subtree_1, subtree_2)


        # DETERMINAR AS PARTIÇÕES DE UM DOS PAIS E OS VÉRTICES COMUNICANTES

        subsets = list()

        while disjoint_edges_2 :
            v, u = disjoint_edges_2.pop()

            # poderia ter sido
            ## if subtree_1.has_node(v) and subtree_1.has_node(u):
            if (v in rooted_tree_1) and (u in rooted_tree_1):
                tmp = {
                    'edges' : {(v , u)},
                    'common' : [v, u],
                    'cost' : self.graph.weight(v, u)
                }
                subsets.append(tmp)

            elif (v in rooted_tree_1) and (not u in rooted_tree_1):
                tmp = self.DFS_with_stop(rooted_tree_1, disjoint_edges_2, GGsub2, u)
                subsets.append(tmp)

            elif not (v in rooted_tree_1) and (u in rooted_tree_1):
                # print('v ', v)
                tmp = self.DFS_with_stop(rooted_tree_1, disjoint_edges_2, GGsub2, v)
                subsets.append(tmp)

            else :
                tmp = self.DFS_with_stop(rooted_tree_1, disjoint_edges_2, GGsub2, v)
                subsets.append(tmp)


        partitions = dict()
        counter = 0

        for ss in subsets :
            # assert len(ss['common']) >= 2, 'Vertices em comun deve ser maior ou igual a 2'
            v = ss['common'][0]
            subsets_2 = {'edges' : set(),'common' : [v], 'cost' : 0}
            for u in ss['common'][1:] :
                edges, cost = self.find_uncommon_edges_from_path(rooted_tree_1, v, u, subtree_2)
                subsets_2['edges'].update(edges)
                subsets_2['common'].append(u)
                subsets_2['cost'] += cost

            partitions[counter] = {'sub1' : ss, 'sub2' : subsets_2 }
            counter += 1

        # REALIZAR A COMPARAÇÃO E MONTAR A SOLUÇÃO FINAL
        GG_child = Graph()
        cost_child = 0

        for v, u in subtree_1.gen_undirect_edges():
            if subtree_2.has_edge(v, u):
                ww = self.graph.weight(v, u)
                cost_child += ww
                GG_child.add_edge(v, u, weight= ww)

        for _, pp in partitions.items():
            edges = {}

            if pp['sub1']['cost'] <= pp['sub2']['cost'] :
                edges = pp['sub1']['edges']
                # print('sub1 escolhido')

            elif pp['sub2']['cost'] < pp['sub1']['cost'] :
                edges = pp['sub2']['edges']
                # print('sub2 escolhido')


            for v , u in edges:
                ww = self.graph.weight(v, u)
                cost_child += ww
                GG_child.add_edge(v, u, weight= ww)

        ## collecting data


        return Chromossome(GG_child, s1, cost_child)


    def std_edges(self, x, y):
        '''
        Uma função auxiliar para padronizar as arestas. Será necessário?
        '''
        return (min(x,y), max(x,y))


    def disjoints_edges_and_subgraph(self, subtree_1 : Graph, subtree_2 : Graph):

        # Definir o conjunto de arestas que somente pertence a subtree_2
        disjoint_edges_2 = set()

        # componentes desconexas de subtree_2
        # esse grafo sera usado por DFS_with_stop para identificar de maneira mais
        # direta, os extremos (vértices comuns) de uma partição de arestas não comuns
        # do pai 2
        GGsub2 = Graph()

        # determinando somente as arestas não comum do pai 2
        for v, u in subtree_2.gen_undirect_edges():
            if not subtree_1.has_edge(v, u):
                GGsub2.add_edge(v, u)
                disjoint_edges_2.add(self.std_edges(v, u))

        return disjoint_edges_2, GGsub2


    def DFS_with_stop(self, rooted_tree_1 : dict, disjoint_edges_2 : set, GGsub2 : Graph, start):

        stack = deque()
        stack.append(start)

        visited = set([start])
        # previous = { start : None }
        previous = set()
        cost = 0

        common_vertice = list()

        while stack :
            v = stack.pop()
            visited.add(v)

            for u in GGsub2.adjacent_to(v):
                if (not u in visited) and (not u in rooted_tree_1):
                    stack.append(u)
                elif u in rooted_tree_1:
                    common_vertice.append(u)

                previous.add(self.std_edges(v, u))
                cost += self.graph.weight(v,u)

                disjoint_edges_2.discard(self.std_edges(v, u))

        partition = {
            'edges' : previous,
            'common' : common_vertice,
            'cost' : cost
                }

        return partition


    def find_uncommon_edges_from_path(self, rtree, a, b, subtree):
        edges = set()
        cost = 0

        v = a
        while rtree[v] :
            previous = rtree[v]

            if not subtree.has_edge(v, previous):
                edges.add(self.std_edges(v, previous))
                w = self.graph.weight(v, previous)
                # print(f"Verificar aresta ({v}, {previous}) - Peso  {w}")
                cost += w

            v = rtree[v]

        u = b
        while rtree[u]:
            previous = rtree[u]

            if not subtree.has_edge(u, previous):
                edges.add(self.std_edges(u, previous))
                w = self.graph.weight(u, previous)
                # print(f"Verificar aresta ({u}, {previous}) - Peso  {w}")
                cost += w

            u = rtree[u]


        return edges, cost


    def common_graph(self, subtree_1 : Graph, subtree_2 : Graph):

        GG_child = Graph()

        for v, u in subtree_1.gen_undirect_edges():
            if subtree_2.has_edge(v, u):
                ww = self.graph.weight(v, u)
                GG_child.add_edge(v, u, weight= ww)

        return GG_child


class GeneticAlgorithm:

    def __init__(self, graph_problem, terminals):

        self.graph = graph_problem
        self.terminals = terminals

        self.population = list()
        self.population_size = 0

        self.best_chromossome = None

        self.gen_population_method = shortest_path

        self.datalog = defaultdict(list)
        # headers to csv file
        self.datalog['crossover'].append(['A_parent', 'B_parent', 'Offspring'])



    def set_crossover_operator(self, operator, probability):
        self.cross_operator = operator
        self.cross_p = probability

    def update_best_chromossome(self, ibest):
        if not self.best_chromossome:
            self.best_chromossome = ibest
        elif ibest.fitness < self.best_chromossome.fitness :
            self.best_chromossome = ibest

    def initial_population(self, size):

        assert size > 0, "Population must have more than 0 individuals"
        assert (size % 2) == 0, "Population size must be a even number"
        self.population_size = size
        initial_nodes = set()
        population = list()

        ## inicialmente escolher todos os vértices terminais
        qtd = 0
        while qtd < self.population_size and qtd < len(self.terminals):
            initial_nodes.add(self.terminals[qtd])
            qtd += 1

        best_cost = float("inf")
        best_for_now = None

        for node in initial_nodes:
            if random.random() < 0.5 :
                subtree, cost = shortest_path(self.graph, node, self.terminals)
            else :
                subtree, cost = shortest_path_with_origin(self.graph, node, self.terminals)

            chromossome = Chromossome(subtree, node, cost)
            population.append(chromossome)

            if cost < best_cost:
                best_cost = cost
                best_for_now = chromossome

        self.population = population
        self.update_best_chromossome(best_for_now)

    def recombine(self):

        offsprings = list()
        pool_size = self.population_size
        count = 0


        while count < pool_size:
            p1, p2 = random.sample(self.population, k=2)
            child = self.cross_operator(p1, p2)
            offsprings.append(child)

            fitness = [p1.fitness, p2.fitness, child.fitness]
            self.datalog["crossover"].append(fitness)

            count += 1

        self.updata_population(offsprings)

    def evaluate(self):

        best_for_now = None
        best_cost = float("inf")

        for chromossome in self.population:
            cost = gg_total_weight(chromossome.subtree)
            chromossome.fitness = cost

            if cost < best_cost:
                best_cost = cost
                best_for_now = chromossome
                # print(best_cost, end="  ")

        self.update_best_chromossome(best_for_now)

    def sort_population(self):
        self.population.sort(key=attrgetter("fitness"))

    def normalized_fitness(self):
        total = sum([c.fitness for c in self.population])

        for c in self.population:
            c.score = (c.fitness / total) * 100

    def selection(self):
        # self.tournament_selection()
        self.wheel_selection()

    def mutate(self):
        raise NotImplementedError("Forma de mutação não definida")

    def tournament_selection(self):
        selected = list()
        K = 2

        for _ in range(self.population_size):
            tournament = random.sample(self.population, K)
            selected.append(max(tournament, key=attrgetter("score")))

        self.population = selected

    def ranking_selection(self):
        pass

    def wheel_selection(self):
        ''' K roulette wheel spins (weighted sampling with replacement)'''
        population = self.population
        weights = [ c.fitness for c in population]

        self.population = random.choices(population, weights, k=self.population_size)

    def updata_population(self, new_population):

        assert len(self.population) == len(new_population), "It is not the same size"
        ## Replace all
        self.population = new_population

    def report_log(self, folder=''):

        if not os.path.exists(folder):
            os.mkdir(folder)

        for key, content in self.datalog.items():
            dest = os.path.join(folder, f'{key}.csv')
            with open(dest, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(content)

        ## best solution found
        best_solution_file = os.path.join(folder,"best_solution.json")
        if os.path.exists(best_solution_file):
            os.remove(best_solution_file)

        with open(best_solution_file, "w") as ff:
            json.dump(self.best_chromossome.subtree.edges, fp=ff, indent=4)



def simulation():

    dataset = os.path.join("datasets","ORLibrary","steinb13.txt")

    reader = ReaderORLibrary()

    STPG = reader.parser(dataset)
    graph = Graph(vertices=STPG.nro_nodes, edges=STPG.graph)

    GA = GeneticAlgorithm(graph, STPG.terminals)
    GA.set_crossover_operator(PartitionCrossover(graph), probability = 1)

    POPULATION_SIZE = 10
    MAX_GENERATION = 100
    iteration = 0

    GA.initial_population(POPULATION_SIZE)
    GA.evaluate()
    GA.sort_population()

    for c in GA.population:
        print(c.fitness)

    while iteration < MAX_GENERATION:
        print("Iteration: ", (iteration + 1), end="\r")
        GA.evaluate()
        # GA.normalized_fitness()
        GA.selection()
        GA.recombine()
        iteration += 1

    GA.evaluate()
    print("\n\n=============================\n\n")
    print(GA.best_chromossome.fitness)


    # OUTPUT_DATA = os.path.join("outputdata", "simulation")
    # GA.report_log(folder=OUTPUT_DATA)

def test():
    import random
    from os import path
    from graph import Reader
    from graph.steiner_heuristics import shortest_path_with_origin

    filename = path.join("datasets", "ORLibrary", "steinb13.txt")

    reader = ReaderORLibrary()

    STPG = reader.parser(filename)

    graph = Graph(vertices=STPG.nro_nodes, edges=STPG.graph)

    ## DETERMINAR DUAS SOLUÇÕES PARCIAIS PELAS HEURISTICAS

    # escolher aleatoriamente um vértice terminal
    s1 = random.choice(STPG.terminals)
    subtree_1, cost1 = shortest_path_with_origin(graph, s1, STPG.terminals) # 0 ate 16

    s2 = random.choice(STPG.terminals)
    subtree_2, cost2 = shortest_path_with_origin(graph, s2, STPG.terminals)

    parent_1 = Chromossome(subtree_1, s1, cost1)
    parent_2 = Chromossome(subtree_2, s2, cost2)

    PX = PartitionCrossover(graph)

    child = PX.crossing(parent_1, parent_2)

if __name__ == "__main__":

    simulation()