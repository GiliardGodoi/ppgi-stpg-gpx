import os
import random
import statistics
import time
from collections import deque

from ga_simplestpartition import SimplePartitionCrossover
from genetic.base import BaseGA, Operator
from genetic.chromosome import BinaryChromosome, TreeBasedChromosome
from genetic.crossover import crossover_2points
from genetic.datalogger import DataLogger
from genetic.mutation import mutation_flipbit
from genetic.selection import roullete_selection
from graph import Graph, ReaderORLibrary
from graph.disjointsets import DisjointSets
from graph.priorityqueue import PriorityQueue
from util import (convert_binary2treegraph, convert_treegraph2binary,
                  evaluate_binary, evaluate_treegraph,
                  random_binary_chromosome, random_treegraph_chromosome)

class HybridGeneticAlgorithm(BaseGA):

    def __init__(self, STPG, **kwargs):
        super().__init__(**kwargs)
        self.STPG = STPG
        self.GRAPH = Graph(edges=STPG.graph)
        self.terminals = set(STPG.terminals)
        self.nro_vertices = STPG.nro_nodes
        self.chromosome_length = STPG.nro_nodes - STPG.nro_terminals

    def generate_new_individual(self, **kwargs):
        return random_binary_chromosome(self.chromosome_length)

    def eval_chromosome(self, chromosome):

        def penality(nro_partitions):
            return (nro_partitions - 1) * 100

        if type(chromosome) is BinaryChromosome:
            return evaluate_binary(chromosome,self.GRAPH, self.terminals, self.nro_vertices, penality)

        elif type(chromosome) is TreeBasedChromosome:
            return evaluate_treegraph(chromosome, penality)
        else:
            raise TypeError("chromosome cannot be evaluated")

    def mutation(self, active=False):
        if active:
            super().mutation()

