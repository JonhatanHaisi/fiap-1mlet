from app.api.api_produto import obter_produto, listar_produto, obter_producao_do_produto, obter_comercializacao_do_produto, obter_processamento_do_produto
from app.models.entities import Produto, Producao, Comercializacao, Processamento
from app.infra.database import Session

from pytest_mock import MockerFixture
import pytest

@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_produto(mocker: MockerFixture): # define a função de teste
    
    produto = Produto(id=1, nome='Produto 1') # cria um produto

    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = produto # configura o mock para retornar o produto

    resultado = await obter_produto(1, mock_session, True) # chama a função obter_produto
    
    assert resultado == produto, 'A função obter_produto não retornou o produto correto' # verifica se o resultado é o produto esperado
    

@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_produto_nao_encontrado(mocker: MockerFixture): # define a função de teste
    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = None # configura o mock para retornar None

    with pytest.raises(Exception) as excinfo: # verifica se a função obter_produto retorna uma exceção
        await obter_produto(1, mock_session, True) # chama a função obter_produto
        
    assert 'Produto não encontrado' in str(excinfo.value), 'A função obter_produto não retornou o erro correto' # verifica se a exceção é a esperada


@pytest.mark.asyncio # indica que a função é assíncrona
async def test_listar_produto(mocker): # define a função de teste
    produtos = [Produto(id=1, nome='Produto 1'), Produto(id=2, nome='Produto 2')] # cria uma lista de produtos

    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .all.return_value = produtos # configura o mock para retornar os produtos

    resultado = await listar_produto(mock_session, True) # chama a função listar_produto
        
    assert resultado == produtos, 'A função listar_produto não retornou a lista de produtos correta' # verifica se o resultado é a lista de produtos esperada



@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_producao_do_produto(mocker): # define a função de teste
    produto = Produto(id=1, nome='Produto 1', producao=[]) # cria um produto
    produto.producao.extend([ # adiciona produção ao produto
        Producao(id=1, ano=2021, quantidade=100, produto_id=1), 
        Producao(id=2, ano=2020, quantidade=200, produto_id=1)
    ])

    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .where.return_value. \
                first.return_value = produto # configura o mock para retornar o produto

    resultado = await obter_producao_do_produto(1, mock_session, True) # chama a função obter_producao_do_produto

    assert resultado == produto.producao, 'A função obter_producao não retornou a lista de produção correta' # verifica se o resultado é a lista de produção esperada


@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_producao_do_produto_nao_encontrado(mocker):
    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = None # configura o mock para retornar None

    with pytest.raises(Exception) as excinfo:
        await obter_producao_do_produto(1, mock_session, True) # chama a função obter_producao_do_produto

    assert 'Produção não encontrada' in str(excinfo.value), 'A função obter_producao não retornou o erro correto' # verifica se a exceção é a esperada

#==============================================================================
# COMERCIALIZAÇÃO	
#==============================================================================
@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_comercializacao_do_produto(mocker): 
    produto = Produto(id=1, nome='Produto 1', comercializacao=[])
    produto.comercializacao.extend([ 
        Comercializacao(id=1, ano=2021, quantidade=100, produto_id=1), 
        Comercializacao(id=2, ano=2020, quantidade=200, produto_id=1)
    ])

    mock_session = mocker.patch.object(Session, '__init__', return_value=None) 
    mock_session.query.return_value \
                .where.return_value. \
                first.return_value = produto 

    resultado = await obter_comercializacao_do_produto(1, mock_session, True) 

    assert resultado == produto.comercializacao, 'A função obter_comercializacao não retornou a lista de comercialização correta' 


@pytest.mark.asyncio 
async def test_obter_comercializacao_do_produto_nao_encontrado(mocker):
    mock_session = mocker.patch.object(Session, '__init__', return_value=None) 
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = None 

    with pytest.raises(Exception) as excinfo:
        await obter_comercializacao_do_produto(1, mock_session, True) 

    assert 'Comercialização não encontrado' in str(excinfo.value), 'A função obter_comercializacao não retornou o erro correto' 



@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_processamento_do_produto(mocker): 
    produto = Produto(id=1, nome='Produto 1', processamento=[])
    produto.processamento.extend([ 
        Processamento(id=1, ano=2021, quantidade=100, produto_id=1), 
        Processamento(id=2, ano=2020, quantidade=200, produto_id=1)
    ])

    mock_session = mocker.patch.object(Session, '__init__', return_value=None) 
    mock_session.query.return_value \
                .where.return_value. \
                first.return_value = produto 

    resultado = await obter_processamento_do_produto(1, mock_session, True) 

    assert resultado == produto.processamento, 'A função obter_processamento não retornou a lista de processamento correta'
