from os import path
from random import choice, shuffle

from ga4stpg.condition import BestKnownReached, Stagnation
from ga4stpg.customevol import GeneticEvolution as Evolution
from ga4stpg.customevol import GeneticPopulation as GPopulation
from ga4stpg.graph.reader import read_problem
from ga4stpg.normalization import normalize
from ga4stpg.selector import roullete
from ga4stpg.tracker import DataTracker
from ga4stpg.util import STEIN_B, display, update_best, update_generation

from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedPrimRST
from ga4stpg.tree.mutate import ReplaceByRandomEdge
from ga4stpg.tree.pxcrossover import PXTree


def non_selection(population):
    return population


def simulation_pxtree_crossover_primbased_population(params):

    STPG = read_problem("datasets", "ORLibrary", params["dataset"])
    crossover = PXTree(STPG)
    evaluator = EvaluateTreeGraph(STPG)
    generator = GenerateBasedPrimRST(STPG)
    mutate = ReplaceByRandomEdge(STPG)

    output_data_dir = path.join("data","test","treegraph", STPG.name)
    tracker = DataTracker(params['runtrial'],target=output_data_dir)

    population = (GPopulation(
        chromosomes=[ generator() for _ in range(params["population_size"])],
        eval_function=evaluator,
        maximize=True)
    .evaluate()
    .normalize(norm_function=normalize)
    .callback(update_best))

    evol = (Evolution()
                .evaluate()
                .normalize(norm_function=normalize)
                .callback(update_best)
                .callback(tracker.log_evaluation)
                .select(selection_func=non_selection)
                .crossover(combiner=crossover)
                .mutate(mutate_function=mutate, probability=params['tx_mutation'])
                .callback(update_generation)
                .callback(display, every=100))
    #
    with Stagnation(interval=params["stagnation_interval"]), \
        BestKnownReached(global_optimum=params['global_optimum']):
        result = population.evolve(evol, n=params["n_iterations"])

    tracker.log_simulation(params, STPG, result)
    tracker.report()

    print(result.stoppedby)

if __name__ == "__main__":
    PARAMS = {
        'runtrial' : 0,
        'dataset' : 'steinb1.txt',
        'global_optimum'       : 82,
        'population_size'     : 100,
        'tx_mutation'         : 0.3,
        # 'tx_crossover'        : 1.0,
        'n_iterations'        : 4_000,
        'stagnation_interval' : 500,
    }

    for dataset, value in STEIN_B[17:]:
        print('='*10,'\n', dataset)
        print('global optimum ', value)
        print('='*10, '\n')
        PARAMS['dataset'] = dataset
        PARAMS['global_optimum'] = value
        for i in range(15):
            PARAMS['runtrial'] = i + 1
            simulation_pxtree_crossover_primbased_population(params=PARAMS)