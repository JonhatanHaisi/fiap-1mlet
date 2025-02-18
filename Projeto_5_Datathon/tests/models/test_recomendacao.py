from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

import datetime
import pytest

from models import recomendacao, models, entities


@pytest.fixture
def mock_session(mocker: MockerFixture):
    session_mock = mocker.MagicMock(spec=Session)
    return session_mock


@pytest.mark.asyncio
async def test_obter_recomendacao_usuario_cold_start(mock_session, mocker: MockerFixture):
    mock_session.query.return_value.filter_by.return_value.all.return_value = []
    mocker.patch("models.recomendacao.obter_recomendacoes_cold_start", return_value=["cold_start_recommendation"])

    result = await recomendacao.obter_recomendacao_usuario("usuario_id", mock_session)

    assert result == ["cold_start_recommendation"]
    mock_session.query.assert_called_once_with(entities.Atividade)
    mock_session.query.return_value.filter_by.assert_called_once_with(usuario="usuario_id")
    mock_session.query.return_value.filter_by.return_value.all.assert_called_once()


@pytest.mark.asyncio
async def test_obter_recomendacao_usuario_personalizada(mock_session, mocker: MockerFixture):
    mock_atividades = [
        entities.Atividade(id=1, usuario="usuario_id", materia_id="materia_id", tempo_leitura=1200, porcentagem_scroll=70)
    ]
    mock_session.query.return_value.filter_by.return_value.all.return_value = mock_atividades
    mocker.patch("models.recomendacao.obter_recomendacoes_personalizadas", return_value=["personalized_recommendation"])

    result = await recomendacao.obter_recomendacao_usuario("usuario_id", mock_session)

    assert result == ["personalized_recommendation"]
    mock_session.query.assert_called_once_with(entities.Atividade)
    mock_session.query.return_value.filter_by.assert_called_once_with(usuario="usuario_id")
    mock_session.query.return_value.filter_by.return_value.all.assert_called_once()


@pytest.mark.asyncio
async def test_obter_recomendacoes_cold_start(mocker: MockerFixture):
    mock_df = mocker.patch("pandas.read_csv").return_value
    mock_df.iterrows.return_value = iter([
        (0, {"page": "1", "title": "Titulo 1", "caption": "Descricao 1"}),
        (1, {"page": "2", "title": "Titulo 2", "caption": "Descricao 2"})
    ])

    result = await recomendacao.obter_recomendacoes_cold_start()

    assert len(result) == 2
    assert result[0].id == "1"
    assert result[0].titulo == "Titulo 1"
    assert result[0].descricao == "Descricao 1"
    assert result[1].id == "2"
    assert result[1].titulo == "Titulo 2"
    assert result[1].descricao == "Descricao 2"


@pytest.mark.asyncio
async def test_obter_recomendacoes_personalizadas(mock_session, mocker: MockerFixture):
    mock_materia = entities.Materia(id="materia_id", titulo="Titulo", descricao="Descricao", conteudo="Conteudo", publicado=datetime.datetime.now())
    mock_session.query.return_value.order_by.return_value.first.return_value = mock_materia
    mock_session.query.return_value.filter.return_value.all.return_value = [mock_materia]
    mock_session.query.return_value.filter_by.return_value.all.return_value = [
        entities.Atividade(id=1, usuario="usuario_id", materia_id="outro_id", tempo_leitura=1200, porcentagem_scroll=70, materia=mock_materia)
    ]

    mocker.patch("models.recomendacao.TEXT_VECTORIZER.transform", return_value=[[1]])
    mocker.patch("models.recomendacao.ACTIVITY_TRANSFORMER.transform", return_value=[[0.1]])
    mocker.patch("sklearn.metrics.pairwise.cosine_similarity", return_value=[[0.9]])

    result = await recomendacao.obter_recomendacoes_personalizadas("usuario_id", mock_session)

    assert len(result) == 1
    assert result[0].id == "materia_id"
    assert result[0].titulo == "Titulo"
    assert result[0].descricao == "Descricao"
