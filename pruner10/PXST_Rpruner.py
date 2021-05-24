from os import path

from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree

from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.mstcrossover import CrossoverGreedyPrim
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mutate import ReplaceByRandomEdge, PrimBasedMutation, Prunning
from ga4stpg.tree.pxpartition import PartitionCrossoverSteinerTree

from ga4stpg.condition import BestKnownReached, Stagnation
from ga4stpg.customevol import GeneticEvolution as Evolution
from ga4stpg.customevol import GeneticPopulation as GPopulation
from ga4stpg.normalization import normalize
from ga4stpg.selector import roullete
from ga4stpg.tracker import DataTracker
from ga4stpg.util import STEIN_B, display, update_best, update_generation

def simulation(name, params):

    filename = path.join("datasets", "ORLibrary", params["dataset"])
    stpg = ReaderORLibrary().parser(filename)

    print("STPG information", '\n', 10*'- ','\n')
    print('Instance: ', stpg.name)
    print('Best Known cost: ', params['global_optimum'])
    print("Nro. Node:", stpg.nro_nodes)
    print("Nro. Edges:", stpg.nro_edges)
    print("Nro. Terminals:", stpg.nro_terminals)
    # print("Terminals: \n", stpg.terminals)
    print("Trial nro: ", parameters['runtrial'])

    generator = GenerateBasedRandomWalk(stpg)
    evaluator = EvaluateTreeGraph(stpg)
    prunner   = Prunning(stpg)
    ### prim_mutation  = PrimBasedMutation(stpg)
    replace_random = ReplaceByRandomEdge(stpg)
    partition_cx = PartitionCrossoverSteinerTree(stpg)

    output_data_dir = path.join("data", name, stpg.name)
    tracker = DataTracker(parameters['runtrial'], target=output_data_dir)

    population = (GPopulation(
        chromosomes=[ generator() for _ in range(params['population_size'])],
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
        .select(selection_func=roullete)
        .crossover(combiner=partition_cx)
        .mutate(mutate_function=replace_random, probability=0.3)
        .mutate(mutate_function=prunner, probability=1.0)
        .callback(update_generation)
        .callback(display, every=100))

    with Stagnation(interval=params["stagnation_interval"]), \
        BestKnownReached(global_optimum=params['global_optimum']):
        result = population.evolve(evol, n=params["n_iterations"])

    tracker.log_simulation(params, stpg, result)

    best_overall = result.documented_best
    test, response = is_steiner_tree(best_overall.chromosome, stpg)

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
            simulation("PXST_Rpruner10", parameters)