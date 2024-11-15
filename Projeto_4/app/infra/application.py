from fastapi import FastAPI


# Cria uma instância de FastAPI
app = FastAPI(
    title="1MLET - API de Previsão de Preço de Ações",
    description="API para utilização de modelo de previsão de preço de fechamento de ações",
    version="0.1.0",
)