class Simulation:

    def __init__(self, name='teste', **kwargs):
        self.name = name

        self.STPG = None
        self.GRAPH = None

        self.CONTROL_FLAG = True
        self.MAX_ITERATIONS = 10000
        self.MAX_LAST_IMPROVEMENT = 500
        self.POPULATION_SIZE = 100

    def setUp(self, dataset='', **kwargs):
        print("executing setUP...")

        self.MAX_ITERATIONS = kwargs.get("max_iterations", self.MAX_ITERATIONS)

        self.setup_dataset(dataset,**kwargs)
        self.setup_ga(**kwargs)

    def setup_dataset(self, dataset, **kwargs):
        print(f"setting instance problem from dataset : {dataset}")
        filename = os.path.join("datasets", "ORLibrary", dataset)
        reader = ReaderORLibrary()
        self.STPG = reader.parser(filename)
        self.GRAPH = Graph(edges=self.STPG.graph)

    def setup_ga(self, **kwargs):
        print("setting GA configurations ...")
        self.GA = HybridGeneticAlgorithm(self.STPG)
        self.CONTROL_FLAG = True # if True --> BinaryRepresentation

        self.GA.tx_crossover = 0.85
        self.GA.tx_mutation =  0.4
        self.GA.population_size = self.POPULATION_SIZE


        self.gpx_strategy = SimplePartitionCrossover(self.GRAPH)

        self.GA.crossover_operator = crossover_2points if self.CONTROL_FLAG else self.gpx_strategy
        self.GA.selection_operator = roullete_selection
        self.GA.mutation_operator = mutation_flipbit

        folder = os.path.join("outputdata", self.name, self.STPG.name)
        trial = str(kwargs.get("nro_trial", ''))
        self.GA.logger = DataLogger(prefix=f"trial_{trial}", outputfolder=folder)
        self.GA.logger.register("simulation", "csv",
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

    def check_stop_criterion(self, **kwargs):
        iteration = kwargs.get("iteration", self.MAX_ITERATIONS)
        optimum = kwargs.get("global_optimum", 0)

        if iteration >= self.MAX_ITERATIONS:
            return (False, "max_generation_reached")
        elif self.GA.last_time_improvement > self.MAX_LAST_IMPROVEMENT:
            return (False, "stagnation")
        elif self.GA.best_chromosome.cost == optimum :
            return (False, "global_optimum_reached")
        else :
            return (True, "non stop")

    def run(self, filename, **kwargs):
        self.setUp(dataset=filename, **kwargs)

        optimum = kwargs.get("global_optimum", 0)

        print("Starting GA execution ...")
        GA = self.GA
        print("generate_population ...")
        GA.generate_population()
        iteration = 0
        start_at = time.time()
        running = True
        while running:
            print("                                                 Iteration:  ", iteration, end="\r")
            GA.evaluate(iteration=iteration)
            GA.sort_population()
            GA.selection()
            GA.recombine()
            GA.mutation(active=self.CONTROL_FLAG)
            iteration += 1
            GA.last_time_improvement += 1
            running, why_stopped = self.check_stop_criterion(iteration=iteration, global_optimum=optimum)
            if running and (iteration % 200) == 0:
                self.change_the_game()

        GA.evaluate()
        GA.normalize(iteration=iteration)

        ends_at = time.time()

        data = {
            "nro_trial" : kwargs.get("trial", 1),
            "global_optimum" : kwargs.get("global_optimum", None),
            "iterations" : iteration,
            "run_time" : (ends_at - start_at),
            "max_last_improvement" : self.GA.last_time_improvement,
            "why_stopped" : why_stopped
        }
        self.finish_it(**data)

    def run_trials(self, filename, total_trials, optimum):

        for trial in range(1, total_trials+1):
            print(f"RUNNING ....... {trial}")
            self.run(filename, nro_trial=trial, global_optimum=optimum)

    def finish_it(self, **kwargs):

        self.GA.logger.log("simulation",
            kwargs.get("nro_trial", 0),
            self.STPG.name,
            self.STPG.nro_nodes,
            self.STPG.nro_edges,
            self.STPG.nro_terminals,
            self.GA.tx_crossover,
            self.GA.tx_mutation,
            kwargs.get("global_optimum", None),
            self.GA.best_chromosome.cost,
            self.GA.best_chromosome.fitness,
            self.POPULATION_SIZE,
            self.MAX_ITERATIONS,
            kwargs.get("iterations", 0),
            kwargs.get("run_time", 0),
            kwargs.get("max_last_improvement", 0),
            kwargs.get("why_stopped", "not_provided")
            )

        ## Generates the reports
        self.GA.logger.report()

    def change_the_game(self):
        print("changing ...                                         ")
        # 1st thing to do: change the control flag
        self.CONTROL_FLAG = not self.CONTROL_FLAG

        # 2nd one is change the crossover strategy
        self.GA.crossover_operator = crossover_2points if self.CONTROL_FLAG else self.gpx_strategy
        print(self.GA.crossover_operator.__class__.__name__) ##

        # 3rd one is convert the chromosome representation
        newpopulation = list()
        for chromosome in self.GA.population:
            if self.CONTROL_FLAG:
                newpopulation.append(convert_treegraph2binary(chromosome, self.GA.terminals, self.GA.nro_vertices))
            else:
                newpopulation.append(convert_binary2treegraph(chromosome,self.GA.GRAPH, self.GA.terminals, self.GA.nro_vertices))

        # 4th one is update the population
        self.GA.population = newpopulation


def test_1():
    simulation = Simulation()

    simulation.MAX_ITERATIONS = 1000
    simulation.POPULATION_SIZE = 10

    simulation.run("steinb13.txt")

def main():
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

    for filename, optimum in DATASETS[12:]:
        simulation = Simulation(name="20200422_hybridi")
        simulation.MAX_ITERATIONS = 10000
        simulation.POPULATION_SIZE = 100
        simulation.run_trials(filename, NUMBER_OF_TRIALS, optimum)

if __name__ == "__main__":
    # test_1()
    main()
