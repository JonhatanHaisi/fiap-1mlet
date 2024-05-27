from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pathlib import Path
from models.entities import Base, User, Grupo, Produto, Producao, Comercializacao, Pais, Quantidade, Faturamento, Processamento

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

def obter_pais_mapeados(): 
    return { pais.nome:pais.id for pais in session.query(Pais).all() }

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

def preparar_dataset_importacao_exportacao(df:pd.DataFrame):
    # Alterando a estrutura dos dados do dataframe para facilitar a importação de dados de importacção e exportacao de produto
    #MAPEA PAISES NO BANCO DE DADOS
    maps_pais = obter_pais_mapeados()

    df['pais_id'] = df['país'].map(maps_pais)

    df = df.set_index('id')
    df = df.drop(columns='país') # a coluna com o nome do pais é removida
    #separação de tabela por quantidade e faturamento
    df = df.melt(id_vars=['pais_id', 'produto','control'], var_name='ano', value_name='valor', ignore_index=False)# transforma colunas em linhas
    df['valor'] = df['valor'].fillna(0) # preenche NaN com zeros
    lista_quantidade = df[df['ano'].str.len() == 4] # filtra apenas quantidade
    lista_faturamento = df[df['ano'].str.len() <= 5] # filtra apenas o faturamento
    lista_faturamento['ano'] = lista_faturamento['ano'].astype(float).astype(int) #transforma objeto em inteiro

    return lista_quantidade, lista_faturamento

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

#importação para banco de dados dos paises
def importa_pais(df:pd.DataFrame):
    # Salvando no banco de dados todos os paises que ainda não foram importados:
    total_importados = 0
    for _, linha in df.iterrows():
        # se o pais ainda não foi importado, salva no banco de dados
        if session.query(Pais).where(Pais.nome == linha['país']).first() is None:
            pais = Pais(nome=linha['país']) # cria um objeto impVinho
            session.add(pais) # adiciona o objeto ao banco de dados
            total_importados += 1 # incrementa o contador de impVinho importados
    session.commit() # salva as alterações no banco de dados
    print(f'Importação de paises: {total_importados}')    

#importacao para banco de dados da quantidade de grupos importados e exportados 
def importa_quantidade(df:pd.DataFrame):
    df = df.copy()

    # OBTEM OS MAPAS DE GRUPOS
    map_grupo = obter_grupos_mapeados()

    # OBTEM OS IDS DE GRUPO
    df['grupo_id'] = df['produto'].map(map_grupo)
    df['grupo_id'] = df['grupo_id'].ffill()

    # Salvando no banco de dados todos os dados de produção que ainda não foram importados:
    total_importados = 0
    for _, linha in df.iterrows():
        # se o Quantidade do produto para o ano ainda não foi importada, salva no banco de dados
        if session.query(Quantidade).where(Quantidade.pais_id == linha['pais_id'], Quantidade.grupo_id == linha['grupo_id'], Quantidade.categoria == linha['control'], Quantidade.ano == linha['ano']).first() is None:
            quantidade = Quantidade(categoria=linha['control'], ano=linha['ano'], quantidade=linha['valor'],  grupo_id=linha['grupo_id'], pais_id=linha['pais_id']) # cria um objeto Faturamento
            session.add(quantidade) # adiciona o objeto ao banco de dados
            total_importados += 1 # incrementa o contador de dados de produção importados
    session.commit() # salva as alterações no banco de dados
    print(f'Dados de quantidade de importação - importados: {total_importados}')

#importacao para banco de dados do faturamento de grupos importados e exportados 
def importa_faturamento(df:pd.DataFrame):
    df = df.copy()

    # OBTEM OS MAPAS DE GRUPOS
    map_grupo = obter_grupos_mapeados()

    # OBTEM OS IDS DE GRUPO
    df['grupo_id'] = df['produto'].map(map_grupo)
    df['grupo_id'] = df['grupo_id'].ffill()

    total_importados = 0
    for index, linha in df.iterrows():
        # se o faturamento do produto para o ano ainda não foi importada, salva no banco de dados
        if session.query(Faturamento).where(Faturamento.pais_id == linha['pais_id'], Faturamento.grupo_id == linha['grupo_id'],Faturamento.categoria == linha['control'], Faturamento.ano == linha['ano']).first() is None:
            fatura = Faturamento(categoria=linha['control'], ano=linha['ano'], faturamento=linha['valor'],  grupo_id=linha['grupo_id'], pais_id=linha['pais_id']) # cria um objeto Faturamento
            session.add(fatura) # adiciona o objeto ao banco de dados
            total_importados += 1 # incrementa o contador de dados de produção importados
    session.commit() # salva as alterações no banco de dados
    print(f'Dados de faturamento de importação - importados: {total_importados}')

