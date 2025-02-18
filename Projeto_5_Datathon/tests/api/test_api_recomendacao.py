from pytest_mock import MockerFixture
import pytest

from app.api import api_recomendacoes

@pytest.mark.asyncio
async def test_obter_recomendacao(mocker: MockerFixture):
    recomendacao_mock = mocker.patch("models.recomendacao.obter_recomendacao_usuario")
    recomendacao_mock.return_value = [ 'Resposnse' ]

    response = await api_recomendacoes.obter_recomendacao(usuario="usuario", session=None)

    assert response == [ 'Resposnse' ], "Response should be [ 'Resposnse' ]"


