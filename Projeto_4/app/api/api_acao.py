from infra.application import app
from infra.security import autenticado

from fastapi import Depends, HTTPException

from model.acao import MODEL, obter_dados_acao_preparados


@app.get("/acao/previsao/{ticker}")
async def previsao_acao(ticker:str):
    data, last_date = obter_dados_acao_preparados(ticker)
    prediction  = MODEL(data)
    return {"ticker": ticker, "previsao": prediction.tolist()[0][0], "last_close_date": last_date }