#faz o tratamento dos arquivos de importação e exportação
def importar_dados_importacao_exportacao(url, nome_grupo, control):
    df = pd.read_csv(url, sep=';')
    df = normalizar_columas(df)
    df['produto'] = nome_grupo
    df['control'] = control

    importar_grupos(df)

    importa_pais(df)

    # PREPARA ARQUIVO PARA IMPORTAR
    quantidade, faturamento = preparar_dataset_importacao_exportacao(df)

    importa_quantidade(quantidade)

    importa_faturamento(faturamento)

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
def importacao_processamento(url):
    processamento = pd.read_csv(url, sep='\t')
    processamento = normalizar_columas(processamento)
    processamento = processamento.rename(columns={'cultivar':'produto'})
    processamento = processamento.drop(columns=['2022'])    

    # IMPORTAR OS GRUPOS
    importar_grupos(processamento)

    # IMPORTAR OS PRODUTOS
    importar_produtos(processamento)

    # IMPORTAR DADOS DE PRODUÇÃO
    lista_grupos, lista_produtos = preparar_dataset_grupo_produto(processamento)

    # REMOVER VALORES NÃO NUMÉRICOS DA COLUNA VALOR
    def converter_para_int(valor):
        try:
            return int(valor)
        except:
            return 0
        
    lista_grupos['valor'] = lista_grupos['valor'].apply(converter_para_int)
    lista_produtos['valor'] = lista_produtos['valor'].apply(converter_para_int)

    # Salvando no banco de dados todos os processamentos que ainda não foram importados:
    total_importados = 0
    print('Importando dados de processamento dos grupos...')
    for index, linha in lista_grupos.iterrows():
        # Se o processamento ainda não foi importado, salva no banco de dados
        if session.query(Processamento).where(Processamento.grupo_id == index, Processamento.ano == linha['ano']).first() is None:
            processamento = Processamento(ano=linha['ano'], quantidade=linha['valor'], grupo_id=index)  # cria um objeto Processamento
            session.add(processamento)  # adiciona o objeto ao banco de dados
            total_importados += 1  # incrementa o contador de processamentos importados
    session.commit()  # salva as alterações no banco de dados
    print(f'Processamentos importados: {total_importados}')

    total_importados = 0
    for index, linha in lista_produtos.iterrows():
        # Se o processamento ainda não foi importado, salva no banco de dados
        if session.query(Processamento).where(Processamento.produto_id == index, Processamento.ano == linha['ano']).first() is None:
            processamento = Processamento(ano=linha['ano'], quantidade=linha['valor'], produto_id=index)  # cria um objeto Processamento
            session.add(processamento)  # adiciona o objeto ao banco de dados
            total_importados += 1  # incrementa o contador de processamentos importados
    session.commit()  # salva as alterações no banco de dados
    print(f'Processamentos importados: {total_importados}')

importacao_processamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv')
importacao_processamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv')
importacao_processamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv')
importacao_processamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv')

#==============================================================================
# COMERCIALIZAÇÃO	
#==============================================================================
comercializacao = pd.read_csv('http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv', sep=';')
comercializacao = normalizar_columas(comercializacao)

importar_grupos(comercializacao)

importar_produtos(comercializacao)

lista_grupos, lista_produtos = preparar_dataset_grupo_produto(comercializacao)

total_importados = 0
print('Importando dados de comercializacao dos grupos...')
for index, linha in lista_grupos.iterrows():
    if session.query(Comercializacao).where(Comercializacao.grupo_id == index, Comercializacao.ano == linha['ano']).first() is None:
        comercializacao = Comercializacao(
            ano=linha['ano'], quantidade=linha['valor'], grupo_id=index)
        session.add(comercializacao)  
        total_importados += 1  
session.commit() 
print(f'Dados de comercializacao importados: {total_importados}')

total_importados = 0
print('Importando dados de comercializacao dos produtos...')
for index, linha in lista_produtos.iterrows():
    if session.query(Comercializacao).where(Comercializacao.produto_id == index, Comercializacao.ano == linha['ano']).first() is None:
        comercializacao = Comercializacao(
            ano=linha['ano'], quantidade=linha['valor'], produto_id=index)
        session.add(comercializacao) 
        total_importados += 1 
session.commit()  
print(f'Dados de comercializacao importados: {total_importados}')

#==============================================================================
# IMPORTAÇÃO
#==============================================================================
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv', 'VINHO DE MESA', 'importacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv', 'ESPUMANTES', 'importacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv', 'UVAS FRESCAS', 'importacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv', 'UVAS PASSAS', 'importacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv', 'SUCO DE UVAS', 'importacao')

#==============================================================================
# EXPORTAÇÃO
#==============================================================================
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv', 'VINHO DE MESA', 'exportacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv', 'ESPUMANTES', 'exportacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv', 'UVAS FRESCAS', 'exportacao')
importar_dados_importacao_exportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv', 'SUCO DE UVAS', 'exportacao')


#==============================================================================
# FINALIZAÇÃO DO SCRIPT
#==============================================================================

# Fecha a conexão com o banco de dados:
session.close()
engine.dispose()

