from app.api.api_pais import obter_pais
from app.models.entities import Pais
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