import numpy as np
import pandas as pd
import sqlalchemy as sql
from dotenv import load_dotenv, find_dotenv
import os

def connect_bd():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    #String de conexão com MySQL
    database_con_string = os.environ.get("DATABASE_CON")
    
    #Conexão
    engine = sql.create_engine(database_con_string)
    return engine


    

#Diretório Local dos Dados
dados_path = os.environ.get("DADOS_PATH")
class subes:

    def __init__(self, nome):
        con = connect_bd()
        self.df = pd.read_sql_table(nome, con)
        
    
    def resumo(self):
        print(self.df.info())
  
  
def main():
    print("Teste Classe:")
    abr = subes ('ABR.xlsx')
    abr.resumo()

if __name__ == "__main__":
    main() 

