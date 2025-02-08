# -*- coding: utf-8 -*-
import os
import random
import statistics
import time
from collections import defaultdict
from operator import attrgetter

from genetic.base import BaseGA
from genetic.chromosome import BinaryChromosome
from genetic.crossover import crossover_2points
from genetic.datalogger import BaseLogger, DataLogger
from genetic.mutation import mutation_flipbit
from genetic.selection import roullete_selection
from graph import Graph, ReaderORLibrary, SteinerTreeProblem
from graph.algorithms import prim
from graph.steiner import prunning_mst


class GeneticAlgorithm(BaseGA):
    '''A binary GA'''
    def __init__(self, STPG : SteinerTreeProblem):
        super().__init__()
        self.graph = Graph(edges=STPG.graph)
        self.terminals = set(STPG.terminals)
        self.nro_vertices = STPG.nro_nodes

        self.tx_crossover = 0.85
        self.tx_mutation = 0.2

        # Quantidade de vértices não obrigatórios.
        self.chromosome_length = STPG.nro_nodes - STPG.nro_terminals

        ## MAPPING NODES DICTIONARY
        # O cromossomo representa unicamente os vértices não-obrigatórios de um grafo.
        # por isso uma estrutura de dicionário é utilizado para mapear o indice do gene
        # no cromossomo para o vértice que aposição representa.
        # O dicionário possui a forma:
        #       { <indice posição do vetor> : <vértice representado> }
        self.map_nodes = dict()
        index = 0 # o array (list) de genes começa com indice igual a 0
        for node in range(1, (STPG.nro_nodes+1)):
            if not node in self.terminals:
                self.map_nodes[index] = node
                index += 1

        self.logger = DataLogger(outputfolder="teste")

    def __mapper(self, index):
        return self.map_nodes[index]

    def generate_new_individual(self, **kwargs):
        '''Generates a single chromosome'''
        length = self.chromosome_length

        genes = ''.join(random.choices(['0', '1'], k=length))

        return BinaryChromosome(genes)

    def generate_population(self, **kwargs):

        super().generate_population(**kwargs)

        opt = kwargs.get("opt", None)

        if opt and opt == "MST" :
            # retira um elemento qualquer da populacao
            self.population.pop() # tamanho - 1
            # Acrescenta um individuo onde todos os vértices participam
            genes = ''.join(['1'] * self.chromosome_length)
            self.population.append(BinaryChromosome(genes))
            print("MST seeded...")

        elif opt and opt == "TRIM" :
            # retira um elemento qualquer da populacao
            self.population.pop() # tamanho - 1
            mstsubgraph = prunning_mst(self.graph, # grafo instância do problema
             random.choice(list(self.terminals)),  # escolhe um vértice terminal aleatório
             self.terminals)                       # vértices terminais

            genes = self.chromosome_from_subgraph(mstsubgraph)
            self.population.append(BinaryChromosome(genes))
            print("TRIM seeded")

        assert len(self.population) == self.population_size, "population doesn't have the same size as before"

    def eval_chromosome(self, chromosome : BinaryChromosome):
        ''' Evaluete chromosome's fitness.

        Parameter
            chromosome : Chromosome class

        Return
            int : fitness value. Though it use MST to compute fitness, it might added to a penalty value.
            bool : indicates if it was added a penalization

        Notes
            1. Define o subgrafo induzido pela união dos vértices presentes no cromossomo
                (vértices não-obrigatórios) e vértices terminais - uma aresta pertence ao
                subgrafo induzido se os seus vértices extremos pertencem a esse subconjunto.

            2. Calcula a MST de cada componente conexa k ( com k >= 1) obtendo um custo total;

            3. Define uma penalidade linearmente dependente de k

            4. Transforma em um problema de maximização subtraindo de cada fitness o maior valor de fitness observado na população.
        '''
        subgraph, vertices = self.subgraph_from_chromosome(chromosome)

        penalize = lambda k : (k - 1) * 100
        total_cost = 0
        nro_partition = 0

        while vertices:
            v = vertices.pop()
            mst, cost = prim(subgraph, v)
            total_cost += cost
            nro_partition += 1

            vertices = vertices.difference(mst.keys())

        penalization = penalize(nro_partition)
        total_cost = total_cost + penalization

        return total_cost, penalization > 0

    def evaluate(self, **kwargs):

        population_cost = 0
        max_cost = 0

        best_fitness = - float("inf") # minus infinity
        bfn_chromosome = None # Best For Now

        count_penalized = 0

        for chromosome in self.population:
            cost, penalized = self.eval_chromosome(chromosome)
            if penalized: count_penalized += 1

            chromosome.cost = cost
            population_cost += cost

            if cost > max_cost:
                max_cost = cost

        # O procedimento abaixo pode ser considerando uma operação de
        # NORMALIZAÇÃO
        # foi mantido no método de avaliação  porque:
        # 1. O maior custo já foi determinado; não precisaria determinar novamente
        # no método 'self.normalize'
        # 2. No artigo ele descrito como um procedimento do fitness.
        # Então resolvi ser consistente com o artigo original.
        # Mas esse procedimento poderia ser implementado no método de normalização
        population_fitness = list()
        for chromosome in self.population:
            chromosome.fitness = max_cost - chromosome.cost
            population_fitness.append(chromosome.fitness)

            if chromosome.fitness > best_fitness:
                best_fitness = chromosome.fitness
                bfn_chromosome = chromosome

        self.update_best_chromosome(bfn_chromosome,**kwargs)
        self.logger.log("evaluation",
            kwargs.get("iteration", 0),
            count_penalized,
            statistics.mean(population_fitness),
            statistics.stdev(population_fitness))

        return population_cost

    def normalize(self,**kwargs):
        pass

    def subgraph_from_chromosome(self, chromosome : BinaryChromosome):
        '''Define the subgraph from a particular chromosome representation.

        Parameter:
            chromosome : Chromosome

        Returns
            Graph: represents the subtree induced by the vertices presented in the chromosome.
            set : all the vertices labels in a set - just to save effort.

        '''
        vertices = set(self.terminals)
        subgraph = Graph()
        dones = set()

        for index, gene in enumerate(chromosome.genes):
            if gene == '1':
                node = self.__mapper(index)
                vertices.add(node)

        for v in vertices:
            subgraph.add_node(v)
            for u in self.graph.adjacent_to(v):
                if (u in vertices) and (u not in dones):
                    w = self.graph.weight(v, u)
                    subgraph.add_edge(v, u, weight=w)
            dones.add(v)

        return subgraph, vertices

    def chromosome_from_subgraph(self, subgraph: Graph):
        '''Enconde a subgraph using the chromosome representation

        Notes:
        It's dont check if subgraph is actually a subgraph from self.graph
        '''
        genes = list()
        all_vertices = ['0'] * self.nro_vertices
        terminals = set(self.terminals)

        for v in subgraph.vertices:
            all_vertices[v-1] = '1'

        for index, value in enumerate(all_vertices):
            node = index + 1
            if node not in terminals:
                genes.append(value)

        return ''.join(genes)


