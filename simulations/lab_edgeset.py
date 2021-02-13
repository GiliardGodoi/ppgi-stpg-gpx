import os

from ga4stpg.edgeset.crossover import CrossoverRandomWalkRST, CrossoverKruskalRST
from ga4stpg.edgeset.evaluation import EvaluateEdgeSet
from ga4stpg.edgeset.generate import gen_random_walk
from ga4stpg.edgeset.mutate import MutationReplaceByRandomEdge

from ga4stpg.condition import BestKnownReached, Stagnation
from ga4stpg.customevol import GeneticEvolution as Evolution
from ga4stpg.customevol import GeneticPopulation as GPopulation
from ga4stpg.graph.reader import read_problem
from ga4stpg.normalization import normalize
from ga4stpg.selector import roullete
from ga4stpg.tracker import DataTracker
from ga4stpg.util import STEIN_B, display, update_best, update_generation


def simulation_random_walk(params):

    STPG = read_problem("datasets", "ORLibrary", params["dataset"])

    crossover = CrossoverRandomWalkRST(STPG)
    evaluation = EvaluateEdgeSet(STPG)
    mutate = MutationReplaceByRandomEdge(STPG)

    output_data_dir = os.path.join("data","test","edgeset", STPG.name)
    tracker = DataTracker(params['runtrial'],target=output_data_dir)

    population = (GPopulation(
        chromosomes=[gen_random_walk(STPG) for _ in range(params["population_size"])],
        eval_function=evaluation,
        maximize=True)
    .evaluate()
    .normalize(norm_function=normalize)
    .callback(update_best))

    evol = (Evolution()
                .evaluate()
                .normalize(norm_function=normalize)
                .callback(update_best)
                .callback(tracker.log_evaluation)
                .select(selection_func=roullete)
                .crossover(combiner=crossover)
                .mutate(mutate_function=mutate, probability=params['tx_mutation'])
                .callback(update_generation)
                .callback(display, every=100))

    with Stagnation(interval=params["stagnation_interval"]), \
        BestKnownReached(global_optimum=params['global_optimum']):
        result = population.evolve(evol, n=params["n_iterations"])

    tracker.log_simulation(params, STPG, result)
    tracker.report()

    print(result.stoppedby)

def simulation_kruskal_crossover(params):

    STPG = read_problem("datasets", "ORLibrary", params["dataset"])

    crossover = CrossoverKruskalRST(STPG)
    evaluation = EvaluateEdgeSet(STPG)
    mutate = MutationReplaceByRandomEdge(STPG)

    output_data_dir = os.path.join("data","test","edgeset", "kruskal_crossover", STPG.name)
    tracker = DataTracker(params['runtrial'],target=output_data_dir)

    population = (GPopulation(
        chromosomes=[gen_random_walk(STPG) for _ in range(params["population_size"])],
        eval_function=evaluation,
        maximize=True)
    .evaluate()
    .normalize(norm_function=normalize)
    .callback(update_best))

    evol = (Evolution()
                .evaluate()
                .normalize(norm_function=normalize)
                .callback(update_best)
                .callback(tracker.log_evaluation)
                .select(selection_func=roullete)
                .crossover(combiner=crossover)
                .mutate(mutate_function=mutate, probability=params['tx_mutation'])
                .callback(update_generation)
                .callback(display, every=100))

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
        'tx_mutation'         : 0.4,
        # 'tx_crossover'        : 1.0,
        'n_iterations'        : 4_000,
        'stagnation_interval' : 500,
    }

    for dataset, value in STEIN_B[:1]:
        print('='*10,'\n', dataset)
        print('global optimum ', value)
        print('='*10, '\n')
        PARAMS['dataset'] = dataset
        PARAMS['global_optimum'] = value
        for i in range(30):
            PARAMS['runtrial'] = i + 1
            simulation_kruskal_crossover(params=PARAMS)
