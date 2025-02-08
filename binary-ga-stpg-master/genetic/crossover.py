import random
from genetic.chromosome import BinaryChromosome

def crossover_2points(A_parent, B_parent):
    length = len(A_parent.genes)
    points = random.sample(range(0, length), k=2)
    points.sort()
    p1, p2 = points

    crossing = lambda genex, geney : genex[:p1] + geney[p1:p2] + genex[p2:]

    offspring_A = BinaryChromosome(crossing(A_parent.genes, B_parent.genes))
    offspring_B = BinaryChromosome(crossing(B_parent.genes, A_parent.genes))

    return offspring_A, offspring_B


def crossover_1points(A_parent, B_parent):
    length = len(A_parent.genes)
    point = random.choice(range(0,length))

    crossing = lambda genex, geney : genex[:point] + geney[point:]

    offspring_A = BinaryChromosome(crossing(A_parent.genes, B_parent.genes))
    offspring_B = BinaryChromosome(crossing(B_parent.genes, A_parent.genes))

    return offspring_A, offspring_B