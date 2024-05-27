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


@app.get("/grupo/{id}/comercializacao", response_model=List[models.Comercializacao], tags=["grupo"])
async def obter_comercializacao_do_grupo(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    grupo = session.query(entities.Grupo).where(entities.Grupo.id == id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return grupo.comercializacao

@app.get("/grupo/{id}/importacao_quantidade", response_model=List[models.Quantidade], tags=["grupo"])
async def obter_importacao_quantidade(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    quantidade = session.query(entities.Quantidade).where(entities.Quantidade.grupo_id == id).where(entities.Quantidade.categoria == 'importacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(quantidade) == 0 :
        raise HTTPException(status_code=404, detail="Quantidade de importação por grupo não encontrada")
    return quantidade

@app.get("/grupo/{id}/importacao_faturamento", response_model=List[models.Faturamento], tags=["grupo"])
async def obter_importacao_faturamento(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    faturamento = session.query(entities.Faturamento).where(entities.Faturamento.grupo_id == id).where(entities.Faturamento.categoria == 'importacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(faturamento) == 0 :
        raise HTTPException(status_code=404, detail="Faturamento de importação por grupo não encontrada")
    return faturamento

@app.get("/grupo/{id}/exportacao_quantidade", response_model=List[models.Quantidade], tags=["grupo"])
async def obter_exportacao_quantidade(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    quantidade = session.query(entities.Quantidade).where(entities.Quantidade.grupo_id == id).where(entities.Quantidade.categoria == 'exportacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(quantidade) == 0 :
        raise HTTPException(status_code=404, detail="Quantidade de exportação por grupo não encontrada")
    return quantidade

@app.get("/grupo/{id}/exportacao_faturamento", response_model=List[models.Faturamento], tags=["grupo"])
async def obter_exportacao_faturamento(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    faturamento = session.query(entities.Faturamento).where(entities.Faturamento.grupo_id == id).where(entities.Faturamento.categoria == 'exportacao').all()
    # se o produto não for encontrado, retorna um erro 404
    if len(faturamento) == 0 :
        raise HTTPException(status_code=404, detail="Faturamento de exportação por grupo não encontrada")
    return faturamento


@app.get("/grupo/{id}/processamento", response_model=List[models.Processamento], tags=["grupo"])
async def obter_processamento_do_grupo(id:int , session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    grupo = session.query(entities.Grupo).where(entities.Grupo.id == id).first()
    # se o produto não for encontrado, retorna um erro 404
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return grupo.processamento

