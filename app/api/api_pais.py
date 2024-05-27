from infra.application import app
from infra.database import Session, create_session
from infra.security import autenticado

from models import entities
from models import models

from typing import List

from fastapi import Depends, HTTPException


@app.get("/pais/{id}", response_model=models.Pais, tags=["pais"])
async def obter_pais(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    pais = session.query(entities.Pais).where(entities.Pais.id == id).first()
    if pais is None:
        raise HTTPException(status_code=404, detail="País não encontrado")
    return pais

@app.get("/pais", response_model=List[models.Pais], tags=["pais"])
async def listar_pais(session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    return session.query(entities.Pais).all()

@app.get("/pais/{id}/importacao_quantidade", response_model=List[models.Quantidade], tags=["pais"])
async def obter_importacao_quantidade(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    quantidade = session.query(entities.Quantidade).where(entities.Quantidade.pais_id == id).where(entities.Quantidade.categoria == 'importacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(quantidade) == 0 :
        raise HTTPException(status_code=404, detail="Quantidade de importação não encontrada")
    return quantidade

@app.get("/pais/{id}/importacao_faturamento", response_model=List[models.Faturamento], tags=["pais"])
async def obter_importacao_quantidade(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    faturamento = session.query(entities.Faturamento).where(entities.Faturamento.pais_id == id).where(entities.Faturamento.categoria == 'importacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(faturamento) == 0 :
        raise HTTPException(status_code=404, detail="Faturamento de importação não encontrada")
    return faturamento

@app.get("/pais/{id}/exportacao_quantidade", response_model=List[models.Quantidade], tags=["pais"])
async def obter_importacao_quantidade(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    quantidade = session.query(entities.Quantidade).where(entities.Quantidade.pais_id == id).where(entities.Quantidade.categoria == 'exportacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(quantidade) == 0 :
        raise HTTPException(status_code=404, detail="Quantidade de exportação não encontrada")
    return quantidade

@app.get("/pais/{id}/exportacao_faturamento", response_model=List[models.Faturamento], tags=["pais"])
async def obter_importacao_quantidade(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    faturamento = session.query(entities.Faturamento).where(entities.Faturamento.pais_id == id).where(entities.Faturamento.categoria == 'exportacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(faturamento) == 0 :
        raise HTTPException(status_code=404, detail="Faturamento de exportação não encontrada")
    return faturamento