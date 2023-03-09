### Backtest module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-08

import pandas as pd
import warnings
import os




def import_data(data_name: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(f"./data/{data_name}.csv")    
    except: #file not found
        warnings.warn("File not found or incorrect path")
        return -1
        
    return data


def export_data(data: pd.core.series, data_name: str) -> None:
    pasta = './data'
    files = []

    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            files.append(arquivo)
            
    if f"{data_name}.csv" in files:
        data_saved = import_data(f"./data/{data_name}.csv")
        data_full = pd.concat([data_saved, data], axis=0)
        data_full.to_csv(path_or_buf=f"./data/{data_name}.csv", index=True)
    else:
        data.to_csv(path_or_buf=f"./data/{data_name}.csv", index=True)



