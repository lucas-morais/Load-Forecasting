import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, MetaData, Table
from modulos.subestacoes import Subestacao

def conexão():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    # String de conexão 
    string_conexao = os.environ.get("CONEXAO")

    engine = create_engine(string_conexao, convert_unicode=True)
    print("Conectado ao Banco de Dados")
    
    metadata = MetaData(bind=engine)
    for t in metadata.sorted_tables:
        print(t)    
    
    return engine

def get_tabela_info(engine):
    
    info = {}
    
    with engine.connect() as connection:
        result = connection.execute("select * from Info")
        
        for row in result:
            sigla = row['SIGLA']

            info [sigla] =  {
                    'nome':row['NOME'].strip(),
                    'latitude':row['LAT'],
                    'longitude':row['LONG']
            }   
            # info["Nome"].append(row["NOME"].strip())
            # info["Sigla"].append(row["SIGLA"])
            # info["Latitude"].append(row["LAT"])
            # info["Longitude"].append(row["LONG"])
    return info 

def get_pontos(tabela, engine):
    with engine.connect() as connection:
        pontos_de_medicao =[]
        query = f'show columns from {tabela} where Field!="data"'
        result = connection.execute(query)
        for row in result:
            pontos_de_medicao.append(row["Field"])
    return pontos_de_medicao
    