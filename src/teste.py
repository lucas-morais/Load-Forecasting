# import os
# from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, MetaData, Table

import modulos.banco_de_dados as bd 
from modulos.plots import mapa
from modulos.subestacoes import Subestacao, Info ,string_conexao, PontoDeMedicao
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import matplotlib.pyplot as plt





if __name__=="__main__":

    
    con = string_conexao()
    info = Info(con)
    tabela_info = info.get_tabela_info()
    subes = Subestacao('JPS', tabela_info['JPS'].get("nome"), con)
    jps = subes.get_tabela(con)
    # print(jps.head())

    # print(jps.describe())
    nomes = [col.rstrip("JPS_TIPO_") for col in jps.columns[1:]]
    print(nomes)
    #jps.boxplot()
    #plt.show()
    # subes = Subestacao('JPS', tabela_info['JPS'].get("nome"), con)
    # barras = subes.get_pontos_de_medicao()
    
    # ponto = PontoDeMedicao('JPS', barras[0], con)

    # ponto.get_dados("2008-08-12", "2009-08-12")
    # print(ponto.serie.tail())
    
   # %%
    