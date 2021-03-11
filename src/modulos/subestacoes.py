import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from statsmodels.tsa.seasonal import seasonal_decompose

def string_conexao():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    # String de conexão 
    conexao = os.environ.get("CONEXAO")

    return conexao



class BancoDeDados(ABC):
    def __init__(self, con_string):
        self._engine = create_engine(con_string, convert_unicode=True)
    
    
    def get_engine(self):
        self._engine

    #@abstractmethod
    #def query_sql(self, query):
    #    pass
    


class Info (BancoDeDados):
    def __init__(self, con_string):
        super().__init__(con_string)
 
    def get_tabela_info(self):
    
        info = {}
    
        with self._engine.connect() as connection:
            result = connection.execute("select * from Info")
        
            for row in result:
                sigla = row['SIGLA']

                info [sigla] =  {
                    'nome':row['NOME'].strip(),
                    'latitude':row['LAT'],
                    'longitude':row['LONG']
                }   
            
        return info



class Subestacao(BancoDeDados):
    def __init__(self, sigla, nome, con_string):
        super().__init__(con_string)
        self._sigla = sigla
        self._nome = nome
        self._tabela = None
    
    
    @property
    def sigla(self):
        return self._sigla
    
    @property
    def nome(self):
        return self._nome
    
    def get_pontos_de_medicao(self):
        pontos_de_medicao =[]

        with self._engine.connect() as connection:
            query = f'show columns from {self._sigla} where Field!="data"'
            result = connection.execute(query)
            for row in result:
                pontos_de_medicao.append(row["Field"])
        
        return pontos_de_medicao

    def get_tabela(self, con_string):
        query = f"SELECT * FROM {self._sigla};" 
        self._tabela = pd.read_sql(query, con_string)
        return self._tabela



class PontoDeMedicao(BancoDeDados):
    def __init__(self, sigla, ponto_medicao, con_string):
        super().__init__(con_string)
        self._ponto_medicao = ponto_medicao
        self._sigla = sigla
        self._serie = None
    
    
    @property
    def ponto_medicao(self):
        return self._ponto_medicao 

    @property
    def serie(self):
        return self._serie
    
    def get_dados(self, data_inicio, data_fim):
        data = []
        potencia = []
        temp = 4*24*4   
        with self._engine.connect() as connection:
            query = f"""select data, {self._ponto_medicao} 
            from {self._sigla} 
            where Date(data) between '{data_inicio}' and '{data_fim}'
            """
            result = connection.execute(query)
            for row in result:
                data.append(row['data'])
                potencia.append(row[self._ponto_medicao])
       
        self._serie = pd.Series(potencia, index=data, name = "potencia" )
        self._serie.index.name = "data"
       

    def plota_serie(self):
        fig = go.Figure([
            go.Scatter(
                x=self._serie.index, 
                y=self._serie.values
            )
        ])
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 
        return fig_json

        
    def plota_perfil(self):
        fig = go.Figure()
        
        for mes in set(self._serie.index.month.values): 
            
            perfil = self._serie[self._serie.index.month==mes].resample('d').mean()
        
            fig.add_trace(go.Scatter(x=perfil.index.day, y=perfil.values))
        
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 
        return fig_json

    def plota_box(self):
        
        fig = go.Figure()
        
        for mes in set(self._serie.index.month.values): 
            
            dados = self._serie[self._serie.index.month==mes]
        
            fig.add_trace(go.Box(y=dados.values))
        
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 
        return fig_json

    
    def plot_decomposicao(self):
        decom = seasonal_decompose(self._serie, model='aditive', period=4*24*7, extrapolate_trend='freq')
        fig = make_subplots(
            rows=3, cols=1,
            specs=[
                [{"type": "scatter"}], 
                [{"type": "scatter"}],
                [{"type": "scatter"}]
            ])
        fig.add_trace(
            go.Scatter(go.Scatter(x=decom.seasonal.index, y=decom.seasonal.values)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(go.Scatter(x=decom.trend.index, y=decom.trend.values)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(go.Scatter(x=decom.resid.index, y=decom.resid.values)),
            row=3, col=1
        )
        
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 
        return fig_json
    
    def get_resumo(self):
        
        resumo = {
            'Média': self._dados.mean(),
            'Desvio Padrão': self._dados.std(),
            'Mediana': self._dados.median(),
            'Valor Máximo': self._dados.max(),
            'Valor Mínimo': self._dados.min(),
            'Valores Inválidos': None 
        }
        return resumo
         

    
    
    