from fastapi.security import HTTPBasicCredentials
from fastapi import HTTPException

from app.infra.database import Session
from app.models.entities import User
from app.infra.security import autenticado

import hashlib
import pytest

def test_autenticado(mocker):
    credenciais = HTTPBasicCredentials(username='admin', password='admin')
    mock_session = mocker.patch.object(Session, '__init__', return_value=None)
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = User(username='admin', password=hashlib.md5('admin'.encode()).hexdigest())
    
    assert autenticado(credenciais, mock_session) == True, 'A função autenticado não retornou True'

    credenciais = HTTPBasicCredentials(username='admin', password='admin')
    mock_session = mocker.patch.object(Session, '__init__', return_value=None)
    mock_session.query.return_value \
                .where.return_value \
                .first.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        autenticado(credenciais, mock_session)
    
    assert 'Credenciais inválidas' in str(excinfo.value), 'A função autenticado não retornou o erro correto'
