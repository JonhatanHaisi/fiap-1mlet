from models import models


def test_atividade_body_to_entity():
    atividade_body = models.AtividadeBody(
        usuario="usuario_id",
        materia="materia_id",
        tempoLeitura=1200,
        porcentagemScroll=70
    )
    atividade_entity = atividade_body.to_entity()

    assert atividade_entity.usuario == "usuario_id"
    assert atividade_entity.materia_id == "materia_id"
    assert atividade_entity.tempo_leitura == 1200
    assert atividade_entity.porcentagem_scroll == 70
    