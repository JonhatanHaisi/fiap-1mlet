from infra.application import app
from infra.database import Session, create_session
from infra.security import autenticado

from models import entities
from models import models

from typing import List

from fastapi import Depends, HTTPException


# Define as rotas da API
# Essas rotas são acessíveis em http://localhost:8000/docs

# "/produto" é o prefixo da rota e "{id}" é um parâmetro
# o parâmetro "{id}" é passado para a função como um argumento
# response_model=models.Produto é um argumento que indica que a função retorna um produto
# tags=["produto"] é um argumento que indica que a função pertence ao grupo "produto"

# a função retorna um produto com o id correspondente
# o argumento "session" é uma sessão do banco de dados
# o argumento "autenticado" é um booleano que indica se o usuário está autenticado
@app.get("/produto/{id}", response_model=models.Produto, tags=["produto"])
async def obter_produto(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    produto = session.query(entities.Produto).where(entities.Produto.id == id).first()
    
    # se o produto não for encontrado, retorna um erro 404
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto


# "/produto" é o prefixo da rota
# response_model=List[models.Produto] é um argumento que indica que a função retorna uma lista de produtos
# tags=["produto"] é um argumento que indica que a função pertence ao grupo "produto"

# a função retorna uma lista de produtos
# o argumento "session" é uma sessão do banco de dados
# o argumento "autenticado" é um booleano que indica se o usuário está autenticado
@app.get("/produto", response_model=List[models.Produto], tags=["produto"])
async def listar_produto(session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    return session.query(entities.Produto).all()
    

# "/produto/{id}/producao" é o prefixo da rota e "{id}" é um parâmetro
# o parâmetro "{id}" é passado para a função como um argumento
# response_model=List[models.Producao] é um argumento que indica que a função retorna uma lista de produção
# tags=["produto"] é um argumento que indica que a função pertence ao grupo "produto"

# a função retorna uma lista de produção de um produto com o id correspondente
# o argumento "session" é uma sessão do banco de dados
# o argumento "autenticado" é um booleano que indica se o usuário está autenticado
@app.get("/produto/{id}/producao", response_model=List[models.Producao], tags=["produto"])
async def obter_producao_do_produto(id:int, session:Session=Depends(create_session), autenticado=Depends(autenticado)):
    produto = session.query(entities.Produto).where(entities.Produto.id == id).first()
    # se o produto não for encontrado, retorna um erro 404
    if produto is None:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    return produto.producao
