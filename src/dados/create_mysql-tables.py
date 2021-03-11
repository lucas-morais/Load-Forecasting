import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine



## Acessando Banco de Dados

#Variáveis de Ambiente
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Diretório Local dos Dados
dados_path = os.environ.get("DADOS_PATH")

# 1.Separando tabelas de dados e informação

info = []
dados = []

for filename in os.listdir(dados_path):
    if filename.startswith("coordenadas"):
        info.append(filename)
    else:
        dados.append(filename)

# 2. Criando Tabela de infos

#String de conexão com MySQL
database_con_string = os.environ.get("CONEXAO")

#Conexão 
engine = create_engine(database_con_string)

fl = dados_path+info[0]
print(fl)
df_info = pd.read_excel(fl, engine="openpyxl")
df_info = df_info.dropna(axis=0, how="all")
print(df_info)



df_info.to_sql("Info", engine, if_exists='replace')
print("Tabela Info adicionada ao BD Subestações")


# 3. Criando Tabelas com Dados

for nome in dados:
    fl = dados_path+nome
    
    df = pd.read_excel(fl, engine="openpyxl")
    #Transforma variáveis no tipo datetime
    df['data'] = pd.to_datetime(df[['DIA','MES','ANO','HORA','MINUTO']]
                            .astype(str).apply(' '.join, 1), format='%d %m %Y %H %M')
    df.set_index('data', inplace=True)
    df.drop(columns=['DIA','MES','ANO','HORA','MINUTO'], axis=1, inplace=True)
    print(df)
    
    temp = nome.rstrip('.xlsx')
    df.to_sql(temp, engine, if_exists = 'replace')
    print("Tabela",temp, "adicionada ao BD Subestações")
        
