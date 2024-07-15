from app.api.api_pais import obter_pais, listar_pais, obter_importacao_quantidade, obter_importacao_faturamento, obter_exportacao_quantidade, obter_exportacao_faturamento
from app.models.entities import Pais, Quantidade, Faturamento
from app.infra.database import Session

from pytest_mock import MockerFixture
import pytest

@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_Pais(mocker: MockerFixture): # define a função de teste
    
    pais = Pais(id=1, nome='Pais 1') # cria um pais

    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = pais # configura o mock para retornar o pais

    resultado = await obter_pais(1, mock_session, True) # chama a função obter_pais
    
    assert resultado == pais, 'A função obter_pais não retornou o pais correto' # verifica se o resultado é o pais esperado
    

@pytest.mark.asyncio # indica que a função é assíncrona
async def test_obter_pais_nao_encontrado(mocker: MockerFixture): # define a função de teste
    mock_session = mocker.patch.object(Session, '__init__', return_value=None) # cria um mock da classe Session
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = None # configura o mock para retornar None

    with pytest.raises(Exception) as excinfo: # verifica se a função obter_pais retorna uma exceção
        await obter_pais(1, mock_session, True) # chama a função obter_pais
        
    assert 'País não encontrado' in str(excinfo.value), 'A função obter_pais não retornou o erro correto' # verifica se a exceção é a esperada

@pytest.mark.asyncio
async def test_listar_pais(mocker: MockerFixture):
    pais = [Pais(id=1, nome='Grupo 1'), Pais(id=2, nome='Grupo 2')]

    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .all.return_value = pais

    resultado = await listar_pais(session_mock, True)
        
    assert resultado == pais, 'A função listar_pais não retornou a lista de pais correta'

@pytest.mark.asyncio
async def test_obter_importacao_quantidade(mocker: MockerFixture):
    lista_quantidade = [
        Quantidade(id=1, grupo_id=1, quantidade=10),
        Quantidade(id=2, grupo_id=1, quantidade=20)
    ]

    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = lista_quantidade
    
    resultado = await obter_importacao_quantidade(1, session_mock, True)

    assert resultado == lista_quantidade, 'A função obter_importacao_quantidade não retornou a comercialização correta'

@pytest.mark.asyncio
async def test_obter_importacao_quantidade(mocker: MockerFixture):
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = []

    with pytest.raises(Exception) as excinfo:
        await obter_importacao_quantidade(1, session_mock, True)
        
    assert 'Quantidade de importação não encontrada' in str(excinfo.value), 'A função obter_importacao_quantidade não retornou o erro correto'

@pytest.mark.asyncio
async def test_obter_importacao_faturamento(mocker: MockerFixture):
    lista_faturamento = [
        Faturamento(id=1, grupo_id=1, quantidade=10),
        Faturamento(id=2, grupo_id=1, quantidade=20)
    ]

    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = lista_faturamento
    
    resultado = await obter_importacao_faturamento(1, session_mock, True)

    assert resultado == lista_faturamento, 'A função obter_importacao_faturamento não retornou a comercialização correta'

@pytest.mark.asyncio
async def test_obter_importacao_faturamento(mocker: MockerFixture):
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = []

    with pytest.raises(Exception) as excinfo:
        await obter_importacao_faturamento(1, session_mock, True)
        
    assert 'Faturamento de importação não encontrada' in str(excinfo.value), 'A função obter_importacao_faturamento não retornou o erro correto'

@pytest.mark.asyncio
async def test_obter_exportacao_quantidade(mocker: MockerFixture):
    lista_quantidade = [
        Quantidade(id=1, grupo_id=1, quantidade=10),
        Quantidade(id=2, grupo_id=1, quantidade=20)
    ]

    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = lista_quantidade
    
    resultado = await obter_exportacao_quantidade(1, session_mock, True)

    assert resultado == lista_quantidade, 'A função obter_exportacao_quantidade não retornou a comercialização correta'

@pytest.mark.asyncio
async def test_obter_exportacao_quantidade(mocker: MockerFixture):
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = []

    with pytest.raises(Exception) as excinfo:
        await obter_exportacao_quantidade(1, session_mock, True)
        
    assert 'Quantidade de exportação não encontrada' in str(excinfo.value), 'A função obter_exportacao_quantidade não retornou o erro correto'

@pytest.mark.asyncio
async def test_obter_exportacao_faturamento(mocker: MockerFixture):
    lista_faturamento = [
        Faturamento(id=1, grupo_id=1, quantidade=10),
        Faturamento(id=2, grupo_id=1, quantidade=20)
    ]

    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = lista_faturamento
    
    resultado = await obter_exportacao_faturamento(1, session_mock, True)

    assert resultado == lista_faturamento, 'A função obter_exportacao_faturamento não retornou a comercialização correta'

@pytest.mark.asyncio
async def test_obter_exportacao_faturamento(mocker: MockerFixture):
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    session_mock.query.return_value \
                .where.return_value \
                .where.return_value \
                .all.return_value = []

    with pytest.raises(Exception) as excinfo:
        await obter_exportacao_faturamento(1, session_mock, True)
        
    assert 'Faturamento de exportação não encontrada' in str(excinfo.value), 'A função obter_exportacao_faturamento não retornou o erro correto'
