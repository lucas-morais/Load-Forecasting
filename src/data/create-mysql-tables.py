import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine



## Acessando Banco de Dados

#Variáveis de Ambiente
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#String de conexão com MySQL
database_con_string = os.environ.get("DATABASE_CON")

#Conexão 
engine = create_engine(database_con_string, echo=True)




