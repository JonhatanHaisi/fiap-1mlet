from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from models import entities, repository


def test_listar_atividade_usuario(mocker: MockerFixture):
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)
    repo = repository.AtividadeRepository(session=session_mock)

    mock_atividades = [
        entities.Atividade(id=1, usuario="usuario_id", materia_id="materia_id", tempo_leitura=1200, porcentagem_scroll=70),
        entities.Atividade(id=2, usuario="usuario_id", materia_id="materia_id", tempo_leitura=600, porcentagem_scroll=50)
    ]
    session_mock.query.return_value.filter_by.return_value.all.return_value = mock_atividades

    atividades = repo.listar_atividade_usuario("usuario_id")

    assert atividades == mock_atividades
    session_mock.query.assert_called_once_with(entities.Atividade)
    session_mock.query.return_value.filter_by.assert_called_once_with(usuario="usuario_id")
    session_mock.query.return_value.filter_by.return_value.all.assert_called_once()

def test_salvar_atividade_usuario(mocker:MockerFixture):
    session_mock = mocker.patch.object(Session, '__init__', return_value=None)

    repo = repository.AtividadeRepository(session=session_mock)
    atividade = entities.Atividade(id=1, usuario="usuario_id", materia_id="materia_id", tempo_leitura=1200, porcentagem_scroll=70)

    result = repo.salvar_atividade_usuario(atividade)

    assert result == atividade
    session_mock.add.assert_called_once_with(atividade)