import numpy as np
import pandas as pd
import sqlalchemy as bd
from dotenv import load_dotenv, find_dotenv
import os
import matplotlib.pyplot as plt
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
    missing = []
    
    for index, row in df.iterrows():
        ind = 0
        if pd.isnull(row[col]):
            
            count = count+1
            if count == 1:
                ind = index
                missing.append([ind,1])
            else:
                count = count + 1
                missing[-1][1] = count
        else:
           count = 0
        
    
    #for index, row in df.iterrows():
    #    print(index, pd.isnull(row[col]))
    #    count = count +1
    #    if count ==10:
    #        break
        
    
    return missing 






class subes:

    def __init__(self, nome):
        temp = nome.rstrip('.xlsx')
        
        con = connect_bd()
        con.begin()
        info = con.execute('SELECT Nome, Latitude, Longitude FROM Info WHERE Abrv = "{}"'.format(temp))
        
        self.nome, self.latitude, self.longitude = list(info)[0]
     
        self.df = pd.read_sql_table(nome, con)
        self.df.index = pd.DatetimeIndex(self.df.index)
        self.cols = self.df.columns.values

    def desc(self):
        print("Nome:", self.nome)
        print("Latitude:", self.latitude)
        print("Longitude:", self.longitude)  
    
    def resumo(self):
        print(self.df.info())

    def missing(self):
        self.df.replace(0,np.nan, inplace = True)

    

class missingAnalysis:

    def __init__(self, df):
        self.df = df
        self.gaps = {}
        self.imp=[] 
    
    def count_gaps(self, cols):
        self.gaps = {}
        for nome in cols:
            self.gaps[nome] = count_missing(self.df, nome)
            lista = self.gaps[nome].copy() 
            lista.sort(key = lambda x:x[1], reverse = True)
            print("Gaps em ordem decrescente:")
            print(lista[0:10])
        
        #return gaps

    def plot_missing(self ,col):
        
        m = self.gaps[col]
        plt.plot(self.df[col])
        for it in  m:
            plt.axvline(it[0], color = 'r', linewidth = 0.1)
        
        plt.ylabel("Potência")
        plt.xlabel("Data")
        plt.title("Dados Missing - {}".format(col))
        plt.show()

    def imputation(self, col, ini, fim,method = 'time'):
        
        mask = (self.df['data']>ini) & (self.df['data']<fim)
        self.imp = self.df[col][mask]
        self.imp = self.imp.interpolate(method = method)



def main():
    print("Teste Classe:")
    jps = subes ('JPS')
    jps.missing()
    jps.desc()
    #print(jps.cols[0])
    
    miss = missingAnalysis(jps.df)
    
    miss.count_gaps(jps.cols[1:3])
    #miss.plot_missing(jps.cols[1])
    
    miss.imputation(jps.cols[1], ini = '2009-12', fim = '2010-02')
    #print(miss.imp.columns.values())
    #l = miss.gaps[jps.cols[1]]
    #print(l[1:10])
    #for it in miss.gaps[jps.cols[1:2]].items():
    #    print(it)
if __name__ == "__main__":
    main() 

