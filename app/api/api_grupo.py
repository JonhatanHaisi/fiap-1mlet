from infra.application import app
from infra.database import Session, create_session
from infra.security import autenticado

from models import entities
from models import models

from typing import List

from fastapi import Depends, HTTPException


@app.get("/grupo/{id}", response_model=models.Grupo, tags=["grupo"])
async def obter_grupo(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    grupo = session.query(entities.Grupo).where(entities.Grupo.id == id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return grupo


@app.get("/grupo", response_model=List[models.Grupo], tags=["grupo"])
async def listar_grupo(session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    return session.query(entities.Grupo).all()
    

@app.get("/grupo/{id}/produtos", response_model=List[models.Produto], tags=["grupo"])
async def obter_produtos_do_grupo(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    grupo = session.query(entities.Grupo).where(entities.Grupo.id == id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrada")
    return grupo.produtos

@app.get("/grupo/{id}/producao", response_model=List[models.Producao], tags=["grupo"])
async def obter_producao_do_grupo(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    grupo = session.query(entities.Grupo).where(entities.Grupo.id == id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrada")
    return grupo.producao
