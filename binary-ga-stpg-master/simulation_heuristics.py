import csv
from os import path

from graph import Graph, ReaderORLibrary
from graph.steiner import (prunning_mst, shortest_path,
                            shortest_path_origin_prim,
                            shortest_path_with_origin)

problems_class = {
        'b' : {'max' : 18},
        'c' : {'max' : 20},
        'd' : {'max' : 20},
        'e' : {'max' : 20},
        'others' : ['dv80.txt', 'dv160.txt', 'dv320.txt']
    }

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

def generate_file_names(key = None):

    if isinstance(problems_class[key], list) :
        for item in problems_class[key]:
            yield item

    elif isinstance(problems_class[key], dict) :
        counter = 1
        MAX = problems_class[key]['max']
        while counter <= MAX :
            yield f"stein{key}{counter}.txt"
            counter += 1

if __name__ == "__main__":

    # Coletar dados da:
    INSTANCE_DATA = list() # instância do problema
    HEURISTIC_RESULTS = list() # resultado obtido

    OUTPUT_DATA = path.join("output_data", "heuristics")
    INPUT_DATA = path.join("datasets", "ORLibrary")

    READER = ReaderORLibrary()

    for item in heuristics:
        heuristic = item['function']
        nickname = item['nickname']

        for filename in generate_file_names('c'):
            print("Processing... ", filename, end="\r")
            ff = path.join(INPUT_DATA, filename)
            stp = READER.parser(ff)
            terminals = set(stp.terminals)

            graph = Graph(edges=stp.graph)

            # stp_data = [
            #     stp.name,
            #     stp.nro_nodes,
            #     stp.nro_edges,
            #     stp.nro_terminals
            # ]

            # INSTANCE_DATA.append(stp_data)

            HEURISTIC_RESULTS = list()

            for node in graph.vertices:
                _, cost = heuristic(graph, node, stp.terminals)
                is_terminal = node in terminals

                data = [node, is_terminal, nickname, cost]
                HEURISTIC_RESULTS.append(data)

            output_file = filename[:-4] # retira a extensão .txt
            with open(path.join(OUTPUT_DATA, f'{nickname}_{output_file}.csv'), 'w' , newline='') as ff:
                writer = csv.writer(ff, delimiter=',')
                writer.writerow(["Node", "Is terminal","Heuristic", "Cost"])
                writer.writerows(HEURISTIC_RESULTS)

    # with open(path.join(OUTPUT_DATA, f'instance_problem.csv'), 'w' , newline='') as ff:
    #         writer = csv.writer(ff, delimiter=',')
    #         writer.writerow(["Problem", "Vertices", "Edges", "Terminals"])
    #         writer.writerows(INSTANCE_DATA)
