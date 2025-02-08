import random

def tournament_selection(population):
    selected = list()
    pool_size = len(population)
    count = 0

    while count < pool_size:
        c1, c2 = random.sample(population, k=2)
        if c1.fitness < c2.fitness:
            selected.append(c1)
        else:
            selected.append(c2)

        count += 1

    return selected


def roullete_selection(population, pool_size):
    # pool_size = len(population)
    fitnesses = [c.fitness for c in population if c.normalized]

    # Return a k sized list of population elements chosen with replacement
    selected = random.choices(population, weights=fitnesses, k=pool_size)

    return selected