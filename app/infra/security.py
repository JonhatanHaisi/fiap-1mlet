from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException

from infra.database import create_session, Session
from models.entities import User

import hashlib


# Cria uma instância de HTTPBasic para autenticação
# essa classe é responsável por fazer a validação das credenciais
security = HTTPBasic()


# Função que valida as credenciais
# essa função verifica se o usuário e senha são válidos
# se não forem válidos, retorna um erro 401
def autenticado(credenciais: HTTPBasicCredentials=Depends(security), session:Session=Depends(create_session)):
    user = session.query(User).where(User.username == credenciais.username).first()
    if user is None or hashlib.md5(credenciais.password.encode()).hexdigest() != user.password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return True
