from os import path

from ga4stpg.condition import BestKnownReached, Stagnation
from ga4stpg.customevol import GeneticEvolution as Evolution
from ga4stpg.customevol import GeneticPopulation as GPopulation

from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree

from ga4stpg.normalization import normalize
from ga4stpg.selector import tournament
from ga4stpg.tracker import DataTracker
from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedPrimRST
from ga4stpg.tree.mstcrossover import CrossoverPrimRST
from ga4stpg.tree.mutate import (PrimBasedMutation, Prunning,
                                 ReplaceByRandomEdge)
from ga4stpg.util import STEIN_B, display, update_best, update_generation



def simulation(simulation_name, params):

    datasets_folder = path.join("datasets", "ORLibrary")
    filename = path.join(datasets_folder, params["dataset"])
    STPG = ReaderORLibrary().parser(filename)

    print("STPG information", '\n', 10*'- ','\n')
    print("Trial: ", parameters['runtrial'])
    print('Instance: ', STPG.name)
    print('Best Known cost: ', params['global_optimum'])
    print("Nro. Node:", STPG.nro_nodes)
    print("Nro. Edges:", STPG.nro_edges)
    print("Nro. Terminals:", STPG.nro_terminals)
    # print("Terminals: \n", STPG.terminals)

    output_folder = path.join("data", simulation_name, STPG.name)
    tracker = DataTracker(params['runtrial'],target=output_folder)

    generator = GenerateBasedPrimRST(STPG)
    evaluator = EvaluateTreeGraph(STPG)
    crossover = CrossoverPrimRST(STPG)
    prunner   = Prunning(STPG)
    mut_prim  = PrimBasedMutation(STPG)
    replace_random = ReplaceByRandomEdge(STPG)

    population = (GPopulation(
        chromosomes=[ generator() for _ in range(params["population_size"])],
        eval_function=evaluator,
        maximize=True)
    .mutate(mutate_function=prunner, probability=1.0)
    .evaluate()
    .normalize(norm_function=normalize)
    .callback(update_best))

    evol = (Evolution()
        .evaluate()
        .normalize(norm_function=normalize)
        .callback(update_best)
        .callback(tracker.log_evaluation)
        .select(selection_func=tournament)
        .crossover(combiner=crossover)
        .mutate(mutate_function=replace_random, probability=0.3)
        .mutate(mutate_function=mut_prim, probability=0.3)
        .mutate(mutate_function=prunner, probability=0.7)
        .callback(update_generation)
        .callback(display, every=100))

    with Stagnation(interval=params["stagnation_interval"]), \
         BestKnownReached(global_optimum=params['global_optimum']):
        result = population.evolve(evol, n=params["n_iterations"])

    tracker.log_simulation(params, STPG, result)

    best_overall = result.documented_best
    test, response = is_steiner_tree(best_overall.chromosome, STPG)

    tracker.log_bestIndividual(best_overall, test, response)

    tracker.report()



if __name__ == "__main__":

    parameters = {
        'runtrial' : 0,
        'dataset' : 'steinb1.txt',
        'global_optimum'       : 82,
        'population_size'     : 100,
        'tx_mutation'         : 0.3,
        'tx_crossover'        : 1.0,
        'n_iterations'        : 4_000,
        'stagnation_interval' : 500,
    }

    for dataset, value in STEIN_B:
        print('='*10,'\n', dataset)
        print('global optimum ', value)
        print('='*10, '\n')
        parameters['dataset'] = dataset
        parameters['global_optimum'] = value
        for i in range(50):
            parameters['runtrial'] = i + 1
            simulation("S5PrimRST_pruner10Mst", parameters)
