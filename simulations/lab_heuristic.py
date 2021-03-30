
from os import path
import csv

from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.steiner import (prunning_mst,
                                    shortest_path,
                                    shortest_path_origin_prim,
                                    shortest_path_with_origin)

output_folder = path.join("..", "data", "exp_heuristic")
instance_folder = path.join("..", "datasets", "ORLibrary")

instance_class = 'c'
instance_qtd = 18

instances = [f'stein{instance_class}{ii}.txt' for ii in range(1, instance_qtd+1)]

assert path.exists(instance_folder)
assert path.exists(output_folder)

heuristics = [
    {
        'function' : prunning_mst,
        'nickname' : "PMH"
    },
    {
        'function' : shortest_path,
        'nickname' : 'SPH'
    },
    {
        'function' : shortest_path_origin_prim,
        'nickname' : 'SPHPrim'
    },
    {
        'function' : shortest_path_with_origin,
        'nickname' : 'SPHO'
    }
]

reader = ReaderORLibrary()
results = list()
results.append(['instance_problem', 'heuristic', 'start_node', 'cost'])

for item in heuristics:
    heuristic = item['function']
    name_heuristic = item['nickname']

    for name in instances:
        STPG = reader.parser(path.join(instance_folder, name))
        graph = STPG.graph
        terminals = STPG.terminals.copy()
        vertices = list(graph.vertices)

        for v in vertices:
            print(f"{name_heuristic.upper()} -- {name.upper()} -- start node: {v}".ljust(100), end='\r')
            _, cost = heuristic(graph, v, terminals)
            results.append([name, name_heuristic, v, cost])
print(" "*100)
output_file = path.join(output_folder, "resultados3.csv")
with open(output_file, "w", newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(results)

print("FIM DO EXPERIMENTO")
print("- -"*10)