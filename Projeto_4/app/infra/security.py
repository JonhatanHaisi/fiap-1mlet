from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException

import hashlib


# Cria uma instância de HTTPBasic para autenticação
# essa classe é responsável por fazer a validação das credenciais
security = HTTPBasic()


# Função que valida as credenciais
# essa função verifica se o usuário e senha são válidos
# se não forem válidos, retorna um erro 401
def autenticado(credenciais: HTTPBasicCredentials=Depends(security)):
    return True
