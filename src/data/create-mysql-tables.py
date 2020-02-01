import pandas as pd


import sqlalchemy
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine

dotenv_path = find_dotenv()
print(dotenv_path)

load_dotenv(dotenv_path)
database_con_string = os.environ.get("DATBASE_USER")
print(database_con_string)
#engine = create_engine(database_con_string, echo=True)
#print("Usuário:", database_user)
#print("Senha:", database_password)



