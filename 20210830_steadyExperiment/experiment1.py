
from os import path
from re import sub

from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.steiner import shortest_path_origin_prim
from ga4stpg.graph.util import is_steiner_tree
from ga4stpg.tree.evaluation import EvaluateTreeGraph
from ga4stpg.tree.generate import GenerateBasedRandomWalk
from ga4stpg.tree.mutate import PrimBasedMutation, Prunning
from ga4stpg.tree.mstcrossover import CrossoverRelativeGreedyPrim
from ga4stpg.tree.pxpartition import PartitionCrossoverSteinerTree
from ga4stpg.util import STEIN_B, STEIN_C


def experiment1(dataset, expected_value):

    filename = path.join('datasets', 'ORLibrary', dataset)
    stpg = ReaderORLibrary().parser(filename)

    crossover = PartitionCrossoverSteinerTree(stpg)

    generator = GenerateBasedRandomWalk(stpg)
    evaluator = EvaluateTreeGraph(stpg)
    pruner = Prunning(stpg)
    mst_transformation = PrimBasedMutation(stpg)

    best_ST = pruner(generator())

    best_cost, _ = evaluator(best_ST)

    i = 0
    MAX_ITER = 4_000
    # MAX_ITER = 100

    while (best_cost != expected_value) and i < MAX_ITER:
        i += 1
        ST = generator()
        ST = pruner(ST)
        red, blue = crossover(best_ST, ST)


        red_cost, _  = evaluator(red)
        blue_cost, _ = evaluator(blue)

        if red_cost < best_cost:
            best_ST   = red
            best_cost = red_cost

        if blue_cost < best_cost :
            best_ST = blue
            best_cost = blue_cost

        gray = mst_transformation(best_ST)
        gray_cost, _ = evaluator(gray)

        if gray_cost < best_cost:
            best_ST = gray
            best_cost = gray_cost

        # print(dataset, expected_value, i, best_cost, end='\r')
        print(dataset, expected_value, i, best_cost, red_cost, blue_cost, gray_cost, end='\r')
    print(dataset, expected_value, i, best_cost)


def experiment_2(dataset, expected_value):
    filename = path.join('datasets', 'ORLibrary', dataset)
    stpg = ReaderORLibrary().parser(filename)

    crossover = CrossoverRelativeGreedyPrim(stpg)

    generator = GenerateBasedRandomWalk(stpg)
    evaluator = EvaluateTreeGraph(stpg)
    pruner = Prunning(stpg)
    mst_transformation = PrimBasedMutation(stpg)

    best_ST = pruner(generator())

    best_cost, _ = evaluator(best_ST)

    i = 0
    MAX_ITER = 4_000
    # MAX_ITER = 100

    while (best_cost != expected_value) and i < MAX_ITER:
        i += 1
        ST = generator()
        ST = pruner(ST)

        red = crossover(best_ST, ST)

        red_cost, _  = evaluator(red)

        if red_cost < best_cost:
            best_ST   = red
            best_cost = red_cost

        gray = mst_transformation(best_ST)
        gray_cost, _ = evaluator(gray)

        if gray_cost < best_cost:
            best_ST = gray
            best_cost = gray_cost

        print(dataset, expected_value, i, best_cost, end='\r')
    print(dataset, expected_value, i, best_cost)


def experiment_3(dataset, expected_value):

    filename = path.join('datasets', 'ORLibrary', dataset)
    stpg = ReaderORLibrary().parser(filename)

    crossover = PartitionCrossoverSteinerTree(stpg)

    random_generator = GenerateBasedRandomWalk(stpg)
    def compound_generator():
        for v in range(1, stpg.nro_nodes):
            subtree, _ = shortest_path_origin_prim(stpg.graph, v, stpg.terminals)
            yield subtree
        while True:
            subtree = random_generator()
            yield subtree

    generator = compound_generator()

    evaluator = EvaluateTreeGraph(stpg)
    pruner = Prunning(stpg)
    mst_transformation = PrimBasedMutation(stpg)

    best_ST = pruner(next(generator))

    best_cost, _ = evaluator(best_ST)

    i = 0
    MAX_ITER = 4_000
    # MAX_ITER = 100

    while (best_cost != expected_value) and i < MAX_ITER:
        i += 1
        ST = next(generator)
        ST = pruner(ST)
        red, blue = crossover(best_ST, ST)


        red_cost, _  = evaluator(red)
        blue_cost, _ = evaluator(blue)

        if red_cost < best_cost:
            best_ST   = red
            best_cost = red_cost

        if blue_cost < best_cost :
            best_ST = blue
            best_cost = blue_cost

        gray = mst_transformation(best_ST)
        gray_cost, _ = evaluator(gray)

        if gray_cost < best_cost:
            best_ST = gray
            best_cost = gray_cost

        print(dataset, expected_value, i, best_cost, red_cost, blue_cost, gray_cost, end='\r')
    print(dataset, expected_value, i, best_cost)

if __name__ == "__main__":
    for dataset, value in STEIN_C[10:]:
        experiment1(dataset, value)
