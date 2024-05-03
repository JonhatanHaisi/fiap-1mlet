from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pathlib import Path
from models.entities import Base, User, Produto, Producao

import pandas as pd
import shutil
import requests
import hashlib

#==============================================================================
# Cria o banco de dados SQLite:
engine = create_engine('sqlite:///database.db', echo=False)
session = Session(engine)
Base.metadata.create_all(engine)

# Cria o diretório temp para armazenar os arquivos baixados:
Path('temp').mkdir(exist_ok=True)

#==============================================================================
# UTILS
#==============================================================================
def importar_csv(url):
    nome_arquivo = url.split('/')[-1]
    with open(f'temp/{nome_arquivo}', 'wb') as file:
        file.write(requests.get(url).content)


#==============================================================================
# USERS
#==============================================================================
if session.query(User).count() == 0:
    users = (
        User(username='1mlet', password=hashlib.md5('1mlet@28'.encode()).hexdigest()),
    )
    session.add_all(users)
    session.commit()

#==============================================================================
# PRODUÇÃO
#==============================================================================

# Baixando os dados de produção do site da Embrapa:
importar_csv('http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv')
producao = pd.read_csv('temp/Producao.csv', sep=';')

# Salvando no banco de dados todos os produtos que ainda não foram importados:
total_importados = 0
for index, linha in producao.iterrows():
    # se o produto ainda não foi importado, salva no banco de dados
    if session.query(Produto).where(Produto.id == linha['id']).first() is None:
        produto = Produto(id=linha['id'], nome=linha['produto']) # cria um objeto Produto
        session.add(produto) # adiciona o objeto ao banco de dados
        total_importados += 1 # incrementa o contador de produtos importados
session.commit() # salva as alterações no banco de dados
print(f'Produtos importados: {total_importados}')

# Alterando a estrutura dos dados do dataframe para facilitar a importação de dados de produção
producao.set_index('id', inplace=True) # id do produto passa a ser o índice
producao.drop(columns='produto', inplace=True) # a coluna com o nome do produto é removida
producao = producao.melt(var_name='ano', value_name='quantidade', ignore_index=False) # ver explicação a seguir

# o método melt() transforma as colunas do dataframe em linhas, mantendo o índice original
# Por exemplo:
# Antes:
# | id | 2000 | 2001 | 2002 |
# |----|------|------|------|
# | 1  | 100  | 200  | 300  |
# | 2  | 150  | 250  | 350  |
#
# Depois:
# | id | ano  | quantidade |
# |----|------|------------|
# | 1  | 2000 | 100        |
# | 1  | 2001 | 200        |
# | 1  | 2002 | 300        |
# | 2  | 2000 | 150        |
# | 2  | 2001 | 250        |
# | 2  | 2002 | 350        |

# Salvando no banco de dados todos os dados de produção que ainda não foram importados:
total_importados = 0
for index, linha in producao.iterrows():
    # se a produção do produto para o ano ainda não foi importada, salva no banco de dados
    if session.query(Producao).where(Producao.produto_id == index, Producao.ano == linha['ano']).first() is None:
        producao = Producao(ano=linha['ano'], quantidade=linha['quantidade'], produto_id=index) # cria um objeto Producao
        session.add(producao) # adiciona o objeto ao banco de dados
        total_importados += 1 # incrementa o contador de dados de produção importados
session.commit() # salva as alterações no banco de dados
print(f'Dados de produção importados: {total_importados}')

#==============================================================================
# PROCESSAMENTO
#==============================================================================
# ....


#==============================================================================
# COMERCIALIZAÇÃO	
#==============================================================================
# ....


#==============================================================================
# IMPORTAÇÃO
#==============================================================================
# ....


#==============================================================================
# EXPORTAÇÃO
#==============================================================================
# ....


#==============================================================================
# FINALIZAÇÃO DO SCRIPT
#==============================================================================

# Exclui o diretório temp e todos os arquivos dentro dele:
shutil.rmtree('temp')

# Fecha a conexão com o banco de dados:
session.close()
engine.dispose()

