from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

import regex as re
import pytest

from models import models, entities
from api import api_usuario


@pytest.mark.asyncio
async def test_obter_id_usuario():
    id = await api_usuario.obter_id_usuario()
    assert re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$').match(id), 'ID inválido'


@pytest.mark.asyncio
async def test_salvar_registro_atividade(mocker: MockerFixture):
    atividade = models.AtividadeBody(
        usuario='123',
        materia='abc',
        tempo_leitura=10,
        porcentagem_scroll=20
    )

    repo_mock = mocker.patch('models.repository.AtividadeRepository.salvar_atividade_usuario')
    repo_mock.return_value = entities.Atividade(id=1)
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)

    response = await api_usuario.salvar_registro_atividade(atividade, session_mock)

    assert response == {"message": "Atividade salva com sucesso", "id": 1}, 'Response inválido'
    session_mock.commit.assert_called_once()
    

@pytest.mark.asyncio
async def test_obter_materias_lidas(mocker: MockerFixture):
    expected = [entities.Atividade(id=1)]

    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    repo_mock = mocker.patch('models.repository.AtividadeRepository.listar_atividade_usuario')
    repo_mock.return_value = expected

    response = await api_usuario.obter_materias_lidas('123', session_mock)

    assert response == expected, 'Response inválido'