def test(dataset):
    from tqdm import tqdm
    from graph.util import has_cycle

    reader = ReaderORLibrary()
    STPG = reader.parser(dataset)

    GA = GeneticAlgorithm(STPG)
    GA.logger = BaseLogger()

    GA.generate_population(population_size=100)

    time_starts = time.time()
    for iteration in tqdm(range(0,50)):
        # print("Iteration: ", (iteration + 1), end="\r")
        GA.evaluate()
        GA.selection()
        GA.recombine() # problema identificado aqui
        GA.mutation()

    time_ends = time.time()

    GA.evaluate()

    GA.logger.report()


    print("Total run time: ", (time_ends - time_starts))

    subgraph, _ = GA.subgraph_from_chromosome(GA.best_chromosome)

    dtree, cost = prim(subgraph, STPG.terminals[0])
    print("Final prim cost: ", cost)
    print("Final fitness: ", GA.eval_chromosome(GA.best_chromosome))

    test_genes = GA.chromosome_from_subgraph(subgraph)

    print(test_genes)
    print(GA.best_chromosome.genes)
    print(all( z == w for z, w in zip(test_genes, GA.best_chromosome.genes)))


def simulation(dataset: str, nro_trial = 0, global_optimum = 0):
    '''Run a simulation trial'''

    # Lendo a instância do problema
    reader = ReaderORLibrary()
    STPG = reader.parser(dataset)

    # Definindo o diretório que será destinado os dados
    datafolder = os.path.join("outputdata", "teste", STPG.name)
    if not os.path.exists(datafolder):
        os.makedirs(datafolder) # or mkdir

    ## Parâmetros  comuns a cada execução
    GA = GeneticAlgorithm(STPG)
    GA.tx_crossover = 0.85
    GA.tx_mutation =  0.2
    POPULATION_SIZE = 100
    MAX_GENERATION = 10000
    MAX_LAST_IMPROVEMENT = 500
    GLOBAL_OPTIMUN = global_optimum

    ## Definindo a função com os critérios de parada

    def check_stop_criterions(iteration=0):

        if iteration >= MAX_GENERATION:
            return (False, "max_generation_reached")
        elif GA.last_time_improvement > MAX_LAST_IMPROVEMENT:
            return (False, "stagnation")
        elif GA.best_chromosome.cost == GLOBAL_OPTIMUN :
            return (False, "global_optimum_reached")
        else :
            return (True, "non stop")

    ## Configurando a coleta de informações
    GA.logger.prefix = f'trial_{nro_trial}'
    GA.logger.mainfolder = datafolder

    GA.logger.register("simulation", "csv",
            "nro_trial",
            "instance_problem",
            "nro_nodes",
            "nro_edges",
            "nro_terminals",
            "tx_crossover",
            "tx_mutation",
            "global_optimum",
            "best_cost",
            "best_fitness",
            "population_size",
            "max_generation",
            "iterations",
            "run_time",
            "max_last_improvement",
            "why_stopped"
            )

    ## =============================================================
    ## EXECUTANDO O ALGORITMO GENÉTICO

    GA.generate_population(population_size=POPULATION_SIZE)
    # GA.generate_population(POPULATION_SIZE, opt="MST")
    running = True
    epoch = 0
    timestart = time.time()
    while running:
        GA.evaluate(iteration=epoch)
        GA.selection()
        GA.recombine()
        GA.mutation()
        GA.last_time_improvement += 1
        epoch += 1
        running, why_stopped = check_stop_criterions(iteration=epoch)
    time_ends = time.time()

    GA.evaluate(iteration=epoch)

    ## Record general simulation data
    GA.logger.log("simulation",
            nro_trial,
            STPG.name,
            STPG.nro_nodes,
            STPG.nro_edges,
            STPG.nro_terminals,
            GA.tx_crossover,
            GA.tx_mutation,
            GLOBAL_OPTIMUN,
            GA.best_chromosome.cost,
            GA.best_chromosome.fitness,
            POPULATION_SIZE,
            MAX_GENERATION,
            epoch,
            (time_ends - timestart),
            MAX_LAST_IMPROVEMENT,
            why_stopped
            )

    ## Generates the reports
    GA.logger.report()


