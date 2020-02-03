import numpy as np
import pandas as pd
import sqlalchemy as bd
from dotenv import load_dotenv, find_dotenv
import os

def connect_bd():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    #String de conexão com MySQL
    database_con_string = os.environ.get("DATABASE_CON")
    
    #Conexão
    engine = bd.create_engine(database_con_string)
    return engine



class subes:

    def __init__(self, nome):
        temp = nome.rstrip('.xlsx')
        
        con = connect_bd()
        con.begin()
        info = con.execute('SELECT Nome, Latitude, Longitude FROM Info WHERE Abrv = "{}"'.format(temp))
        
        self.nome, self.latitude, self.longitude = list(info)[0]
     
        self.df = pd.read_sql_table(nome, con)
    
    def desc(self):
        print("Nome:", self.nome)
        print("Latitude:", self.latitude)
        print("Longitude:", self.longitude)  
    
    def resumo(self):
        print(self.df.info())
  
  
def main():
    print("Teste Classe:")
    abr = subes ('JPS.xlsx')
    abr.desc()
    #print(abr.nome)
    #abr.resumo()

if __name__ == "__main__":
    main() 

