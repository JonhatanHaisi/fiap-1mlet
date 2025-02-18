from infra.application import app
from infra.database import Session, create_session

from fastapi import Depends
from typing import List

from models import recomendacao, models


@app.post("/recomendacao", response_model=List[models.Recomendacao], tags=["recomendação"])
async def obter_recomendacao(usuario: str = None, session:Session = Depends(create_session)):
    return await recomendacao.obter_recomendacao_usuario(usuario, session)
