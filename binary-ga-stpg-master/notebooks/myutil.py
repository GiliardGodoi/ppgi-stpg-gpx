# -*- coding: utf-8 -*-
"""
Created on 25 03 2020

@author: Giliard Almeida de Godoi

Funções recorrentes para a leitura, tratamento e análise dos dados.
"""
import os
import pandas as pd
import numpy as np

problems_class = {
        'b' : {'max' : 18},
        'c' : {'max' : 20},
        'd' : {'max' : 20},
        'e' : {'max' : 20},
        'others' : ['dv80', 'dv160', 'dv320']
    }

def instance_problems_filenames(key, file_extension = "txt"):

    if isinstance(problems_class[key], list) :
        for item in problems_class[key]:
            yield item + file_extension

    elif isinstance(problems_class[key], dict) :
        counter = 1
        MAX = problems_class[key]['max']
        while counter <= MAX :
            yield f"stein{key}{counter}.{file_extension}"
            counter += 1

            
def read_simulation(simulationfolder, filetemplate, mintrial=1, maxtrial=30):
    
    MAIN_FOLDER = os.path.join("..", "outputdata", simulationfolder)
 
    # simulations: diretórios que contem os dados para cada um dos datasets.
    # ['B1', 'B2', 'B3' ... ]
    simulations = [os.path.join(MAIN_FOLDER, folder) 
                   for folder in os.listdir(MAIN_FOLDER) 
                       if os.path.isdir(os.path.join(MAIN_FOLDER, folder))
                  ]
  
    # filetemplate: INDICA QUAL DADOS ESTAMOS ANALISANDO.
    # Cada execução (trial) gera um arquivo diferente. 
    # files: é um array com o nome de todos os arquivos
    files = [filetemplate.format(i) for i in range(mintrial,maxtrial+1)]

    data_pieces = [ pd.read_csv(os.path.join(folder, file))
            for folder in simulations   
                for file in files       
    ]

    # concatena (junta) todos os DataFrames em um só
    return pd.concat(data_pieces, ignore_index=True)


def read_simulation_dataset(dataset, simulationfolder, filetemplate, mintrial=1, maxtrial=30):

    MAIN_FOLDER = os.path.join("..", "outputdata", simulationfolder, dataset)
    
    data_pieces = list()
    for trial in range(mintrial,maxtrial+1):
        file = filetemplate.format(trial)
        df = pd.read_csv(os.path.join(MAIN_FOLDER, file))
        df['trial'] = str(trial)
        data_pieces.append(df)
    
    return pd.concat(data_pieces)

