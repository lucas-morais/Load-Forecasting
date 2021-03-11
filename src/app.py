from flask import Flask, render_template, request
from modulos.subestacoes import Info, Subestacao, PontoDeMedicao,string_conexao 

CON = string_conexao() 
INFO = Info(CON).get_tabela_info()

# Criando aplicação
app = Flask(__name__)

# Página principal
@app.route('/')
def pagina_principal():
    return render_template("index.html", subestacoes= INFO)

@app.route('/subestacao', methods=['POST'])
def pagina_subestacao():
    sigla = request.form["subestacao"]
    nome = INFO[sigla].get("nome")
    subes = Subestacao(sigla, INFO[sigla].get("nome"), CON) 
    pontos = subes.get_pontos_de_medicao()
    return render_template("subestacao.html", sigla=sigla, nome=nome, pontos=pontos)
    
@app.route('/ponto_medicao', methods = ['POST'])
def pagina_ponto_medicao():
    barra = request.form["barra"]
    data_inicio = request.form["data_inicio"]
    data_fim = request.form["data_fim"]
    sigla = request.form["sigla"]
    ponto_medicao = PontoDeMedicao(sigla, barra, CON)

    data, potencia = ponto_medicao.get_dados(data_inicio, data_fim)
    resumo = ponto_medicao.get_resumo()
    return render_template("ponto_medicao.html", resumo=resumo)
    

if __name__=='__main__':
    app.run(debug=True)
    