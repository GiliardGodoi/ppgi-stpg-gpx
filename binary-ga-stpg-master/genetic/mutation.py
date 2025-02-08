import random
from genetic.chromosome import BinaryChromosome

def mutation_flipbit(chromosome):
    '''Flip exactly one bit from the chromosome genes'''

    flipbit = lambda x : '1' if x == '0' else '0'

    index = random.randrange(0, len(chromosome.genes))
    genes = chromosome.genes
    genes = genes[:index] + flipbit(genes[index]) + genes[(index + 1):]

    return BinaryChromosome(genes)