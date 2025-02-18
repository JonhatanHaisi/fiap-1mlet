from infra.application import app
from infra.database import Session, create_session

from models import repository
from models import entities
from models import models

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
from fastapi import Depends, Body
from typing import List

import uuid


@app.post("/usuario/id", tags=["usuario"])
async def obter_id_usuario():
    return str(uuid.uuid4())


@cache(expire=600)
@app.post("/usuario/atividade", tags=["usuario"])
async def salvar_registro_atividade(
    atividade: models.AtividadeBody = Body(...), 
    session:Session=Depends(create_session)
):
    repo = repository.AtividadeRepository(session)
    entity = repo.salvar_atividade_usuario(atividade.to_entity())
    session.commit()
    return {"message": "Atividade salva com sucesso", "id": entity.id}


@app.get("/usuario/atividades/{usuario_id}", response_model=List[models.AtividadeResponse], tags=["usuario"])
async def obter_materias_lidas(usuario_id: str, session: Session=Depends(create_session)):
    await FastAPICache.clear('salvar_registro_atividade', usuario_id)
    return repository.AtividadeRepository(session).listar_atividade_usuario(usuario_id)

