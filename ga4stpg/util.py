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

STEIN_D = [
    ("steind1.txt", 106),
    ("steind2.txt", 220),
    ("steind3.txt", 1565),
    ("steind4.txt", 1935),
    ("steind5.txt", 3250),
    ("steind6.txt", 67),
    ("steind7.txt", 103),
    ("steind8.txt", 1072),
    ("steind9.txt", 1448),
    ("steind10.txt", 2110),
    ("steind11.txt", 29),
    ("steind12.txt", 42),
    ("steind13.txt", 500),
    ("steind14.txt", 667),
    ("steind15.txt", 1116),
    ("steind16.txt", 13),
    ("steind17.txt", 23),
    ("steind18.txt", 223),
    ("steind19.txt", 310),
    ("steind20.txt", 537),
]


STEIN_E = [
    ("steine1.txt", 111),
    ("steine2.txt", 214),
    ("steine3.txt", 4013),
    ("steine4.txt", 5101),
    ("steine5.txt", 8128),
    ("steine6.txt", 73),
    ("steine7.txt", 145),
    ("steine8.txt", 2640),
    ("steine9.txt", 3604),
    ("steine10.txt", 5600),
    ("steine11.txt", 34),
    ("steine12.txt", 67),
    ("steine13.txt", 1280),
    ("steine14.txt", 1732),
    ("steine15.txt", 2784),
    ("steine16.txt", 15),
    ("steine17.txt", 25),
    ("steine18.txt", 564),
    ("steine19.txt", 758),
    ("steine20.txt", 1342),
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