def main():
    import os
    import time
    from tqdm import tqdm
    from graph import ReaderORLibrary

    NUMBER_OF_TRIALS = 30
    DATASETS = [
        ("steinb1.txt",   82), # 0
        ("steinb2.txt",   83),
        ("steinb3.txt",  138),
        ("steinb4.txt",   59),
        ("steinb5.txt",   61), # 4
        ("steinb6.txt",  122),
        ("steinb7.txt",  111),
        ("steinb8.txt",  104),
        ("steinb9.txt",  220), # 8
        ("steinb10.txt",  86),
        ("steinb11.txt",  88),
        ("steinb12.txt", 174),
        ("steinb13.txt", 165), # 12
        ("steinb14.txt", 235),
        ("steinb15.txt", 318), # 14
        ("steinb16.txt", 127), # 15
        ("steinb17.txt", 131), # 16
        ("steinb18.txt", 218), # 17
    ]

    # Prestar atenção ao tempo de execução. Isso pode demorar bastante.
    for filename, global_optimum in DATASETS:
        dataset = os.path.join("datasets","ORLibrary", filename)
        if os.path.exists(dataset):
            print(dataset, global_optimum)
            print("Executing trial for : ", filename, end="\r")
            for nro in range(1, NUMBER_OF_TRIALS + 1):
                print("Executing trial for : ", filename," Trial nro: ", nro, end="\r")
                simulation(dataset, nro_trial=nro, global_optimum=global_optimum)


if __name__ == "__main__":
    import os
    test(os.path.join("datasets","ORLibrary","steinb1.txt"))
    # main()
