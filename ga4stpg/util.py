import functools
import pickle
import os

STEIN_B = [
    ("steinb1.txt",   82), # 0
    ("steinb2.txt",   83),
    ("steinb3.txt",  138),
    ("steinb4.txt",   59),
    ("steinb5.txt",   61), # 4
    ("steinb6.txt",  122),
    ("steinb7.txt",  111),
    ("steinb8.txt",  104),
    ("steinb9.txt",  220), # 8
    ("steinb10.txt",  86),
    ("steinb11.txt",  88),
    ("steinb12.txt", 174),
    ("steinb13.txt", 165), # 12
    ("steinb14.txt", 235),
    ("steinb15.txt", 318), # 14
    ("steinb16.txt", 127), # 15
    ("steinb17.txt", 131), # 16
    ("steinb18.txt", 218), # 17
]

STEIN_C = [
    ("steinc1.txt", 85),
    ("steinc2.txt", 144),
    ("steinc3.txt", 754),
    ("steinc4.txt", 1079),
    ("steinc5.txt", 1579),
    ("steinc6.txt", 55),
    ("steinc7.txt", 102),
    ("steinc8.txt", 509),
    ("steinc9.txt", 707),
    ("steinc10.txt", 1093),
    ("steinc11.txt", 32),
    ("steinc12.txt", 46),
    ("steinc13.txt", 258),
    ("steinc14.txt", 323),
    ("steinc15.txt", 556),
    ("steinc16.txt", 11),
    ("steinc17.txt", 18),
    ("steinc18.txt", 113),
    ("steinc19.txt", 146),
    ("steinc20.txt", 267),
]

def display(population):
    size = len(population)
    msg = f"Population {population.id} | size {size} | generation {population.generation} | best cost {population.documented_best.cost}"
    print(msg)

def update_best(population):
    population._update_documented_best()

def update_generation(population):
    population.generation += 1

def record_parents(crossover):

    filename = os.path.join("log", "individuals.pickle")

    @functools.wraps(crossover)
    def wrapper(*args):

        _ , parent_a, parent_b = args
        # print(self.STPG.name)

        child = crossover(*args)

        with open(filename, "ab") as file:
            pickle.dump([
                parent_a.edges,
                parent_b.edges,
                child.edges
                ], file)

        return child

    return wrapper
