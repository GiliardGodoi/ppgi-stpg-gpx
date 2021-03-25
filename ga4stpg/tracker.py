import csv
import json
import os
import logging
from collections import defaultdict
from statistics import pvariance, mean as fmean

def handle_default(obj):
    if isinstance(obj, set):
        return list(obj)
    print(f"Object of type {type(obj)} is not JSON serializable")
    return ""

class DataLogger:
    '''Simple class to collect and store data from the simulations.

    Notes:
    1. Guarda os dados solicitados em memória e
    depois persiste em um arquivo do tipo especificado.
    Não faz o gerenciamento da quantidade de registros em memória.

    A intenção é reutilizar esse código nos demais módulos de simulações.

    Forma de utilização.

    1. Registrar os dados que serão capturados com register:
        - o parâmetro key em register identifica a informação que estamos capturando.
        Também será usado como base para o nome do arquivo.
        - filetype indica indica o tipo de arquivo a ser gerado: csv ou json
        - Se o arquivo especificado é csv, é necessário registrar a os campos dos dados.
        Será calculado um campo size com o tamanho da lista de cabeçalhos passados.
        Esse campo será utilizado para determinar se recebemos a mesma quantidade de registro futuramente.
        Entretanto não fazemos a verificação da correspondência dos campos.

    2. A captura de dados é feita pela função log(key, *args, **kargs).
    Os possíveis usos são:
        Para filetype == csv
        - log(key, x_1, x_2, ..., x_n) -> se o tipo de arquivo associado a key for csv,
        os dados serão apensados a uma lista

        Para filetype == json
        - log(key, dict_obj) -> se o tipo de arquivo associado a key for json,
        Então o objeto dict_obj será apensado a uma lista e ira ser persistido em um arquivo json.
        Útil para gravar um dicionário das arestas de um grafo.
        - log(key, dict_1, dict_2, ..., dict_n) log também pode receber diversos dict dentro de args.
        Entretanto se um dos elementos de args não for um dict irá gerar uma exceção.
        - log(key, fied1='value', ..., fieldn='value') -> log também irá trabalhar 'com keywords arguments'
        e irá registrar kwargs como um dicionário.
    '''

    def __init__(self, prefix='', outputfolder='out', defaults=False):

        self.storage = dict()
        self.mainfolder = outputfolder
        self.prefix = prefix

        if defaults:
            self.set_defaults_headers()

    def set_defaults_headers(self):
        raise NotImplementedError()

    def register(self, key, filetype, *args):
        if not key:
            raise ValueError(f"Key not provided: {key!r}")
        if not filetype:
            raise ValueError("filetype not provided")
        if filetype not in ['csv', 'json'] :
            raise ValueError("filetype must be csv or json")
        if key in self.storage:
            raise ValueError(f"Key <{key}> already exists")

        self.storage[key] = {"filetype": filetype , 'data' : list() }

        if (filetype == 'csv') and args and all(isinstance(item, str ) for item in args):
            self.storage[key]['data'].append(args)
            self.storage[key]['size'] = len(args)
        elif filetype == 'json' :
            pass
        else:
            raise TypeError("Header not provided or bad formated for csv file type")

    def log(self, key, *args, **kwargs):
        if not key:
            raise TypeError("Key not provided")
        if key not in self.storage:
            raise KeyError(f"There is no key <{key}> registered")

        if self.storage[key]['filetype'] == 'csv':
            if len(args) == self.storage[key]['size']:
                self.storage[key]['data'].append(args)
            else:
                raise ValueError("args bad formated")

        elif self.storage[key]['filetype'] == 'json':
            if len(args) == 1 and isinstance(args[0], dict):
                self.storage[key]['data'].append(args[0])
            if len(args) > 1:
                for item in args:
                    if isinstance(item, dict):
                        self.storage[key]['data'].append(item)
                    else:
                        raise TypeError("Item is not dict like object")
            elif kwargs:
                self.storage[key]['data'].append(kwargs)
        else:
            pass

    def report(self):

        if not os.path.exists(self.mainfolder):
            os.makedirs(self.mainfolder)

        prefix = f'{self.prefix}_' if self.prefix else ''
        mainfolder = self.mainfolder if self.mainfolder else '.'

        for key, content in self.storage.items():
            filename = os.path.join(mainfolder, f'{prefix}{key}')
            if content["filetype"] == 'csv':
                self.__write_csv__(filename, content["data"])
            elif content["filetype"] == 'json':
                self.__write_json__(filename, content["data"])

    def __write_csv__(self, filename, data, mode='w'):

        if mode not in ['w', 'a', 'x']:
            raise TypeError("Mode must be 'w', 'a' or 'x' ")

        filename = self.__enforce_extension__(filename, enforce_extension='.csv')

        try:
            with open(filename, mode, newline='') as file :
                writer = csv.writer(file)
                writer.writerows(data)
        except Exception as msg:
            print(msg)
            return False

        return True

    def __write_json__(self, filename, data, mode='w'):

        if mode not in ['w', 'a', 'x']:
            raise TypeError("Mode must be w or w+")

        if not isinstance(data, (dict, list)):
            raise TypeError("Data must be a list or dictionary")

        filename = self.__enforce_extension__(filename, enforce_extension='.json')

        try:
            with open(filename, mode) as file :
                json.dump(data, fp=file, indent=2, default=handle_default)
        except Exception as msg:
            print(msg)
            return False

        return True

    def __enforce_extension__(self, filename, enforce_extension='.txt'):
        #enforces the extension
        if not filename.endswith(enforce_extension):
            if '.' in filename:
                extension = filename[filename.rfind('.'):]
                filename = filename.replace(extension, enforce_extension)
            else:
                filename += enforce_extension

        return filename


