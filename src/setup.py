import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


def checa_env():
    path_env = find_dotenv()
    if (path_env == ""):
       cria_variaveis(".env")
    else:
        print(f"Variáveis de Ambiente no caminho: {path_env}")
        checa_variaveis(path_env)

def cria_variaveis(path_env):
    print(f"\n\nDigite sua string de conexão:")
    con = input()
    with open(path_env, "w") as f:
        f.write(f"CONEXAO = {con}") 
        

def checa_variaveis(path_env):
    load_dotenv(path_env)
    conexao = os.environ.get("CONEXAO")
    if (conexao is None):
        print("String de conexão não encontrada")
        print("Você pode fornecer a string de conexão com o banco de dados pelo console ",
            "ou criar um arquivo .env com a variável CONEXAO")
        print("Forncer string de conexão pelo console? s/n")
        resposta = input()
        if resposta == 's':
            cria_variaveis(path_env)
        elif resposta == 'n':
            pass
        else:
            checa_variaveis(path_env)
    else:
        print(f"String de conexão: {conexao}")   


if __name__=="__main__":
    checa_env()