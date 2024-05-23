from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pathlib import Path
from models.entities import Base, User, Grupo, Produto, Producao, Comercializacao

import pandas as pd
import hashlib

#==============================================================================
# Cria o banco de dados SQLite:
engine = create_engine('sqlite:///database.db', echo=False)
session = Session(engine)
Base.metadata.create_all(engine)

#==============================================================================
# UTILS
#==============================================================================
def normalizar_columas(df: pd.DataFrame):
    '''
    Normaliza as colunas para ficar com letras minuscolas
    '''
    df.columns = df.columns.str.lower()
    return df

def obter_grupos_mapeados(): 
    return { grupo.nome:grupo.id for grupo in session.query(Grupo).all() }

def obter_produtos_mapeados():
    return { (produto.control, produto.grupo_id) : produto.id for produto in session.query(Produto).all() }

def preparar_dataset_grupo_produto(df:pd.DataFrame):
    df = df.copy()

    # OBTEM OS MAPAS DE GRUPOS E PRODUTOS
    map_grupo = obter_grupos_mapeados()
    map_produto = obter_produtos_mapeados()

    # OBTEM OS IDS DE GRUPO
    df['grupo_id'] = df['produto'].map(map_grupo)
    df['grupo_id'] = df['grupo_id'].ffill()

    # OBTEM OS IDS DE PRODUTO
    keys = [ (r['control'], r['grupo_id']) for _,r in df.iterrows() ]
    df['produto_id'] = [ map_produto.get(k) for k in keys ]

    # SEPARA OS GRUPOS DOS PRODUTOS EM 2 DATAFRAMES
    mascara = df['control'].isna() | (~df['control'].str.contains('_').astype(bool))
    lista_grupos = df.loc[mascara]
    lista_produtos = df.loc[~mascara]

    # LIMPA COLUNAS DESNECESSÁRIAS E MELT DOS DATAFRAMES
    lista_grupos = lista_grupos.set_index('grupo_id')
    lista_grupos = lista_grupos.drop(columns=['id','control', 'produto', 'produto_id'])
    lista_grupos = lista_grupos.melt(var_name='ano', value_name='valor', ignore_index=False)

    lista_produtos = lista_produtos.set_index('produto_id')
    lista_produtos = lista_produtos.drop(columns=['id','control', 'produto', 'grupo_id'])
    lista_produtos = lista_produtos.melt(var_name='ano', value_name='valor', ignore_index=False)

    return lista_grupos, lista_produtos

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
# IMPORTAÇÕES COMUNS
#==============================================================================
def importar_grupos(df: pd.DataFrame):
    df = df.copy()

    # DEFINE AS LINHAS REFERENTES A GRUPOS
    df['grupo']  = False
    mascara = df['control'].isna() | (~df['control'].str.contains('_').astype(bool))
    df.loc[mascara, 'grupo'] = True

    # IMPORTA OS GRUPOS
    total_importados = 0
    for _, linha in df[df['grupo']].iterrows():
        # se o grupo ainda não foi importado, salva no banco de dados
        if session.query(Grupo).where(Grupo.nome == linha['produto']).first() is None:
            grupo = Grupo(nome=linha['produto']) # cria um objeto Grupo
            session.add(grupo) # adiciona o objeto ao banco de dados
            total_importados += 1 # incrementa o contador de grupos importados
    session.commit() # salva as alterações no banco de dados
    print(f'Grupos importados: {total_importados}')


def importar_produtos(df: pd.DataFrame):
    df = df.copy()
    
    # mapeia os grupos em um dicionário
    grupos = obter_grupos_mapeados()
    
    # cria uma coluna para filtrar os grupos
    df['grupo']  = False
    mascara = df['control'].isna() | (~df['control'].str.contains('_').astype(bool))
    df.loc[mascara, 'grupo'] = True

    # cria uma coluna com o nome dos grupos dos produtos
    df['grupo_nome'] = None
    df.loc[df['grupo'], 'grupo_nome'] = df['produto']
    df['grupo_nome'] = df['grupo_nome'].ffill()

    # cria uma coluna com os id dos grupos dos produtos
    df = df.assign(grupo_id = df['grupo_nome'].map(grupos))

    total_importados = 0
    for index, linha in df[~df['grupo']].iterrows():
        # se o produto ainda não foi importado, salva no banco de dados
        if session.query(Produto).where(Produto.control == linha['control']).where(Produto.grupo_id == linha['grupo_id']).first() is None:
            produto = Produto(nome=linha['produto'].strip(), control=linha['control'], grupo_id=linha['grupo_id']) # cria um objeto Produto
            session.add(produto) # adiciona o objeto ao banco de dados
            total_importados += 1 # incrementa o contador de produtos importados
    session.commit() # salva as alterações no banco de dados
    print(f'Produtos importados: {total_importados}')

#==============================================================================
# PRODUÇÃO
#==============================================================================

# Baixando os dados de produção do site da Embrapa:
producao = pd.read_csv('http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv', sep=';')
producao = normalizar_columas(producao)

# IMPORTAR OS GRUPOS
importar_grupos(producao)

# IMPORTAR OS PRODUTOS
importar_produtos(producao)

# IMPORTAR DADOS DE PRODUÇÃO
lista_grupos, lista_produtos = preparar_dataset_grupo_produto(producao)

total_importados = 0
print('Importando dados de produção dos grupos...')
for index, linha in lista_grupos.iterrows():
    # se a produção do produto para o ano ainda não foi importada, salva no banco de dados
    if session.query(Producao).where(Producao.grupo_id == index, Producao.ano == linha['ano']).first() is None:
        producao = Producao(ano=linha['ano'], quantidade=linha['valor'], grupo_id=index) # cria um objeto Producao
        session.add(producao) # adiciona o objeto ao banco de dados
        total_importados += 1 # incrementa o contador de dados de produção importados
session.commit() # salva as alterações no banco de dados
print(f'Dados de produção importados: {total_importados}')

total_importados = 0
print('Importando dados de produção dos produtos...')
for index, linha in lista_produtos.iterrows():
    # se a produção do produto para o ano ainda não foi importada, salva no banco de dados
    if session.query(Producao).where(Producao.produto_id == index, Producao.ano == linha['ano']).first() is None:
        producao = Producao(ano=linha['ano'], quantidade=linha['valor'], produto_id=index) # cria um objeto Producao
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
comercio = pd.read_csv('http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv', sep=';')
comercio = normalizar_columas(comercio)

importar_grupos(comercio)

importar_produtos(comercio)

lista_grupos, lista_produtos = preparar_dataset_grupo_produto(comercio)

total_importados = 0
print('Importando dados de comercializacao dos grupos...')
for index, linha in lista_grupos.iterrows():
    if session.query(Comercializacao).where(Comercializacao.grupo_id == index, Comercializacao.ano == linha['ano']).first() is None:
        comercio = Comercializacao(
            ano=linha['ano'], quantidade=linha['valor'], grupo_id=index)
        session.add(comercio)  
        total_importados += 1  
session.commit() 
print(f'Dados de comercializacao importados: {total_importados}')

total_importados = 0
print('Importando dados de comercializacao dos produtos...')
for index, linha in lista_produtos.iterrows():
    if session.query(Comercializacao).where(Comercializacao.produto_id == index, Comercializacao.ano == linha['ano']).first() is None:
        comercio = Comercializacao(
            ano=linha['ano'], quantidade=linha['valor'], produto_id=index)
        session.add(comercio) 
        total_importados += 1 
session.commit()  
print(f'Dados de comercializacao importados: {total_importados}')

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

# Fecha a conexão com o banco de dados:
session.close()
engine.dispose()

