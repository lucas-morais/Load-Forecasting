Load-Forecasting
==============================

Projeto para previsão de carga utilizando dados de subestações da Paraíba

Organização do Projeto
------------

    ├── LICENSE
    ├── Makefile           <- Makefile com comandos: (vazio)
    ├── README.md          <- README com a hierarquia do prjeto.
    ├── dados
    │   ├── externos       <- Dados de fontes complementares. Ex.:Clima
    │   ├── interim        <- Dados intermidiários.
    │   ├── processados    <- Conjunto de Dados final. Pronto para ser submetido ao modelo
    │   └── brutos         <- Dados originais. Não transformados.
    │
    ├── docs               <-Documentação Gerada com Sphinx
    │
    ├── models             <- Modelos treinados e sumarizados
    │
    ├── notebooks          <- Jupyter notebooks. Notebooks com análises interativas e Demonstações Teóricas
    │                         
    ├── referencias        <- Dicionário de dados, referências bibliográficas e Bibliotecas.
    │
    ├── relatorios         <- Arquivos gerados com LaTex, Markdown e HTML
    │   └── figuras        <- Figuras geradas para o relatório
    │
    ├── requirementos.txt  <- Requrimentos para reprodução do prjeto.
    │                         
    ├── setup.py           <- Faz o projeto instalável
    ├── src                <- Source code para o prjeto.
    │   ├── __init__.py    <- Faz de src um módulo
    │   │
    │   ├── modulos        <- Biclioteca para manipulação de dados 
    │   │   ├── __init__.py
    │   │   └── tools.py 
    │   │     
    ├── dados              <- Script para a geração de Dados 
    │   │   └── create-mysql-db.py
    │   │
    │   ├── atributos      <- Script para transformar conjunto de dados em atributos para modelos
    │   │   └── eng-de-atributos.py
    │   │
    │   ├── modelos        <- Scripts para treinamento e predição 
    │   │   ├── modelo_predicao.py
    │   │   └── modelo_treino.py
    │   │
    │   └── visualizacao   <- Scripts para criação de visualizações explanatórias
    │       └── visualizar.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Projeto baseado em <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
