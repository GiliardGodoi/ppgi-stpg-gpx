import random
import statistics
from operator import attrgetter

from genetic.chromosome import BinaryChromosome
from genetic.crossover import crossover_2points
from genetic.datalogger import BaseLogger
from genetic.mutation import mutation_flipbit
from genetic.selection import roullete_selection


class Operator:

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.operation(*args, **kwargs)

    def operation(self, *args, **kwargs):
        raise NotImplementedError("This method must be implemented by the subclass")

class BaseGA:
    '''Define the basic class to define a GA'''

    def __init__(self, *args, **kwargs):

        self.population = list()
        self.population_size = 10
        self.selected_population = list()

        self.crossover_operator = crossover_2points
        self.selection_operator = roullete_selection
        self.mutation_operator = mutation_flipbit

        self.tx_crossover = 0.9
        self.tx_mutation = 0.2

        self.best_chromosome = None
        self.last_time_improvement = 0

        self.__logger = BaseLogger()

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger):
        print('logger...')
        self.__logger = logger
        self.__logger.register('best_fitness', 'csv', 'iteration', 'cost', 'fitness')
        self.__logger.register('best_from_round', 'csv', 'iteration', 'cost', 'fitness')
        self.__logger.register("evaluation", 'csv', "iteration" , "penalization", "average", "std_deviation")

    def generate_new_individual(self, **kwargs):
        raise NotImplementedError("")

    def generate_population(self, **kwargs):
        self.population_size = kwargs.get("population_size", self.population_size)
        assert self.population_size > 0, "Population must have more than 0 individuals"
        assert (self.population_size % 2) == 0, "Population size must be a even number"

        counter = 0
        newpopulation = list()

        while counter < self.population_size:
            newpopulation.append(self.generate_new_individual(**kwargs))
            counter += 1

        self.update_population(newpopulation, **kwargs)

    def eval_chromosome(self, chromosome):
        raise NotImplementedError("")

    def evaluate(self, **kwargs):
        '''Evaluates the entire population.

        Returns:
            int or float : total population cost
            int or float : maximun cost from the current generation
            float : average cost from the current generation
        '''
        evaluated_costs = list()
        count_penalized = 0
        for chromosome in self.population:
            cost, is_penalized = self.eval_chromosome(chromosome)
            chromosome.cost = cost
            evaluated_costs.append(cost)
            if is_penalized: count_penalized += 1

        self.normalize(penalized=count_penalized, **kwargs)

    def selection(self):
        self.selected_population = self.selection_operator(self.population, self.population_size)

    def recombine(self):
        newpopulation = list()
        population_size = self.population_size
        count = 0

        while count < population_size:
            parent_a, parent_b = random.sample(self.selected_population, k=2)
            ## Como a operação de seleção é executada.
            child = self.crossover_operator(parent_a, parent_b)

            if isinstance(child, (list, tuple)) :
                newpopulation.extend(child)
                count += len(child)
            else :
                newpopulation.append(child)
                count += 1

        self.update_population(newpopulation)

    def mutation(self, **kwargs):
        population_size = self.population_size
        count = 0
        while count < population_size:
            if random.random() < self.tx_mutation:
                self.population[count] = self.mutation_operator(self.population[count])
            count += 1

    def normalize(self, **kwargs):
        best_fitness_value = -float("inf")
        best_chromosome = None

        max_cost = max(chromosome.cost for chromosome in self.population)
        population_fitness = list()

        for chromosome in self.population:
            fitness = max_cost - chromosome.cost
            chromosome.fitness = fitness
            population_fitness.append(fitness)

            if chromosome.fitness > best_fitness_value:
                best_fitness_value = chromosome.fitness
                best_chromosome = chromosome

        self.logger.log("evaluation",
            kwargs.get("iteration", 0),
            kwargs.get("penalized", None),
            statistics.mean(population_fitness),
            statistics.stdev(population_fitness))

        self.update_best_chromosome(best_chromosome, **kwargs)

    def update_population(self, newpopulation, **kwargs):
        '''It's execute the population replace strategy'''

        assert len(newpopulation) == self.population_size, "It is not the same size"
        ## Replace all
        self.population = newpopulation

    def update_best_chromosome(self, chromosome, **kwargs):
        if self.best_chromosome is None:
            self.best_chromosome = chromosome
            self.__logger.log('best_fitness', kwargs.get("iteration", 0), chromosome.cost, chromosome.fitness)
            self.last_time_improvement = 0

        elif self.best_chromosome.cost > chromosome.cost:
            self.best_chromosome = chromosome
            self.__logger.log('best_fitness', kwargs.get("iteration", 0), chromosome.cost, chromosome.fitness)
            self.last_time_improvement = 0

        self.__logger.log('best_from_round', kwargs.get("iteration", 0), chromosome.cost, chromosome.fitness)

    def sort_population(self):
        '''Sort the population by fitness attribute'''
        self.population.sort(key=attrgetter("fitness"))
