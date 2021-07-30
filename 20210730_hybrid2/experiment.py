from operator import attrgetter
from os import path

from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree

from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mutate import ReplaceByRandomEdge, PrimBasedMutation, Prunning
from ga4stpg.tree.pxpartition import PartitionCrossoverSteinerTree
from ga4stpg.tree.mstcrossover import CrossoverPrimRST

from ga4stpg.condition import BestKnownReached, Stagnation
from ga4stpg.customevol import GeneticEvolution as Evolution
from ga4stpg.customevol import GeneticPopulation as GPopulation
from ga4stpg.normalization import normalize
from ga4stpg.selector import roullete, tournament
from ga4stpg.tracker import DataTracker
from ga4stpg.util import STEIN_C, display, update_best, update_generation

def display_experiment_params(params, stpg):
    print("STPG information", '\n', 10*'- ','\n')
    print('Instance: ', stpg.name)
    print('Best Known cost: ', params['global_optimum'])
    print("Nro. Node:", stpg.nro_nodes)
    print("Nro. Edges:", stpg.nro_edges)
    print("Nro. Terminals:", stpg.nro_terminals)
    # print("Terminals: \n", stpg.terminals)
    print("Trial nro: ", parameters['runtrial'])

def experiment(name, params):

    filename = path.join("datasets", "ORLibrary", params["dataset"])
    stpg = ReaderORLibrary().parser(filename)

    display_experiment_params(params, stpg)

    generator = GenerateBasedRandomWalk(stpg)
    evaluator = EvaluateTreeGraph(stpg)
    pruner    = Prunning(stpg)
    prim_mutation  = PrimBasedMutation(stpg)
    replace_random = ReplaceByRandomEdge(stpg)
    crossover_pxst = PartitionCrossoverSteinerTree(stpg)
    crossover_primRst = CrossoverPrimRST(stpg)

    output_data_dir = path.join("data", name, stpg.name)
    tracker = DataTracker(parameters['runtrial'], target=output_data_dir)

    population = (GPopulation(
        chromosomes=[ generator() for _ in range(params['population_size'])],
        eval_function=evaluator,
        maximize=True)
    .mutate(mutate_function=pruner, probability=1.0)
    .evaluate()
    .normalize(norm_function=normalize)
    .callback(update_best))

    pipe1 = (Evolution()
        .evaluate()
        .normalize(norm_function=normalize)
        .callback(update_best)
        .callback(tracker.log_evaluation)
        .select(selection_func=tournament)
        .crossover(combiner=crossover_primRst)
        .mutate(mutate_function=replace_random, probability=0.3)
        .mutate(mutate_function=prim_mutation, probability=0.3)
        .mutate(mutate_function=pruner, probability=1.0)
        .callback(update_generation)
        .callback(display, every=50))

    pipe2 = (Evolution()
        .evaluate()
        .normalize(norm_function=normalize)
        .callback(update_best)
        .callback(tracker.log_evaluation)
        .select(selection_func=tournament)
        .crossover(combiner=crossover_pxst)
        .mutate(mutate_function=replace_random, probability=0.3)
        .mutate(mutate_function=prim_mutation, probability=0.3)
        .mutate(mutate_function=pruner, probability=1.0)
        .callback(update_generation)
        .callback(display, every=50))

    for _ in range(5):
        population = population.evolve(pipe1, n=10)
        population.evaluate()
        best_so_far = population.documented_best
        intended_size = population.intended_size
        population.individuals.append(best_so_far)
        population.individuals = sorted(population.individuals, key=attrgetter("cost"))[:intended_size]

        population = population.evolve(pipe2, n=10)
        population.evaluate()
        best_so_far = population.documented_best
        intended_size = population.intended_size
        population.individuals.append(best_so_far)
        population.individuals = sorted(population.individuals, key=attrgetter("cost"))[:intended_size]


    tracker.log_simulation(params, stpg, population)

    best_overall = population.documented_best
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
        'n_iterations'        : 10,
        'stagnation_interval' : 100,
    }

    for dataset, value in STEIN_C:
        parameters['dataset'] = dataset
        parameters['global_optimum'] = value
        for i in range(30):
            parameters['runtrial'] = i + 1
            experiment("S12_hybrid_swap", parameters)