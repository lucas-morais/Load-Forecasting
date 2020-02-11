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

def count_missing(df, col):
    count = 0
    for index, row in df.iterrows():
        if(row == np.nan):
            count = count+1
        else:
            count = 0;    

class missingAnalysis:

    def __init__(self, df):
        self.df = df 
    
    def gaps(self, cols):
        for nome in cols:
            print(nome,':',self.df[nome].isna().sum())
            print(self.df[nome][(self.df[nome].isnull()) & (self.df[nome].shift().isnull())])
        print("OK")



class subes:

    def __init__(self, nome):
        temp = nome.rstrip('.xlsx')
        
        con = connect_bd()
        con.begin()
        info = con.execute('SELECT Nome, Latitude, Longitude FROM Info WHERE Abrv = "{}"'.format(temp))
        
        self.nome, self.latitude, self.longitude = list(info)[0]
     
        self.df = pd.read_sql_table(nome, con)

        self.cols = self.df.columns.values

    def desc(self):
        print("Nome:", self.nome)
        print("Latitude:", self.latitude)
        print("Longitude:", self.longitude)  
    
    def resumo(self):
        print(self.df.info())

    def missing(self):
        self.df.replace(0,np.nan, inplace = True)

    
def main():
    print("Teste Classe:")
    jps = subes ('JPS')
    jps.missing()
    jps.desc()
    #print(jps.cols)
    
    #miss = missingAnalysis(jps.df)
    #miss.gaps(jps.cols[1:2])
    count_missing(jps.df, jps.cols[1:2])
if __name__ == "__main__":
    main() 

