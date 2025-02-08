import csv
import json
import os
from collections import defaultdict


class BaseLogger():
    '''Default logger. It doesn't do anything. It's just for prevent errors.
    Based in idea from Design Partterns Null Object.
    '''

    def __init__(self, prefix='', outputfolder='outputdata'):
        pass

    def register(self, key, filetype, *args):
        pass

    def log(self, key, *args):
        pass

    def report(self):
        pass

class DataLogger(BaseLogger):
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

    def __init__(self, prefix='', outputfolder='out'):

        self.storage = dict()
        self.mainfolder = outputfolder
        self.prefix = prefix

    def register(self, key, filetype, *args):
        if not key:
            raise ValueError(f"Key not provided: {key!r}")
        if not filetype:
            raise ValueError("filetype not provided")
        if filetype not in ['csv', 'json'] :
            raise ValueError("filetype must be csv or json")

        self.storage[key] = {"filetype": filetype , 'data' : list() }

        if (filetype == 'csv') and args and all(isinstance(item, str ) for item in args):
            self.storage[key]['data'].append(args)
            self.storage[key]['size'] = len(args)
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

        if not isinstance(data, dict):
            print("")

        filename = self.__enforce_extension__(filename, enforce_extension='.json')

        try:
            with open(filename, mode) as file :
                json.dump(data, fp=file, indent=4)
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


if __name__ == "__main__":
    from tqdm import tqdm
    import random


    logger = DataLogger(outputfolder=None)
    logger.register("teste",'i', 'int', 'measure', 'category', 'temp')

    for i in tqdm(range(100000)):
        logger.log("teste", i, random.randint(50,1000), random.random() * 100, random.choice(['A', 'B', 'C']), random.random() * 100)


    logger.report()
