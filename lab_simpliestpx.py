import os
import time
from statistics import variance

from base.binary.combiner import crossover_1point, crossover_2points
from base.chromosome import random_binary
from base.condition import IterationLimit, Stagnation
from base.customevol import SteinerEvolution as Evolution
from base.customevol import SteinerPopulation as Population
from base.mutate import flip_onebit
from base.normalization import normalize
from base.pickers import random_picker
from base.selector import roullete
from base.tracker import DataTracker
from base.util import STEIN_B, display, update_best, update_generation
from evol.exceptions import StopEvolution
from graph import Graph
from graph.reader import read_problem
from pxsimpliest import SimpliestPX
from treetools import Converter, Eval


def check_variance(population : 'Population'):
    fitness_var = variance(p.fitness for p in population)
    if fitness_var < 10 :
        raise StopEvolution(f"Variance == {fitness_var}")

def is_connected(individual : 'SteinerIndividual'):
    return individual.qtd_partitions == 1

def kapsalis_gpx(simulation_name, params : dict):

    STPG = read_problem("datasets", "ORLibrary", params["dataset"])
    lenght = STPG.nro_nodes - STPG.nro_terminals
    converter = Converter(STPG)
    tracker = DataTracker(params['runtrial'], target=os.path.join("outputdata", simulation_name, STPG.name))

    population = (Population(chromosomes=[ random_binary(lenght) for _ in range(params["population_size"]) ],
                            eval_function=Eval(STPG),
                            maximize=True)
                            .evaluate()
                            .callback(normalize)
                            .callback(update_best))

    binary = (Evolution()
                .evaluate()
                .callback(normalize)
                .callback(update_best)
                .callback(tracker.log_evaluation)
                .select(selection_func=roullete)
                .crossover(combiner=crossover_2points, parent_picker=random_picker)
                .mutate(mutate_function=flip_onebit, probability=0.5)
                .callback(update_generation)
                .callback(display, every=10)
                )

    treegraph = (Evolution()
                .evaluate()
                .callback(normalize)
                .callback(update_best)
                .callback(tracker.log_evaluation)
                .select(selection_func=roullete)
                .crossover(combiner=SimpliestPX(STPG), parent_picker=random_picker) # .mutate(mutate_function=flip_onebit, probability=0.2)
                .callback(update_generation)
                .callback(display, every=10)
                )

    hybridi = (Evolution()
                .repeat(binary, n=params['iteration_binary'])
                .map(converter.binary2treegraph)
                .evaluate()
                .callback(normalize)
                .filter(is_connected)
                .callback(display)
                .repeat(treegraph, n=params['iteration_treegraph'])
                .map(converter.treegraph2binary))

    max_generation = params['n_iterations'] * (params['iteration_binary'] + params['iteration_treegraph'])

    with IterationLimit(limit=max_generation), \
        Stagnation(interval=params["stagnation_interval"]):
        result = population.evolve(hybridi, n=params["n_iterations"])

    tracker.log_simulation(params, STPG, result)
    tracker.report()

    return result

if __name__ == "__main__":

    PARAMS = {
        'runtrial' : 0,
        'dataset' : 'steinb4.txt',
        'global_optimum'       : 59,
        'population_size'     : 50,
        'tx_mutation'         : 0.2,
        'n_iterations'        : 10,
        'iteration_binary'    : 50,
        'iteration_treegraph' : 50,
        'stagnation_interval' : 1_000,
    }


    kapsalis_gpx("20200622_hybridi-test", PARAMS)
