from fastapi import FastAPI


# Cria uma instância de FastAPI
app = FastAPI(
    title="1MLET - API Embrapa",
    description="API para consumo de dados de vinicultura da Embrapa",
    version="0.1.0",
)
