from infra.application import app
from infra.database import Session, create_session

from fastapi_cache.decorator import cache

from models.repository import AtividadeRepository
from models.models import AtividadeBody, AtividadeResponse 

from fastapi import Depends, Body
from typing import List

import uuid


@app.get("/usuario/id", tags=["usuario"])
async def obter_id_usuario():
    return str(uuid.uuid4())


@app.post("/usuario/atividade", tags=["usuario"])
async def salvar_registro_atividade(
    atividade: AtividadeBody = Body(...), 
    session:Session=Depends(create_session)
):
    repo = AtividadeRepository(session)
    entity = repo.salvar_atividade_usuario(atividade.to_entity())
    session.commit()
    return {"message": "Atividade salva com sucesso", "id": entity.id}

@app.get("/usuario/atividades/{usuario_id}", response_model=List[AtividadeResponse], tags=["usuario"])
async def obter_materias_lidas(usuario_id: str, session: Session=Depends(create_session)):
    return AtividadeRepository(session).listar_atividade_usuario(usuario_id)