class DataTracker(DataLogger):

    def __init__(self, runtrial, target='outputdata'):
        super().__init__(prefix=f"trial_{runtrial}", outputfolder=target, defaults=True)

    def set_defaults_headers(self):
        self.register("simulation", "csv",
                    "nro_trial",
                    "instance_problem",
                    "nro_nodes",
                    "nro_edges",
                    "nro_terminals",
                    "global_optimum",
                    "tx_mutation",
                    "population_size",
                    "max_generation",
                    "best_cost",
                    "best_fitness",
                    "iterations",
                    "run_time",
                    "max_last_improvement",
                    "stopped_by")

        self.register("evaluation", 'csv',
            "generation",
            "pop_mean_cost",
            "pop_var_cost",
            "pop_mean_fitness",
            "pop_var_fitness",
            "pop_penalizations",
            "pop_mean_partition",
            "pop_var_partition",
            "currentbest_cost",
            "currentbest_fitness",
            "bestdocumented_cost",
            "bestdocumented_fitness",
            "bestdocumented_last_improvement")

        self.register("bestindividual", "json")
        self.register("is_steiner_tree", "csv",
                "test",
                'has_cycle',
                'all_terminals_in',
                'all_leaves_are_terminals',
                'all_edges_are_reliable',
                'graph_is_connected')

    def log_evaluation(self, population : 'Population', **kwargs):

        count_penalization = 0
        partitions = list()
        fitnesses = list()
        costs = list()

        generation = population.generation

        for individual in population:
            qtd = individual.qtd_partitions
            if qtd > 1:
                count_penalization += 1
            partitions.append(qtd)
            fitnesses.append(individual.fitness)
            costs.append(individual.cost)

        currentbest = population.current_best
        bestoverall = population.documented_best

        self.log("evaluation",
                 generation,
                 fmean(costs),
                 pvariance(costs),
                 fmean(fitnesses),
                 pvariance(fitnesses),
                 count_penalization,
                 fmean(partitions),
                 pvariance(partitions),
                 currentbest.cost,
                 currentbest.fitness,
                 bestoverall.cost,
                 bestoverall.fitness,
                 bestoverall.last_improvement
                )

    def log_simulation(self,
                        params : 'SimulationParams',
                        STPG : 'SteinerTreeProblem',
                        POPULATION : 'Population'):

        bestchromosome = POPULATION.documented_best

        self.log("simulation",
            params["runtrial"],
            STPG.name,                         # instance problem info >>
            STPG.nro_nodes,
            STPG.nro_edges,
            STPG.nro_terminals,
            params["global_optimum"],          # simulation params >>
            params["tx_mutation"],
            POPULATION.intended_size,
            params["n_iterations"],
            bestchromosome.cost,               # results >>
            bestchromosome.fitness,
            POPULATION.generation,
            POPULATION.runtime,
            bestchromosome.last_improvement,
            POPULATION.stoppedby
        )

    def log_bestIndividual(self, individual, test, complete_test):

        self.log("bestindividual", individual.chromosome.edges)
        self.log("is_steiner_tree",
                    test,
                    complete_test["has_cycle"],
                    complete_test["all_terminals_in"],
                    complete_test["all_leaves_are_terminals"],
                    complete_test["all_edges_are_reliable"],
                    complete_test["graph_is_connected"])
